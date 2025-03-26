import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_path):
    """
    Load a language model and its tokenizer
    
    Args:
        model_path: Path to the model directory
        
    Returns:
        Tuple of (model, tokenizer)
    """
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        torch_dtype=torch.float16, 
        device_map="auto"
    )
    model.gradient_checkpointing_enable()
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer 