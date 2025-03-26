import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

class DocumentIndexer:
    def __init__(self, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the document indexer
        
        Args:
            embedding_model_name: Name of the HuggingFace embedding model to use
        """
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.k = 3  # Number of relevant chunks to retrieve
        
    def load_and_chunk_document(self, file_path, chunk_size=500, overlap=100):
        """
        Load a document and split it into overlapping chunks
        
        Args:
            file_path: Path to the document file
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
            
        Returns:
            List of document chunks
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            chunks = []
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if len(chunk) > 200:  # Only include substantive chunks
                    chunks.append(chunk)
            
            return chunks
        except Exception as e:
            print(f"Error loading document {file_path}: {e}")
            return []
    
    def create_faiss_index(self, texts, doc_source=None):
        """
        Create a FAISS vector index from text chunks
        
        Args:
            texts: List of text chunks
            doc_source: Source identifier for the documents
            
        Returns:
            FAISS index object or None if texts is empty
        """
        if not texts:
            return None
        metadatas = [{"source": doc_source, "index": i} for i in range(len(texts))] if doc_source else None
        return FAISS.from_texts(texts, self.embedding_model, metadatas=metadatas)
    
    def retrieve_relevant_text(self, question, vector_store, k=None):
        """
        Retrieve relevant document chunks based on a query
        
        Args:
            question: Query text
            vector_store: FAISS vector store
            k: Number of results to retrieve (defaults to self.k)
            
        Returns:
            List of relevant document chunks
        """
        if vector_store:
            return vector_store.similarity_search(question, k=k or self.k)
        return [] 