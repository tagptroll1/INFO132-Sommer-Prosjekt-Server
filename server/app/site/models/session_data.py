from typing import List, Optional


class DataModel:
    TABLE = "data"

    user_id: str
    question_id: str
    selected_answer: str
    started_question: str  # string version of DateTime 
    ended_question: str  # string version of DateTime 
    
