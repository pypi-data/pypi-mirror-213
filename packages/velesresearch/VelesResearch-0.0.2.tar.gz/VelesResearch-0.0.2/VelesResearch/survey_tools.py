from typeguard import typechecked

from typing import List
from question_types import Question
from structure import *

def question(label: str, question_type: str, question_text: str, *answers: Union[str, List[str]], options: Optional[QuestionOptions]=None, description: Optional[str]=None, options: Optional[PageOptions]=None):
    "Wrapper around Question class"
    return Question(label, question_type, question_text, answers, options=options, description=description)

def questionnaire(label, items, answers, question_type="radio", options=None, description=None) -> List[Question]:
    "Convert whole questionnaire to Question objects list"
    q_list = []
    for i in enumerate(items):
        q_list.append(Question(f"{label}_{i[0] + 1}", question_type, i[1], answers, options=options, description=description))
    return q_list

def page(label: str, *questions: Union[Question, List[Question]], title: Optional[str]=None, description: Optional[str]=None, options: Optional[PageOptions]=None):
    "Wrapper around Page class"
    return Page(label, questions, title=title, description=description, options=options)

def survey(*pages: Union[Page, List[Page]], title: Optional[str]=None, description: Optional[str]=None):
    "Create Survey object from pages, create json file"
    s = Survey(pages, title=title, description=description)
    s.create()
    return s
