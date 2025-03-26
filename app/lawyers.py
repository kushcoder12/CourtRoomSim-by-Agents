import re
from app.utils.text_processing import generate_response

class LawyerAgent:
    def __init__(self, side, model, tokenizer, vector_store, case_description):
        """
        Initialize lawyer agent
        
        Args:
            side: "for" or "against" the motion
            model: AI language model
            tokenizer: Model tokenizer
            vector_store: FAISS vector store for relevant documents
            case_description: Description of the legal case
        """
        self.side = side
        self.model = model
        self.tokenizer = tokenizer
        self.vector_store = vector_store
        self.case_description = case_description
        
        if side == "for":
            self.agent_name = "Book Authors' Counsel"
            self.position = "arguing for copyright protection and compensation for all works used to train LLMs."
        else:
            self.agent_name = "LLM Companies' Counsel"
            self.position = "arguing that using published works falls under fair use without requiring additional permissions"
            
    def generate_argument(self, stage, document_indexer, previous_arguments=None, rebuttal_to=None):
        """
        Generate a lawyer argument
        
        Args:
            stage: "opening", "rebuttal", or "closing"
            document_indexer: DocumentIndexer instance
            previous_arguments: List of previous arguments (optional)
            rebuttal_to: Text to rebut (optional, for rebuttal stage)
            
        Returns:
            Generated argument text with agent label
        """
        # Build query based on stage
        if stage == "opening":
            query = f"Legal arguments {self.position}"
        elif stage == "rebuttal" and rebuttal_to:
            query = f"Counter this: {rebuttal_to}"
        elif stage == "closing":
            query = f"Summarize strongest points {self.position}"
        else:
            query = f"Legal arguments for {self.side} side in copyright case"
        
        # Retrieve relevant document sections
        docs = document_indexer.retrieve_relevant_text(query, self.vector_store)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Build concise prompt - critically, we don't want to overwhelm the model
        prompt = f"""Case: {self.case_description}

Document Context:
{context}

As the {self.agent_name}, {self.position}, provide a concise and powerful {stage} statement. """
        
        if stage == "rebuttal":
            prompt += f"Directly counter this argument: '{rebuttal_to}'"
        
        # Generate the response with length control
        response = generate_response(prompt, self.model, self.tokenizer, max_tokens=180)
        
        # Ensure we have a complete statement
        if not response.endswith(('.', '!', '?')):
            response += "."
        
        return f"{self.agent_name} ({stage}): {response}" 