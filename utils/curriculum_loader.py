import json
from pathlib import Path

def load_curriculum(grade):
    curriculum_path = Path("curriculum") / f"{grade.lower()}_ela_curriculum.json"
    if curriculum_path.exists():
        with open(curriculum_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}
