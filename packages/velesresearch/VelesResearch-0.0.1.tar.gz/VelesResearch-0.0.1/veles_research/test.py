from json import dumps
from question_types import Question
from survey_tools import *
from structure import *
from options import Question_options

RSSI = """I feel that I am a person of worth, at least on an equal plane with others.
I feel that I have a number of good qualities.
All in all, I am inclined to feel that I am a failure.
I am able to do things as well as most other people.
I feel I do not have much to be proud of.
I take a positive attitude toward myself.
On the whole, I am satisfied with myself.
I wish I could have more respect for myself.
I certainly feel useless at times.
At times I think I am no good at all.""".split("\n")

scale = ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"]

opts = Question_options(required=True)

q = questionnaire("RSSI", RSSI, scale, options=opts)

q1 = Question("RSSI_1", "radio", RSSI[0], scale, options=opts)

p = Page("RSSI", q)

s = Survey(p, title="Rosenberg Self-Esteem Scale", description="This scale is a measure of self-esteem, that is, how positively or negatively people view themselves.")

s.create()