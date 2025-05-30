from typing import List

from pydantic import BaseModel


class QuizDataItem(BaseModel):
    """
    quiz data dict item
    """
    question: str
    options: List[str]
    correct_option: int


