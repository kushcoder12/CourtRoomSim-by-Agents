from app.utils.text_processing import generate_response

class JudgeAgent:
    def __init__(self, model, tokenizer, combined_vector_store, case_description):
        """
        Initialize judge agent
        
        Args:
            model: AI language model
            tokenizer: Model tokenizer
            combined_vector_store: FAISS vector store with combined documents
            case_description: Description of the legal case
        """
        self.model = model
        self.tokenizer = tokenizer
        self.vector_store = combined_vector_store
        self.case_description = case_description
        
    def evaluate_arguments(self, for_argument, against_argument, stage, document_indexer):
        """
        Evaluate lawyer arguments with clear scoring
        
        Args:
            for_argument: Text of "for" side argument
            against_argument: Text of "against" side argument
            stage: Current stage of the simulation ("opening", "rebuttal", "FINAL")
            document_indexer: DocumentIndexer instance
            
        Returns:
            Judge's evaluation text
        """
        # Gather relevant legal principles
        query = "Key legal principles for fair use and copyright in digital contexts"
        docs = document_indexer.retrieve_relevant_text(query, self.vector_store, k=4)
        legal_context = "\n\n".join([doc.page_content for doc in docs])
        
        prompt = f"""Case: {self.case_description}

Legal Context:
{legal_context}

Book Authors' argument:
{for_argument}

LLM Companies' argument:
{against_argument}

As the Judge, evaluate these {stage} arguments concisely. If final verdict, state winner with reasoning. Otherwise, score each side (1-10) and score should not be same for both on: Legal Reasoning, Evidence, Persuasiveness.
"""
        
        response = generate_response(prompt, self.model, self.tokenizer, max_tokens=512)
        
        # Let's ensure scores are present if not final verdict
        from app.utils.text_processing import extract_scores
        if stage != "FINAL" and not any(keyword in response.lower() for keyword in ["score", "rating", "point", "legal reasoning", "evidence", "persuasiveness"]):
            # Add default scoring if none detected
            response += "\n\nScores - Book Authors: Legal Reasoning: 7, Evidence: 7, Persuasiveness: 7. LLM Companies: Legal Reasoning: 7, Evidence: 7, Persuasiveness: 7."
        
        return f"Judge ({stage}):\n{response}" 