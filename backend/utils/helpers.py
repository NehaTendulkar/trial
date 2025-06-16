
import re

def extract_json(text: str) -> str:
    """Extract JSON object from text (e.g., removing markdown)."""
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else text
