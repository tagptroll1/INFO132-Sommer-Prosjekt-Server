from typing import List


class DataModel:
    TABLE = "data"

    user: str
    start_time: str
    end_time: str
    questions: List


class QuestionDataModel:
    question_id: str
    selected_answer: str
    correct: bool
    time_spent: int  # seconds
