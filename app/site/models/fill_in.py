from typing import List, Optional


class FillInModel:
    TABLE = "questions"
    TYPE = "fillin"

    tags: List
    difficulty: int
    question_text: Optional[str]
    question_code: Optional[str]
    question_answer: str
