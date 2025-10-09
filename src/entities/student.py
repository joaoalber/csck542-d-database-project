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

    @classmethod
    def search(cls, term):
        repo = MySQLRepository()
        query = """
            SELECT *
            FROM student
            WHERE LOWER(name) LIKE CONCAT('%%', LOWER(%s), '%%')
        """
        rows = repo.select(query, (term,))
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

    @classmethod
    def top_completed_students(cls):
        repo = MySQLRepository()
        query = """
            SELECT 
                s.student_id AS student_id,
                s.name AS student_name,
                e.final_grade AS final_grade
            FROM student s
            JOIN enrollment e ON e.student_id = s.student_id
            WHERE e.status = 'Completed'
            AND e.final_grade >= 70;
        """
        rows = repo.select(query)
        students = []
        for row in rows:
            students.append({
                "id": row.get("student_id"),
                "name": row.get("student_name"),
                "final_grade": row.get("final_grade")
            })
        return students

    @classmethod
    def not_enrolled_yet(cls):
        repo = MySQLRepository()
        query = """
            SELECT 
                s.student_id AS student_id,
                s.name AS student_name
            FROM student s
            LEFT JOIN enrollment e ON e.student_id = s.student_id
            WHERE e.student_id IS NULL;
        """
        rows = repo.select(query)
        students = []
        for row in rows:
            students.append({
                "name": row.get("student_name"),
            })
        return students

    def __repr__(self):
        return f"<Student id={self.id} name={self.name} contact_info={self.contact_info}>"
