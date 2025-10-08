import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.repository import MySQLRepository

class Lecturer:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def all(cls):
        repo = MySQLRepository()
        rows = repo.select("SELECT * FROM lecturer;")
        repo.close()

        lecturers = [
            cls(
                id=row.get("id"),
                name=row.get("name")
            )
            for row in rows
        ]
        return lecturers

    def __repr__(self):
        return f"<Lecturer id={self.id} name={self.name}>"
