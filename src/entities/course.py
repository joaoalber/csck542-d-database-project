import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.repository import MySQLRepository

class Course:
    def __init__(self, course_code=None, name=None, status=None):
        self.course_code = course_code
        self.name = name
        self.status = status

    @classmethod
    def all(cls):
        repo = MySQLRepository()
        rows = repo.select("SELECT * FROM course;")

        courses = []
        for row in rows:
            course = cls(
                course_code=row.get("course_code"),
                name=row.get("name"),
                status=row.get("status")
            )
            courses.append(course)
        return courses

    @classmethod
    def search(cls, term):
        repo = MySQLRepository()
        query = """
            SELECT *
            FROM course
            WHERE LOWER(name) LIKE CONCAT('%%', LOWER(%s), '%%')
        """
        rows = repo.select(query, (term,))
        repo.close()

        courses = [
            cls(
                course_code=row.get("course_code"),
                name=row.get("name"),
                status=row.get("status")
            )
            for row in rows
        ]
        return courses

    @classmethod
    def with_no_students_yet(cls):
        repo = MySQLRepository()
        query = """
            SELECT 
                c.course_code AS course_code,
                c.name AS course_name,
                c.status AS course_status
            FROM course c
            WHERE NOT EXISTS (
                SELECT 1 FROM enrollment e WHERE e.course_code = c.course_code
            );
        """
        rows = repo.select(query)
        courses = []
        for row in rows:
            courses.append({
                "course_code": row.get("course_code"),
                "name": row.get("course_name"),
                "status": row.get("course_status")
            })
        return courses

    @classmethod
    def lecturer_expertises(cls):
        repo = MySQLRepository()
        
        query = """
            SELECT 
                c.course_code AS course_code,
                c.name AS course_name,
                l.name AS lecturer_name,
                GROUP_CONCAT(e.area) AS lecturer_areas
            FROM course c
            JOIN lecturer l ON c.lecturer_id = l.lecturer_id
            JOIN expertise e ON l.lecturer_id = e.lecturer_id
            WHERE e.area IS NOT NULL
            GROUP BY c.course_code, c.name, l.name;
        """
        
        rows = repo.select(query)
        
        courses = []
        for row in rows:
            courses.append({
                "course_code": row.get("course_code"),
                "course_name": row.get("course_name"),
                "lecturer_name": row.get("lecturer_name"),
                "lecturer_areas": row.get("lecturer_areas").split(',') if row.get("lecturer_areas") else []
            })
        
        return courses


    def __repr__(self):
        return f"<Course id={self.course_code} name={self.name} status={self.status}>"
