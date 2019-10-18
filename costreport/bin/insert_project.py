import os
import sys

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from costreport.app import db
from costreport.data.projects import Project


def main():
    while True:
        insert_a_project()


def insert_a_project():
    p = Project()
    p.project_code = input("Project code:").strip().lower()
    if len(p.project_code) < 1:
        raise ValueError("Value must not be NULL")
    p.project_name = input("Project name:").strip()
    if len(p.project_name) < 1:
        raise ValueError("Value must not be NULL")

    db.session.add(p)
    db.session.commit()


if __name__ == "__main__":
    main()
