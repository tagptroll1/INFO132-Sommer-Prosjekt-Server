from typing import List, NamedTuple


class Table(NamedTuple):
    primary_key: str
    keys: List[str]
    locked: bool = True


TABLES = {
    "multi_choice": Table(
        primary_key="id",
        keys=sorted([
            "id",
            "tags",             # str (comma seperated)
            "difficulty",       # int
            "question_text",    # str
            "question_answer",  # str
            "choices"           # str (comma seperated)
        ])
    ),
}
