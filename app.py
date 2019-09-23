import pathlib
import flask


app = flask.Flask(__name__)


def get_project_list():
    return [
        {"project_no": "12345", "project_name": "project A"},
        {"project_no": "54321", "project_name": "project B"},
        {"project_no": "13579", "project_name": "project C"},
    ]


@app.route("/")
def index():
    return "This is the index"


@app.route("/projects")
def projects():
    project_list = get_project_list()
    return flask.render_template("projects/projects.html", projects=project_list)


if __name__ == "__main__":
    app.run(debug=True)
