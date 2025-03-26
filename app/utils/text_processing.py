import re
import torch

def clean_response(response):
    """
    Clean and format AI response to be concise and complete
    
    Args:
        response: Raw text response from model
        
    Returns:
        Cleaned and formatted response
    """
    # Remove any potential prefixes the model might generate
    response = re.sub(r'^.*?(Lawyer|Judge):', '', response, flags=re.DOTALL)
    
    # Trim to complete sentences
    sentences = re.split(r'(?<=[.!?])\s+', response)
    if len(sentences) > 10:  # If response is long, keep only the first 5 sentences
        response = ' '.join(sentences[:5])
    
    # Remove any trailing incomplete sentences
    if not response.endswith(('.', '!', '?')):
        last_period = max(response.rfind('.'), response.rfind('!'), response.rfind('?'))
        if last_period > 0:
            response = response[:last_period+1]
            
    return response.strip()

def generate_response(prompt, model, tokenizer, max_tokens=250):
    """
    Generate a concise response from an AI model
    
    Args:
        prompt: Input prompt text
        model: AI language model
        tokenizer: Model tokenizer
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        Generated response text
    """
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            with torch.cuda.amp.autocast():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (after the prompt)
        if response.startswith(prompt):
            response = response[len(prompt):].strip()
            
        # Clean and format the response
        response = clean_response(response)
        
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error generating response."
    finally:
        # Clean up memory
        torch.cuda.empty_cache()

def extract_scores(evaluation):
    """
    Extract numeric scores from judge's evaluation text
    
    Args:
        evaluation: Judge's evaluation text
        
    Returns:
        Dictionary of scores
    """
    scores = {"legal_reasoning": 0, "evidence": 0, "persuasiveness": 0}
    
    # Look for patterns like "Legal Reasoning: 8", etc.
    legal_match = re.search(r"Legal Reasoning:?\s*(\d+)", evaluation, re.IGNORECASE)
    evidence_match = re.search(r"Evidence:?\s*(\d+)", evaluation, re.IGNORECASE)
    persuasive_match = re.search(r"Persuasiveness:?\s*(\d+)", evaluation, re.IGNORECASE)
    
    if legal_match:
        scores["legal_reasoning"] = int(legal_match.group(1))
    if evidence_match:
        scores["evidence"] = int(evidence_match.group(1))
    if persuasive_match:
        scores["persuasiveness"] = int(persuasive_match.group(1))
        
    # If no scores found, assign default scores
    if sum(scores.values()) == 0:
        scores = {"legal_reasoning": 7, "evidence": 7, "persuasiveness": 7}
        
    return scores 