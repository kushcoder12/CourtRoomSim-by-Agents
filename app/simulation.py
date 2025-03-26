import re
import os
from datetime import datetime
from app.utils.text_processing import extract_scores

class CourtSimulation:
    def __init__(self, 
                 case_description, 
                 judge_agent, 
                 lawyer_for, 
                 lawyer_against,
                 document_indexer,
                 output_path):
        """
        Initialize courtroom simulation
        
        Args:
            case_description: Description of the legal case
            judge_agent: JudgeAgent instance
            lawyer_for: LawyerAgent for the motion
            lawyer_against: LawyerAgent against the motion
            document_indexer: DocumentIndexer instance
            output_path: Path to save transcript
        """
        self.case_description = case_description
        self.judge = judge_agent
        self.lawyer_for = lawyer_for
        self.lawyer_against = lawyer_against
        self.document_indexer = document_indexer
        self.output_path = output_path
        
        self.transcript = []
        self.for_arguments = []
        self.against_arguments = []
        self.judge_evaluations = []
        self.for_scores = {"legal_reasoning": 0, "evidence": 0, "persuasiveness": 0}
        self.against_scores = {"legal_reasoning": 0, "evidence": 0, "persuasiveness": 0}
    
    def add_to_transcript(self, text):
        """
        Add text to the transcript and print to console
        
        Args:
            text: Text to add
        """
        self.transcript.append(text)
        print(text)  # Print to console for monitoring
    
    def update_scores(self, evaluation):
        """
        Extract and update scores for both sides
        
        Args:
            evaluation: Judge's evaluation text
        """
        # Check if the evaluation text explicitly separates the two sides
        if "Book Authors" in evaluation and "LLM Companies" in evaluation:
            # Split by the section headers
            parts = re.split(r"(Book Authors|LLM Companies)", evaluation)

            for i, part in enumerate(parts):
                if "Book Authors" in part and i + 1 < len(parts):
                    for_text = parts[i] + parts[i + 1]
                    for_scores = extract_scores(for_text)
                    for key in for_scores:
                        self.for_scores[key] += for_scores[key]

                if "LLM Companies" in part and i + 1 < len(parts):
                    against_text = parts[i] + parts[i + 1]
                    against_scores = extract_scores(against_text)
                    for key in against_scores:
                        self.against_scores[key] += against_scores[key]
        else:
            # If no clear division, use the same scores for both
            scores = extract_scores(evaluation)
            for key in scores:
                self.for_scores[key] += scores[key]
                self.against_scores[key] += scores[key]
    
    def get_total_scores(self):
        """
        Calculate total scores for both sides
        
        Returns:
            Tuple of (for_total, against_total)
        """
        for_total = sum(self.for_scores.values())
        against_total = sum(self.against_scores.values())
        return for_total, against_total
    
    def run_simulation(self):
        """
        Run the full courtroom simulation
        """
        # Initialize transcript with header
        self.add_to_transcript("================================")
        self.add_to_transcript("AI COURTROOM PROCEEDINGS")
        self.add_to_transcript(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        self.add_to_transcript("Case: Authors vs. LLM Companies")
        self.add_to_transcript("================================\n")
        self.add_to_transcript(self.case_description.strip() + "\n")
        
        # PHASE 1: Opening Statements
        self.add_to_transcript("\n===== OPENING STATEMENTS =====\n")
        
        # Book Authors (For motion) opening
        for_opening = self.lawyer_for.generate_argument("opening", self.document_indexer)
        self.add_to_transcript(for_opening + "\n")
        self.for_arguments.append(for_opening)
        
        # LLM Companies (Against motion) opening
        against_opening = self.lawyer_against.generate_argument("opening", self.document_indexer)
        self.add_to_transcript(against_opening + "\n")
        self.against_arguments.append(against_opening)
        
        # Judge evaluates openings
        opening_eval = self.judge.evaluate_arguments(
            for_opening, against_opening, "opening", self.document_indexer)
        self.add_to_transcript(opening_eval + "\n")
        self.judge_evaluations.append(opening_eval)
        
        # Update scores
        self.update_scores(opening_eval)
        
        # PHASE 2: First Round of Rebuttals
        self.add_to_transcript("\n===== FIRST REBUTTALS =====\n")
        
        # Extract just the statement part from opening arguments (removing agent labels)
        against_opening_content = re.sub(r"^.*?\):\s*", "", against_opening)
        for_opening_content = re.sub(r"^.*?\):\s*", "", for_opening)
        
        # For side rebuts against opening
        for_rebuttal = self.lawyer_for.generate_argument(
            "rebuttal", 
            self.document_indexer,
            rebuttal_to=against_opening_content
        )
        self.add_to_transcript(for_rebuttal + "\n")
        self.for_arguments.append(for_rebuttal)
        
        # Against side rebuts for opening
        against_rebuttal = self.lawyer_against.generate_argument(
            "rebuttal",
            self.document_indexer,
            rebuttal_to=for_opening_content
        )
        self.add_to_transcript(against_rebuttal + "\n")
        self.against_arguments.append(against_rebuttal)
        
        # Judge evaluates first rebuttals
        rebuttal1_eval = self.judge.evaluate_arguments(
            for_rebuttal, against_rebuttal, "rebuttal", self.document_indexer)
        self.add_to_transcript(rebuttal1_eval + "\n")
        self.judge_evaluations.append(rebuttal1_eval)
        
        # Update scores
        self.update_scores(rebuttal1_eval)
        
        # PHASE 3: Second Round of Rebuttals
        self.add_to_transcript("\n===== SECOND REBUTTALS =====\n")
        
        # Extract just the statement part from first rebuttals
        against_rebuttal_content = re.sub(r"^.*?\):\s*", "", against_rebuttal)
        for_rebuttal_content = re.sub(r"^.*?\):\s*", "", for_rebuttal)
        
        # For side rebuts against's first rebuttal
        for_rebuttal2 = self.lawyer_for.generate_argument(
            "rebuttal",
            self.document_indexer,
            rebuttal_to=against_rebuttal_content
        )
        self.add_to_transcript(for_rebuttal2 + "\n")
        self.for_arguments.append(for_rebuttal2)
        
        # Against side rebuts for's first rebuttal
        against_rebuttal2 = self.lawyer_against.generate_argument(
            "rebuttal",
            self.document_indexer,
            rebuttal_to=for_rebuttal_content
        )
        self.add_to_transcript(against_rebuttal2 + "\n")
        self.against_arguments.append(against_rebuttal2)
        
        # Judge evaluates second rebuttals
        rebuttal2_eval = self.judge.evaluate_arguments(
            for_rebuttal2, against_rebuttal2, "rebuttal", self.document_indexer)
        self.add_to_transcript(rebuttal2_eval + "\n")
        self.judge_evaluations.append(rebuttal2_eval)
        
        # Update scores
        self.update_scores(rebuttal2_eval)
        
        # PHASE 4: Closing Arguments
        self.add_to_transcript("\n===== CLOSING ARGUMENTS =====\n")
        
        # Book Authors closing
        for_closing = self.lawyer_for.generate_argument("closing", self.document_indexer)
        self.add_to_transcript(for_closing + "\n")
        self.for_arguments.append(for_closing)
        
        # LLM Companies closing
        against_closing = self.lawyer_against.generate_argument("closing", self.document_indexer)
        self.add_to_transcript(against_closing + "\n")
        self.against_arguments.append(against_closing)
        
        # PHASE 5: Final Verdict
        self.add_to_transcript("\n===== FINAL VERDICT =====\n")
        
        # Display current scores
        for_total, against_total = self.get_total_scores()
        score_summary = f"""
SCORES SUMMARY:
BOOK AUTHORS:
- Legal Reasoning: {self.for_scores['legal_reasoning']}
- Evidence: {self.for_scores['evidence']}
- Persuasiveness: {self.for_scores['persuasiveness']}
- TOTAL: {for_total}

LLM COMPANIES:
- Legal Reasoning: {self.against_scores['legal_reasoning']}
- Evidence: {self.against_scores['evidence']}
- Persuasiveness: {self.against_scores['persuasiveness']}
- TOTAL: {against_total}
"""
        self.add_to_transcript(score_summary)
        
        # Judge renders final verdict
        final_verdict = self.judge.evaluate_arguments(
            for_closing, against_closing, "FINAL", self.document_indexer)
        self.add_to_transcript(final_verdict)
        
        # Add closing to transcript
        self.add_to_transcript("\n================================")
        winner = "BOOK AUTHORS" if for_total > against_total else "LLM COMPANIES"
        self.add_to_transcript(f"The court rules in favor of: {winner}")
        self.add_to_transcript("================================")
        
        # Save transcript to file
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.transcript))
        
        print(f"Courtroom simulation complete. Transcript saved to {self.output_path}")
        return self.transcript 