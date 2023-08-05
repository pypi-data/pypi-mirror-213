from typeguard import typechecked

from typing import Optional

@typechecked
class Question_options:
    def __init__(self, required: bool=False, answers_order: str="none", inherit_answers: Optional[str]=None, comment: bool=False, comment_text: str="Other", comment_placeholder: str="", visible: bool=True):
        self.required = required
        self.answers_order = answers_order
        self.inherit_answers = inherit_answers
        self.comment = comment
        self.comment_text = comment_text
        self.comment_placeholder = comment_placeholder
        self.visible = visible

class Page_options:
    def __init__(self, read_only: bool=False, time_limit: Optional[int]=None, visible: bool=True):
        self.read_only = read_only
        self.time_limit = time_limit
        self.visible = visible
        
class Survey_options:
    def __init__(self, language: str="en", url_on_complete: Optional[str]=None):
        self.language = language
        self.url_on_complete = url_on_complete
