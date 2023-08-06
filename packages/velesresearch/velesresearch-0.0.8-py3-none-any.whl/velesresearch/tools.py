"Functions and wrappers for creating survey structure"
from collections.abc import Sequence
from pydantic import validate_arguments
import numpy as np
from .structure import Question, Page, Survey
from .options import QuestionOptions, PageOptions, SurveyOptions


@validate_arguments
def question(
    label: str,
    question_text: str | Sequence[str],
    *answers: str | Sequence[str],
    question_type: str = "radio",
    description: str | None = None,
    options: QuestionOptions | None = None,
) -> Question:
    "Wrapper around Question class"
    answers_list = list(np.concatenate([answers]).flat)
    if isinstance(question_text, str):
        return Question(
            label=label,
            question_text=question_text,
            answers=answers_list,
            question_type=question_type,
            description=description,
            options=options,
        )
    else:
        question_list = list(np.concatenate([question_text]).flat)
        q_list = []
        for i in enumerate(question_list):
            q_list.append(
                Question(
                    label=f"{label}_{i[0] + 1}",
                    question_text=i[1],
                    answers=answers_list,
                    question_type=question_type,
                    description=description,
                    options=options,
                )
            )
        return q_list


def page(
    label: str,
    *questions: Question | Sequence[Question],
    title: str | None = None,
    description: str | None = None,
    options: PageOptions | None = None,
) -> Page:
    "Wrapper around Page class"
    questions_list = list(np.concatenate([questions]).flat)
    return Page(
        label=label,
        questions=questions_list,
        title=title,
        description=description,
        options=options,
    )


def survey(
    *pages: Page | Sequence[Page],
    title: str | None = None,
    description: str | None = None,
    options: SurveyOptions | None = None,
    create_file: bool = True,
) -> Survey:
    "Create Survey object from pages, create json file"
    pages_list = list(np.concatenate([pages]).flat)
    survey_obj = Survey(
        pages=pages_list, title=title, description=description, options=options
    )
    if create_file:
        survey_obj.create()
    return survey_obj
