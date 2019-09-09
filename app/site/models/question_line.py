from typing import List


class QuestionLineModel:
    TABLE = "questions"
    TYPE = "questionline"

    tags: List
    difficulty: int
    question_text: str
    # Each line of code
    question_code: List
    # The answer if which line number is correct
    question_answer: int
