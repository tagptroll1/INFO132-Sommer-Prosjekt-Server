from typing import List


class MultiChoiceModel:
    TABLE = "questions"
    TYPE = "multichoice"

    tags: List
    difficulty: int
    question_text: str
    question_code: str
    question_answer: str
    alternatives: List
