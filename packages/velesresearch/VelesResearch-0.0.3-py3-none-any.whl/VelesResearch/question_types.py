"Classes for different types of questions"

from typeguard import typechecked

from typing import Optional, List, Union, Sequence
from json import dumps
from options import QuestionOptions

@typechecked
class Question:
    "General question class"

    def __init__(self, label: str, question_type: str, question_text: str, *answers: Union[str, Sequence[str]], options: Optional[QuestionOptions]=None, description: Optional[str]=None):
        self.label = label
        self.question_type = question_type
        self.question_text = question_text
        self.answers = answers
        self.options = options
        self.description = description

    def __str__(self):
        answers = "  - " + "\n  - ".join(self.answers)
        return f"{self.label}:\n{self.question_text} ({self.question_type})\n{answers}"

    def __repr__(self):
        return f"Question({self.label})"

    def json(self):
        "Converts question to SurveyJS-compliant json"
        from structure import SurveyEncoder
        return dumps(self, cls=SurveyEncoder, indent=4)

def radio(self, label: str, question_text: str, *answers: Union[str, List[str]], options: Optional[QuestionOptions]=None, description: Optional[str]=None):
    "Single choice question"
    return Question(label, "radio", options, question_text, answers, options=options, description=description)

def radio(self, label: str, question_text: str, *answers: Union[str, List[str]], options: Optional[QuestionOptions]=None, description: Optional[str]=None):
    "Single choice question"
    return Question(label, "checkbox", options, question_text, answers, options=options, description=description)
