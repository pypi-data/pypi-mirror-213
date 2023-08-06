"Wrappers for different question types."

from .tools import question


def radio(label, question_text, *answers, description=None, options=None):
    return question(
        label,
        question_text,
        *answers,
        question_type="radio",
        description=description,
        options=options
    )


def checkbox(label, question_text, *answers, description=None, options=None):
    return question(
        label,
        question_text,
        *answers,
        question_type="checkbox",
        description=description,
        options=options
    )
