import pandas as pd
from datetime import datetime
from typing import List
from models.schema import ProblemStatement

def load_excel_data(filepath: str) -> List[ProblemStatement]:
    df = pd.read_excel(filepath)

    # Define mapping from Excel columns to our schema fields
    excel_column_map = {
        "Problem Title": "title",
        "Problem Description": "description",
        "Domain": "category",
        "Level": "difficulty_level",
        "Technology": "tech_stack"
    }

    standardized_data = []

    for _, row in df.iterrows():
        tech_stack_raw = row.get("Technology", "")
        tech_list = [tech.strip() for tech in str(tech_stack_raw).split(',')] if tech_stack_raw else []

        schema_entry = ProblemStatement(
            title=row.get("Problem Title", ""),
            description=row.get("Problem Description", ""),
            category=row.get("Domain", None),
            difficulty_level=row.get("Level", "Medium"),
            tech_stack=tech_list,
            source="SIH_2023",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        standardized_data.append(schema_entry)

    return standardized_data
