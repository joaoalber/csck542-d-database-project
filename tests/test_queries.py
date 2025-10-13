
import pymysql
from pprint import pprint

CONN = dict(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="university",
    cursorclass=pymysql.cursors.DictCursor,
)

def run(sql, params=None):
    with pymysql.connect(**CONN) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

def show(title, rows):
    print(f"\n=== {title} ===")
    pprint(rows)

def assert_rows_as_set(rows, key_tuple, expected):
    got = {tuple(r[k] for k in key_tuple) for r in rows}
    exp = set(expected)
    assert got == exp, f"\nExpected: {sorted(exp)}\nGot     : {sorted(got)}"

def main():
    db = run("SELECT DATABASE() AS db;")[0]["db"]
    print("Connected to DB:", db)

    sql1 = """
    SELECT s.student_id, s.name
    FROM course c
    JOIN lecturer l ON l.lecturer_id = c.lecturer_id
    JOIN enrollment e ON e.course_code = c.course_code
    JOIN student s ON s.student_id = e.student_id
    WHERE c.course_code = %s AND l.name = %s
    ORDER BY s.student_id;
    """
    rows1 = run(sql1, ("CS205", "Dr. Omar"))
    show("Q1: students in CS205 taught by Dr. Omar", rows1)
    assert_rows_as_set(
        rows1, ("student_id", "name"),
        {(1, "Alya AlKetbi"), (2, "Mizna AlMansoori"), (3, "Hamad AlMarri")}
    )

    sql2 = """
    SELECT s.student_id, s.name, ROUND(AVG(gr.score),2) AS avg_score
    FROM student s
    JOIN enrollment e ON e.student_id = s.student_id
    JOIN grade_result gr ON gr.enrollment_id = e.enrollment_id
    WHERE s.year_of_study = 4
    GROUP BY s.student_id, s.name
    HAVING AVG(gr.score) > 70
    ORDER BY s.student_id;
    """
    rows2 = run(sql2)
    show("Q2: final-year avg > 70%", rows2)
    
    assert_rows_as_set(rows2, ("student_id", "name"),
                       {(2, "Mizna AlMansoori"), (3, "Hamad AlMarri")})

    sql3 = """
    SELECT s.student_id, s.name
    FROM student s
    LEFT JOIN enrollment e ON e.student_id = s.student_id
    WHERE e.enrollment_id IS NULL
    ORDER BY s.student_id;
    """
    rows3 = run(sql3)
    show("Q3: students with no enrollments", rows3)
    assert_rows_as_set(rows3, ("student_id", "name"),
                       {(4, "João Rossi"), (5, "Alyan Tremb")})

    sql4 = """
    SELECT s.name AS student, l.name AS advisor
    FROM student s
    JOIN lecturer l ON l.lecturer_id = s.advisor_id
    WHERE s.name = %s;
    """
    rows4 = run(sql4, ("Alya AlKetbi",))
    show("Q4: advisor for Alya", rows4)
    assert_rows_as_set(rows4, ("student", "advisor"),
                       {("Alya AlKetbi", "Dr. Aisha")})

    sql5 = """
    SELECT DISTINCT l.lecturer_id, l.name
    FROM lecturer l
    JOIN expertise x ON x.lecturer_id = l.lecturer_id
    WHERE x.area = %s
    ORDER BY l.lecturer_id;
    """
    rows5 = run(sql5, ("ML",))
    show("Q5: lecturers with 'ML' expertise", rows5)
    assert_rows_as_set(rows5, ("lecturer_id", "name"), {(1, "Dr. Aisha")})

    sql6 = """
    SELECT c.course_code, c.name
    FROM course c
    JOIN lecturer l ON l.lecturer_id = c.lecturer_id
    JOIN department d ON d.dept_id = c.dept_id
    WHERE d.name = %s
    ORDER BY c.course_code;
    """
    rows6 = run(sql6, ("Computer Science",))
    show("Q6: courses taught by CS dept lecturers", rows6)
    assert_rows_as_set(rows6, ("course_code", "name"),
                       {("CS101","Intro to Programming"),
                        ("CS205","Databases"),
                        ("CS302","Programming Logic")})

    sql7 = """
    WITH counts AS (
      SELECT pi_lecturer_id AS lecturer_id, COUNT(*) AS n
      FROM research_project
      GROUP BY pi_lecturer_id
    ),
    maxn AS (SELECT MAX(n) AS max_n FROM counts)
    SELECT l.lecturer_id, l.name, c.n
    FROM counts c
    JOIN maxn m ON c.n = m.max_n
    JOIN lecturer l ON l.lecturer_id = c.lecturer_id
    ORDER BY l.lecturer_id;
    """
    rows7 = run(sql7)
    show("Q7: lecturers with most supervised projects", rows7)
    assert_rows_as_set(rows7, ("lecturer_id", "name", "n"),
                       {(1, "Dr. Aisha", 1), (2, "Dr. Omar", 1)})

    print("\n✅ All query tests passed.")

if __name__ == "__main__":
    main()
