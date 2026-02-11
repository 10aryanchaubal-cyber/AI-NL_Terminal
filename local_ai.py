import subprocess
import json
import re
from config import AI_MODEL, AI_TIMEOUT

def run_llm(prompt):
    try:
        # Check if ollama is running first (simple ping check could be added in main, 
        # but here we just try-except properly)
        result = subprocess.run(
            ["ollama", "run", AI_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            encoding='utf-8',
            errors='ignore',
            timeout=AI_TIMEOUT
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""
    except Exception:
        return ""

def extract_json(text):
    """
    Robustly extract JSON object or array from LLM output using regex.
    """
    try:
        # Try to find a JSON object
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        
        # Try to find a JSON array
        match_arr = re.search(r'(\[.*\])', text, re.DOTALL)
        if match_arr:
            return json.loads(match_arr.group(1))
            
        return None
    except json.JSONDecodeError:
        return None

def ai_interpret(sentence):
    prompt = f"""
You are an NLP engine for a terminal assistant.
Extract intent and entities from the user's sentence.

Allowed intents:
CREATE_FOLDER, DELETE_FOLDER,
CREATE_FILE, DELETE_FILE,
RENAME_FILE, MOVE_FILE, COPY_FILE,
LIST_FILES, CURRENT_DIR,
GO_TO, GO_BACK, GO_HOME,
CAT_FILE, WHOAMI, SYSTEM_INFO

Sentence: "{sentence}"

Return ONLY valid JSON with this structure:
{{
  "intent": "INTENT_NAME",
  "entities": {{
    "name": "filename or foldername",
    "source": "source_path",
    "destination": "dest_path"
  }},
  "confidence": 0.0 to 1.0 (float)
}}
"""
    response = run_llm(prompt)
    data = extract_json(response)
    
    if data:
        return data
        
    return {"intent": "UNKNOWN", "entities": {}, "confidence": 0.0}

def ai_suggest_options(sentence):
    prompt = f"""
A user entered the following ambiguous command: "{sentence}"

Suggest up to 3 possible intended actions.
Return ONLY a JSON array:
[
  {{
    "intent": "INTENT_NAME",
    "entities": {{ "source": "", "destination": "", "name": "" }},
    "description": "Short human readable description"
  }}
]
"""
    response = run_llm(prompt)
    data = extract_json(response)
    return data if data else []

def ai_explain(topic):
    prompt = f"Explain the terminal command '{topic}' simply and briefly."
    return run_llm(prompt)

def ai_teach(topic):
    prompt = f"Teach a beginner how to use '{topic}' in the terminal. Provide examples."
    return run_llm(prompt)
