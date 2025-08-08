# Use llama3.2 via local Ollama API for resume analysis
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"  # or "llama3.2" if that's the tag

def analyze_resume_text(resume_text, prompt=None):
    """
    Uses local Ollama llama3.2 model to analyze resume text.
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
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": input_text
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        # Ollama streams newline-delimited JSON objects
        lines = response.text.strip().split('\n')
        import json
        all_text = ""
        for line in lines:
            try:
                obj = json.loads(line)
                all_text += obj.get("response", "")
            except Exception:
                continue
        # Return only the first 20 words for review
        review = " ".join(all_text.split()[:100])
        return review
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

# Test the function
if __name__ == "__main__":
    test_text = "Robert Smith\nSoftware Engineer\nExperience: 5 years in Python and JavaScript development."
    sys_prompt = "Analyze this resume and provide feedback on skills and experience."
    result = analyze_resume_text(test_text, sys_prompt)
    print("LLM Analysis:\n", result)

