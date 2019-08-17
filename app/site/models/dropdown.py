from typing import List


class DropdownModel:
    TABLE = "questions"
    TYPE = "dropdown"

    tags: List
    difficulty: int
    question_text: str
    question_code: str
    question_answer: str
    alternatives: List
