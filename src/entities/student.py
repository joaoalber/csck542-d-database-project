import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.repository import MySQLRepository

class Student:
    def __init__(self, id=None, name=None, contact_info=None):
        self.id = id
        self.name = name
        self.contact_info = contact_info

    @classmethod
    def all(cls):
        repo = MySQLRepository()
        rows = repo.select("SELECT * FROM student;")
        repo.close()

        students = [
            cls(
                id=row.get("id"),
                name=row.get("name"),
                contact_info=row.get("contact_info")
            )
            for row in rows
        ]
        return students

    def __repr__(self):
        return f"<Student id={self.id} name={self.name} contact_info={self.contact_info}>"
