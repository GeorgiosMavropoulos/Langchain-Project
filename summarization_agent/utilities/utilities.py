import json 
"""This function converts the data into a structured json format"""
def to_obj(s):
    try:
        return json.loads(s)
    except Exception:
        return {}