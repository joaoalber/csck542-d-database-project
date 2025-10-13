
import pymysql
from pymysql.err import IntegrityError, OperationalError

CONN = dict(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="university",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=False,  # so we can rollback after each test
)

def expect_integrity_error(sql, params=None, label=""):
    print(f"\n[TEST] {label}")
    conn = pymysql.connect(**CONN)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
        conn.commit()
        print("❌ FAILED (no error raised)")
    except IntegrityError as e:
        print("✅ PASSED (IntegrityError)")
        print("   →", e)
        conn.rollback()
    except OperationalError as e:
        # Some engines raise OperationalError on certain FK/PK violations
        print("✅ PASSED (OperationalError acceptable here)")
        print("   →", e)
        conn.rollback()
    finally:
        conn.close()

def main():
    expect_integrity_error(
        "INSERT INTO student (student_id, name) VALUES (1, 'Duplicate Name');",
        label="Duplicate PK in STUDENT (student_id=1 already exists)"
    )

    expect_integrity_error(
        "INSERT INTO enrollment (enrollment_id, student_id, course_code, status) "
        "VALUES (999, 9999, 'CS101', 'Enrolled');",
        label="FK violation: ENROLLMENT.student_id → STUDENT(student_id)"
    )

    expect_integrity_error(
        "INSERT INTO enrollment (enrollment_id, student_id, course_code, status) "
        "VALUES (1000, 1, 'NOCOURSE', 'Enrolled');",
        label="FK violation: ENROLLMENT.course_code → COURSE(course_code)"
    )

    expect_integrity_error(
        "INSERT INTO grade_result (result_id, grade_item_id, enrollment_id, score) "
        "VALUES (5000, 1, 424242, 70.0);",
        label="FK violation: GRADE_RESULT.enrollment_id → ENROLLMENT(enrollment_id)"
    )

    expect_integrity_error(
        "INSERT INTO course (course_code, name, dept_id, level, credits, lecturer_id, status, schedule) "
        "VALUES (NULL, 'Bad Course', 1, 1, 3, 1, 'Active', 'Wed 10:00');",
        label="NOT NULL/PK violation: COURSE.course_code cannot be NULL"
    )

if __name__ == "__main__":
    main()
