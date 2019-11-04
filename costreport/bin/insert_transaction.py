import os
import sys

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import costreport.data.db_session as db_session
from costreport.data.transactions import Transaction


def main():
    init_db()
    while True:
        insert_a_transaction()


def insert_a_transaction():
    t = Transaction()
    t.project_id = input("Project id:").strip().lower()
    if len(t.project_id) < 1:
        raise ValueError("Value cannot be NULL")
    t.costcode_id = input("Costcode:").strip()
    if len(t.costcode_id) < 1:
        raise ValueError("Value cannot be NULL")
    t.value = input("Value").strip()
    if len(t.value) < 1:
        raise ValueError("Value cannot be NULL")
    t.note = input("Note").strip()

    session = db_session.create_session()
    session.add(t)
    session.commit()


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join("..", "db", "costreport.sqlite")
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == "__main__":
    main()
