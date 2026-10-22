import json 
"""This function converts the data into a py dictionary"""
def to_obj(s):
        try:
            s = s.strip()
            if s.startswith("```json"): s = s[7:]
            elif s.startswith("```"): s = s[3:]
            if s.endswith("```"): s = s[:-3]
            import json
            return json.loads(s.strip())
        except Exception:
            return {}