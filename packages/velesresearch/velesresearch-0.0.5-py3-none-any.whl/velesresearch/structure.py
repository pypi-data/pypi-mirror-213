"Structural elements of the survey"
from collections.abc import Sequence
from json import JSONEncoder, dumps
import numpy as np
from .options import QuestionOptions, PageOptions, SurveyOptions


class Question:
    "General question class"

    def __init__(
        self,
        label: str,
        question_type: str,
        question_text: str,
        *answers: str | Sequence[str],
        options: QuestionOptions | None = None,
        description: str | None = None,
    ):
        self.label = label
        self.question_type = question_type
        self.question_text = question_text
        self.answers = list(np.concatenate([answers]).flat)
        self.options = options
        self.description = description

    def __str__(self):
        answers = "  - " + "\n  - ".join(self.answers)
        return (
            f"{self.label}:\n  {self.question_text} ({self.question_type})\n{answers}"
        )

    def __repr__(self):
        return f"Question({self.label})"


class Page:
    "General page class"

    def __init__(
        self,
        label: str,
        *questions: Question | Sequence[Question],
        title: str | None = None,
        description: str | None = None,
        options: PageOptions | None = None,
    ):
        self.label = label
        self.questions = list(np.concatenate([questions]).flat)
        self.title = title
        self.description = description
        self.options = options

    def __str__(self):
        page = f"Page {self.label}:\n"
        for i in enumerate(self.questions):
            page += f"  {i[0] + 1}. {i[1].label}\n"
        return page


class Survey:
    "General survey class"

    def __init__(
        self,
        *pages: Page | Sequence[Page],
        title: str | None = None,
        description: str | None = None,
        options: SurveyOptions | None = None,
    ):
        self.pages = list(np.concatenate([pages]).flat)
        self.title = title
        self.description = description
        self.options = options

    def create(self):
        "Saves survey to survey.json file"
        json = dumps(obj=self, cls=SurveyEncoder, indent=2)
        survey_file = open("survey.json", "w", encoding="utf-8")
        survey_file.write(json)
        survey_file.close()


class SurveyEncoder(JSONEncoder):
    "Create SurveyJS-compliant json from Question object"

    def default(self, o):
        if isinstance(o, Survey):
            json = {
                "title": o.title,
                "description": o.description,
                "pages": [self.default(p) for p in o.pages],
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
                "choices": o.answers,
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
                    if opts["comment_text"]:
                        json["commentText"] = opts["comment_text"]
                    if opts["comment_placeholder"]:
                        json["commentPlaceholder"] = opts["comment_placeholder"]
                if opts["other"]:
                    json["showOtherItem"] = True
                    if opts["other_text"]:
                        json["otherText"] = opts["other_text"]
                    if opts["other_placeholder"]:
                        json["otherPlaceHolder"] = opts["other_placeholder"]
                if opts["none"]:
                    json["showNoneItem"] = True
                    if opts["none_text"]:
                        json["noneText"] = opts["none_text"]
                if opts["clear_button"]:
                    json["showClearButton"] = True

        return json
