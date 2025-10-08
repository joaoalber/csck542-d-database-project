import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.repository import MySQLRepository

class Course:
    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def all(cls):
        repo = MySQLRepository()
        rows = repo.select("SELECT * FROM course;")

        courses = []
        for row in rows:
            course = cls(
                id=row.get("id"),
                name=row.get("name"),
                description=row.get("description")
            )
            courses.append(course)
        return courses

    def __repr__(self):
        return f"<Course id={self.id} name={self.name}>"
