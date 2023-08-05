from typeguard import typechecked

from typing import Union, List, Optional
from json import JSONEncoder
from numpy import concatenate, array
from question_types import Question

@typechecked
class Page:
    def __init__(self, label: str, *questions: Union[Question, List[Question]], title: Optional[str]=None, description: Optional[str]=None, options: Optional[Page_options]=None):
        self.label = label
        self.questions = list(concatenate([questions]).flat)
        self.title = title
        self.description = description

@typechecked
class Survey:
    def __init__(self, *pages: Union[Page, List[Page]], title: Optional[str]=None, description: Optional[str]=None, options: Optional[Survey_options]=None):
        self.pages = list(concatenate([pages]).flat)
        self.title = title
        self.description = description
        self.language = language
    
    def json(self):
        from json import dumps
        return dumps(obj=self, cls=SurveyEncoder, indent=2)
    
    def create(self):
        from json import dumps
        json = dumps(obj=self, cls=SurveyEncoder, indent=2)
        f = open("survey.json", "w")
        f.write(json)
        f.close()

class SurveyEncoder(JSONEncoder):
    "Create SurveyJS-compliant json from Question object"

    def default(self, o):
        if isinstance(o, Survey):
            json = {
                "title": o.title,
                "description": o.description,
                "pages": [self.default(p) for p in o.pages]
            }
            
            if o.options:
                opts = o.options.__dict__
                if opts["language"] != "en":
                    json["locale"] = opts["language"]
                if opts["url_on_complete"]:
                    json["navigateToUrl"] = opts["url_on_complete"]
            
        elif isinstance(o, Page):
            json = {
                "name": o.label,
                "elements": [self.default(q) for q in o.questions],
            }
            
            if o.title:
                json["title"] = o.title
            if o.description:
                json["description"] = o.description
            if o.options:
                opts = o.options.__dict__
                if opts["read_only"]:
                    json["readOnly"] = True
                if opts["time_limit"]:
                    json["maxTimeToFinish"] = opts["time_limit"]
                if not opts["visible"]:
                    json["visible"] = False
       
        else:
            # SurveyJS types dictionary
            surveyjs_types = {"radio": "radiogroup", "checkbox": "checkbox"}
            
            json = {
                "name": o.label,
                "type": surveyjs_types[o.question_type],
                "title": o.question_text,
                "choices": o.answers
            }
            
            if o.description:
                json["description"] = o.description
                
            if o.options:
                opts = o.options.__dict__
                if not opts["visible"]:
                    json["visible"] = False
                if opts["required"]:
                    json["isRequired"] = True
                if opts["answers_order"] != "none":
                    json["choicesOrder"] = opts["answers_order"]
                if opts["inherit_answers"]:
                    json["choicesFromQuestion"] = opts["inherit_answers"]
                if opts["comment"]:
                    json["showCommentArea"] = True
                    json["commentText"] = opts["comment_text"]
                    json["commentPlaceholder"] = opts["comment_placeholder"]
            
        return json
