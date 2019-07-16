from typing import List


class MultiChoiceModel:
    TABLE = "multi_choice"

    tags: List
    difficulty: int
    question_text: str
    question_code: str
    question_answer: str
    choices: List
