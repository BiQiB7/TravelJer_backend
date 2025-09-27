import json

def extract_json_from_string(s: str) -> dict:
    """
    Extracts a JSON object from a string, which might be inside a markdown code block.
    """
    try:
        # Find the start of the JSON object
        start_index = s.find('{')
        # Find the end of the JSON object
        end_index = s.rfind('}') + 1
        
        if start_index == -1 or end_index == 0:
            raise ValueError("No JSON object found in the string.")
            
        json_str = s[start_index:end_index]
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Failed to decode JSON: {e}")