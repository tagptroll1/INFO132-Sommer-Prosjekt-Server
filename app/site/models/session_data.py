from typing import List, Optional


class DataModel:
    TABLE = "data"

    user: str
    start_time: str
    end_time: str
    questions: List
        # List of
        # question_id
        # selected_answer
        # correct
        # time_spent

class QuestionDataModel:
    question_id: str
    selected_answer: str
    correct: bool
    time_spent: int # seconds
    
