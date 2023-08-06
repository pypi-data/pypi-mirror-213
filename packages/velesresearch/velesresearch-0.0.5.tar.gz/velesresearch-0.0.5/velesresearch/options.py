"Options objects definitions"


class QuestionOptions:
    "Options for Question object"

    def __init__(
        self,
        required: bool = False,
        answers_order: str = "none",
        inherit_answers: str | None = None,
        comment: bool = False,
        comment_text: str = "Other",
        comment_placeholder: str = "",
        visible: bool = True,
        other: bool = False,
        other_text: str = "Other",
        other_placeholder: str = "",
        none: bool = False,
        none_text: str = "None",
        clear_button: bool = False,
    ):
        self.required = required
        self.answers_order = answers_order
        self.inherit_answers = inherit_answers
        self.comment = comment
        self.comment_text = comment_text
        self.comment_placeholder = comment_placeholder
        self.visible = visible
        self.other = other
        self.other_text = other_text
        self.other_placeholder = other_placeholder
        self.none = none
        self.none_text = none_text
        self.clear_button = clear_button


class PageOptions:
    "Options for Page object"

    def __init__(
        self,
        read_only: bool = False,
        time_limit: int | None = None,
        visible: bool = True,
    ):
        self.read_only = read_only
        self.time_limit = time_limit
        self.visible = visible


class SurveyOptions:
    "Optrions for Survey object"

    def __init__(self, language: str = "en", url_on_complete: str | None = None):
        self.language = language
        self.url_on_complete = url_on_complete
