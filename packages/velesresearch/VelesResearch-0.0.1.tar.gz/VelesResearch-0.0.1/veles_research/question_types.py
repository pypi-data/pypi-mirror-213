"Classes for different types of questions"

from typeguard import typechecked

from typing import Optional, List
from json import dumps
from options import Question_options

@typechecked
class Question:
    "General question class"

    def __init__(self, label: str, question_type: str, question_text: str, answers: List[str], options: Optional[Question_options]=None, description: Optional[str]=None):
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


def radio(label, options, question_text, answers):
    "Single choice question"
    return Question(label, "radio", options, question_text, answers)


def checkbox(label, options, question_text, answers):
    "Multiple choice question class"
    return Question(label, "checkbox", options, question_text, answers)
