from typeguard import typechecked

from typing import List
from question_types import Question
from structure import *

def questionnaire(label, items, answers, question_type="radio", options=None, description=None) -> List[Question]:
    "Convert whole questionnaire to Question objects list"
    q_list = []
    for i in enumerate(items):
        q_list.append(Question(f"{label}_{i[0] + 1}", question_type, i[1], answers, options=options, description=description))
    return q_list

def survey(*pages: Union[Page, List[Page]], title: Optional[str]=None, description: Optional[str]=None):
    "Create Survey object from pages, create json file"
    s = Survey(pages, title=title, description=description)
    s.create()
    return s
