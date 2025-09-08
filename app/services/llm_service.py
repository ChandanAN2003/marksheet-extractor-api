import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def get_extraction_prompt(extracted_text: str):
    return f"""
    You are a specialized AI for extracting structured data from academic marksheets.
    Analyze the provided raw marksheet text and output a JSON object strictly following the schema below. If a field is not found, set its value to null.
    For each extracted field, provide a "value" and a "confidence" score from 0.0 to 1.0, where 1.0 is absolute certainty. The confidence score should reflect how certain you are that the extracted value is correct and directly from the text.

    Marksheet Text:
    ```
    {extracted_text}
    ```

    JSON Schema:
    {{
      "candidate_details": {{
        "name": {{"value": "...", "confidence": "..."}},
        "fathers_name": {{"value": "...", "confidence": "..."}},
        "roll_no": {{"value": "...", "confidence": "..."}},
        "registration_no": {{"value": "...", "confidence": "..."}},
        "dob": {{"value": "...", "confidence": "..."}},
        "exam_year": {{"value": "...", "confidence": "..."}},
        "board_university": {{"value": "...", "confidence": "..."}},
        "institution": {{"value": "...", "confidence": "..."}}
      }},
      "subject_marks": [
        {{
          "subject": {{"value": "...", "confidence": "..."}},
          "max_marks": {{"value": "...", "confidence": "..."}},
          "obtained_marks": {{"value": "...", "confidence": "..."}},
          "grade": {{"value": "...", "confidence": "..."}}
        }}
      ],
      "overall_result": {{"value": "...", "confidence": "..."}},
      "issue_date": {{"value": "...", "confidence": "..."}},
      "issue_place": {{"value": "...", "confidence": "..."}}
    }}
    """

def extract_data_with_llm(text: str):
    try:
        response = model.generate_content(get_extraction_prompt(text))
        json_string = response.text.strip().strip('`').lstrip('json').strip()
        return json.loads(json_string)
    except Exception as e:
        print(f"Error from LLM service: {e}")
        return None