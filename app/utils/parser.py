import json
import re


def _extract_json_text(result):
    content = result

    if isinstance(result, dict):
        content = result.get("response")

        if not content:
            candidates = result.get("candidates") or []

            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text_parts = [
                    part.get("text", "")
                    for part in parts
                    if isinstance(part, dict) and part.get("text")
                ]
                content = "\n".join(text_parts)

    if not isinstance(content, str):
        raise Exception("Response text not found")

    content = content.strip()
    return re.sub(r"^```json\s*|\s*```$", "", content, flags=re.MULTILINE).strip()


def parse_llm_response(result):
    try:
        content = _extract_json_text(result)
        parsed = json.loads(content)
        return parsed.get("motivations", [])
    except Exception as e:
        raise Exception(f"Invalid JSON from LLM: {str(e)}")


def parse_motor_response(result):
    try:
        content = _extract_json_text(result)
        parsed = json.loads(content)
        return parsed.get("motors", [])
    except Exception as e:
        raise Exception(f"Invalid motor JSON from LLM: {str(e)}")
