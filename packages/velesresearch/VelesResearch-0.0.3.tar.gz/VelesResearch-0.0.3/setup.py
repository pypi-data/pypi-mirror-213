from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "Surveys and experiments tool"
LONG_DESCRIPTION = "Free and open source surveys and experiments tool for social sciences"

setup(
    name="VelesResearch",
    version = VERSION,
    author = "Jakub Jędrusiak",
    author_email = "<kuba23031999@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    keywords = ['python', 'surveys', 'experiments', 'social sciences'],
    requires=["json", "numpy", "typeguard", "typing"]
)
