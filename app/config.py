import os

class SimulationConfig:
    """Configuration class for courtroom simulation"""
    
    # Default case description
    DEFAULT_CASE_DESCRIPTION = """
This case concerns the rights of book authors versus LLM companies regarding the use of copyrighted literary 
works for training large language models without explicit permission or compensation to the authors.
"""
    
    def __init__(self, 
                 case_description=None,
                 for_motion_doc=None,
                 against_motion_doc=None,
                 transcript_output=None,
                 judge_model_path=None,
                 lawyer_for_model_path=None,
                 lawyer_against_model_path=None):
        """
        Initialize simulation configuration
        
        Args:
            case_description: Description of the case
            for_motion_doc: Path to document arguing for the motion
            against_motion_doc: Path to document arguing against the motion
            transcript_output: Path to save transcript output
            judge_model_path: Path to judge model
            lawyer_for_model_path: Path to model for lawyer arguing for the motion
            lawyer_against_model_path: Path to model for lawyer arguing against the motion
        """
        # Use provided values or defaults
        self.case_description = case_description or self.DEFAULT_CASE_DESCRIPTION
        
        # Set default paths relative to current directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        
        # Input document paths
        self.for_motion_doc = for_motion_doc or os.path.join(data_dir, "inputs", "for_motion.txt")
        self.against_motion_doc = against_motion_doc or os.path.join(data_dir, "inputs", "against_motion.txt")
        
        # Output path
        self.transcript_output = transcript_output or os.path.join(base_dir, "courtroom_transcript.txt")
        
        # Model paths
        # These should be provided by user, no good defaults for local paths
        self.judge_model_path = judge_model_path
        self.lawyer_for_model_path = lawyer_for_model_path
        self.lawyer_against_model_path = lawyer_against_model_path
        
    def validate(self):
        """
        Validate configuration settings
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if all necessary model paths are specified
        if not self.judge_model_path:
            return False, "Judge model path is required"
        if not self.lawyer_for_model_path:
            return False, "Lawyer 'for' model path is required"
        if not self.lawyer_against_model_path:
            return False, "Lawyer 'against' model path is required"
            
        # Check if input documents exist
        if not os.path.exists(self.for_motion_doc):
            return False, f"Document for motion not found at {self.for_motion_doc}"
        if not os.path.exists(self.against_motion_doc):
            return False, f"Document against motion not found at {self.against_motion_doc}"
            
        # Ensure output directory exists
        output_dir = os.path.dirname(self.transcript_output)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                return False, f"Could not create output directory {output_dir}: {e}"
                
        return True, "" 