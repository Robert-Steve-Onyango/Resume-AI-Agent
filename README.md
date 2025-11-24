# AI Resume Reader

Analyzes resume text using a local Ollama LLM (default model: **`llama3.2`**) and returns an LLM-generated summary or feedback.

---

## Key File

**`ai_engine.py`**

- Exposes: `analyze_resume_text(resume_text, prompt=None)`
- Sends a POST request to a local Ollama API
- Parses newline-delimited JSON (NDJSON)
- Concatenates all `"response"` fields
- Returns the **first 100 words** of the model output  
  *(Note: code comment mentions 20 words, but actual return is 100)*

---

## Prerequisites

- Python 3.x  
- `requests` library (`pip install requests`)  
- Ollama running locally and reachable at `http://localhost:11434`  
  - (Update `OLLAMA_URL` if using another host/port)
- The target model installed in Ollama  
  - Default: `OLLAMA_MODEL = "llama3.2"`

---

## How to Run (Minimal)

1. Install Python dependencies:
   ```bash
   pip install requests
2. Run the built-in test:
```bash
python ai_engine.py

