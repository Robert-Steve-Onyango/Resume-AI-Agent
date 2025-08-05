from parsing import extract_text_from_pdf

# Use a free LLM model via transformers (e.g., distilbert-base-uncased for demonstration)
from transformers import pipeline

# Load a basic text-generation pipeline (can be replaced with a more advanced LLM)
generator = pipeline('text-generation', model='distilgpt2')

def analyze_resume_text(resume_text, prompt=None):
    """
    Uses a free LLM model to analyze resume text.
    Args:
        resume_text (str): The extracted resume text.
        prompt (str, optional): An optional prompt for the LLM.
    Returns:
        str: LLM-generated output.
    """
    if prompt:
        input_text = prompt + "\n" + resume_text
    else:
        input_text = resume_text
    result = generator(input_text, max_length=200, num_return_sequences=1)
    return result[0]['generated_text']
