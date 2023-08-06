"Functions for generating survey package."
from __future__ import annotations
from os import getcwd, mkdir
from importlib.metadata import version
from json import dump
from pathlib import Path
from pynpm import NPMPackage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .structure import Survey


def install_npm_deps(path: str | Path = getcwd()) -> None:
    """Install npm dependencies for VelesResearch."""

    npm_dependencies = {
        "name": "Veles Survey",
        "version": version("velesresearch"),
        "private": True,
        "dependencies": {
            "json-loader": "latest",
            "react": "latest",
            "react-dom": "latest",
            "survey-react-ui": "latest",
        },
        "devDependencies": {"react-scripts": "latest"},
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
        },
        "eslintConfig": {"extends": ["react-app", "react-app/jest"]},
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version",
            ],
        },
    }

    if isinstance(path, str):
        path = Path(path)
    path = path / "package.json"
    package_json = open(path, "w", encoding="utf-8")
    dump(npm_dependencies, package_json)
    package_json.close()
    NPMPackage(path).install()


def generate_survey(Survey_object: "Survey", path: str | Path = getcwd()) -> None:
    "Saves survey to survey.js file"

    index_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{Survey_object.label}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="surveyElement"></div>
  </body>
</html>"""

    index_js = """import React from "react";
import { createRoot } from "react-dom/client";
import SurveyComponent from "./SurveyComponent";

const root = createRoot(document.getElementById("surveyElement"));
root.render(<SurveyComponent />);"""

    index_css = ""

    SurveyComponent = """import React from "react";
import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/defaultV2.min.css";
import "./index.css";
import { json } from "./survey.js";

function SurveyComponent() {
    const survey = new Model(json);
    survey.onComplete.add((sender, options) => {
        console.log(JSON.stringify(sender.data, null, 3));
    });
    return (<Survey model={survey} />);
}

export default SurveyComponent;"""

    if isinstance(path, str):
        path = Path(path)

    # package.json
    mkdir(path / "src")
    mkdir(path / "public")

    # survey.js
    survey_js = open(path / "src" / "survey.js", "w", encoding="utf-8")
    survey_js.write("export const json = ")
    survey_js.close()
    survey_js = open(path / "src" / "survey.js", "a", encoding="utf-8")
    from .structure import SurveyEncoder

    dump(Survey_object, survey_js, cls=SurveyEncoder)
    survey_js.close()

    # index.js
    index_js_file = open(path / "src" / "index.js", "w", encoding="utf-8")
    index_js_file.write(index_js)
    index_js_file.close()

    # index.css
    index_css_file = open(path / "src" / "index.css", "w", encoding="utf-8")
    index_css_file.write(index_css)
    index_css_file.close()

    # SurveyComponent.jsx
    survey_component_file = open(
        path / "src" / "SurveyComponent.jsx", "w", encoding="utf-8"
    )
    survey_component_file.write(SurveyComponent)
    survey_component_file.close()

    # index.html
    index_html_file = open(path / "public" / "index.html", "w", encoding="utf-8")
    index_html_file.write(index_html)
    index_html_file.close()


def build_survey(path: str | Path = getcwd()) -> None:
    """Builds survey package."""

    if isinstance(path, str):
        path = Path(path)

    NPMPackage(path).run_script("build")
