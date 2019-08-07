from typing import List, Optional


class DataModel:
    TABLE = "data"

    user: str
    question_id: str
    selected_answer: str
    correct: bool
    ended_question: str  # string version of DateTime 
    
