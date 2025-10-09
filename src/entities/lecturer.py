import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.repository import MySQLRepository

class Lecturer:
    def __init__(self, lecturer_id=None, name=None):
        self.lecturer_id = lecturer_id
        self.name = name

    @classmethod
    def all(cls):
        repo = MySQLRepository()
        rows = repo.select("SELECT * FROM lecturer;")
        repo.close()

        lecturers = [
            cls(
                lecturer_id=row.get("lecturer_id"),
                name=row.get("name")
            )
            for row in rows
        ]
        return lecturers
    
    @classmethod
    def with_no_courses_yet(cls):
        repo = MySQLRepository()
        query = """
            SELECT 
                l.lecturer_id AS lecturer_id,
                l.name AS lecturer_name
            FROM lecturer l
            WHERE NOT EXISTS (
                SELECT 1 FROM course c WHERE c.lecturer_id = l.lecturer_Id
            );
        """
        rows = repo.select(query)
        lecturers = []
        for row in rows:
            lecturers.append({
                "lecturer_id": row.get("lecturer_id"),
                "lecturer_name": row.get("lecturer_name"),
            })
        return lecturers

    @classmethod
    def with_advised_students(cls):
        repo = MySQLRepository()
        query = """
            SELECT 
                l.lecturer_id AS lecturer_id,
                l.name AS lecturer_name,
                s.student_id AS student_id,
                s.name AS student_name
            FROM lecturer l
            JOIN student s
                ON s.advisor_id = l.lecturer_id
        """
        rows = repo.select(query)

        lecturers = {}
        for row in rows:
            lid = row['lecturer_id']
            if lid not in lecturers:
                lecturers[lid] = {
                    "lecturer_id": lid,
                    "lecturer_name": row['lecturer_name'],
                    "students": []
                }
            lecturers[lid]["students"].append({
                "student_id": row['student_id'],
                "student_name": row['student_name']
            })

        lecturers_list = list(lecturers.values())
        return lecturers_list

    @classmethod
    def search(cls, term):
        repo = MySQLRepository()
        query = """
            SELECT *
            FROM lecturer
            WHERE LOWER(name) LIKE CONCAT('%%', LOWER(%s), '%%')
        """
        rows = repo.select(query, (term,))
        repo.close()

        lecturers = [
            cls(
                lecturer_id=row.get("lecturer_id"),
                name=row.get("name")
            )
            for row in rows
        ]
        return lecturers

    def __repr__(self):
        return f"<Lecturer lecturer_id={self.lecturer_id} name={self.name}>"
