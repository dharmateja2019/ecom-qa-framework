import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

def ask_llm(prompt: str, timeout: int = 30) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.Timeout:
        return "LLM_TIMEOUT"
    except Exception as e:
        return f"LLM_ERROR: {str(e)}"

def validate_product_response(product: dict) -> dict:
    prompt = f"""
You are a QA engineer reviewing an API response.
Analyze this product data and respond ONLY with valid JSON:
{{
  "is_valid": true or false,
  "issues": ["list of issues if any"],
  "confidence": "high/medium/low"
}}

Product data:
{json.dumps(product, indent=2)}

Check for: missing fields, unrealistic prices, 
empty titles, invalid ratings.
Respond with JSON only, no explanation.
"""
    result = ask_llm(prompt, timeout=60)
    
    if result in ("LLM_TIMEOUT", "") or result.startswith("LLM_ERROR"):
        return {"is_valid": None, "issues": ["LLM failed to respond"], 
                "confidence": "none"}
    
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        json_str = result[start:end]
        return json.loads(json_str)
    except:
        return {"is_valid": None, "issues": ["LLM returned invalid JSON"], 
                "confidence": "none"}

def suggest_test_cases(sample_response: dict) -> str:
    prompt = f"""
You are a senior QA engineer. 
Given this sample API response, suggest 5 test cases.

Sample response: {json.dumps(sample_response, indent=2)}

Format each as:
- Test name: [name]
  Scenario: [what to test]
  Why: [why this matters]

Focus on edge cases, security, business logic.
"""
    return ask_llm(prompt, timeout=90)