# TABLES
INSERT INTO DEPARTMENT (dept_id, name, faculty, research_areas) VALUES
(1,'Computer Science','Engineering & IT','Databases; ML; Systems'),
(2,'Information Systems','Engineering & IT','HCI; Integration'),
(3,'Mathematics','Science','Algebra; Discrete');

INSERT INTO COMMITTEE (committee_id, name) VALUES
(1,'Ethics Board'), (2,'Hiring'), (3,'Curriculum');

INSERT INTO PROGRAM (program_id, name, degree_awarded, duration_years) VALUES
(1,'BSc Computer Science','BSc',4),
(2,'BSc Information Systems','BSc',4),
(3,'MSc Data Science','MSc',2);

INSERT INTO STUDENT_ORG (org_id, name) VALUES
(1,'AI Club'), (2,'CyberSec Society'), (3,'Data Science Guild');

# LECTURERS & RELATED 
INSERT INTO LECTURER (lecturer_id, name, dept_id, committee_id) VALUES
(1,'Dr. Aisha',1,1),
(2,'Dr. Omar',1,2),
(3,'Dr. Lina',2,3);

INSERT INTO RESEARCH_GROUP (group_id, name, dept_id, head_lecturer_id) VALUES
(1,'RG-ML',1,1);

INSERT INTO RESEARCH_PROJECT (project_id, title, pi_lecturer_id, funding_sources) VALUES
(1,'Project-101',1,'Gov Grant'),
(2,'Project-202',2,'Industry');


# COURSES 
INSERT INTO COURSE (course_code, name, description, dept_id, level, credits, lecturer_id, status, schedule) VALUES
('CS101','Intro to Programming','Basics of Python',1,1,3,1,'Active','Sun 10:00'),
('CS205','Databases','Relational design',1,2,3,2,'Active','Mon 12:00'),
('IS210','Systems Analysis','Methods & tools',2,2,3,3,'Active','Tue 14:00'),
('CS302','Programming Logic','Basics of logic',1,2,3,1,'Active','Mon 13:00');

# STUDENTS 
INSERT INTO STUDENT (student_id, name, dob, contact_info, program_id, year_of_study,
                     graduation_status, advisor_id, org_id) VALUES
(1,'Alya AlKetbi','2001-05-10','alya@example.edu',3,2,'In Progress',1,1),
(2,'Mizna AlMansoori','2000-02-20','mizna@example.edu',1,4,'Eligible',2,2),
(3,'Hamad AlMarri','2002-09-01','hamad@example.edu',1,4,'In Progress',1,1),
(4,'João Rossi','2001-02-01','joao@example.edu',NULL,NULL,NULL,NULL,NULL),
(5,'Alyan Tremb','2000-03-01','alyan@example.edu',NULL,NULL,NULL,NULL,NULL);

# ENROLLMENTS 
INSERT INTO ENROLLMENT (enrollment_id, student_id, course_code, status, final_grade) VALUES
(1,1,'CS101','Enrolled',NULL),
(2,1,'CS205','Enrolled',NULL),
(3,2,'CS205','Completed',75),
(4,2,'IS210','Completed',65),
(5,3,'CS205','Enrolled',NULL);

# ASSESSMENT STRUCTURE
INSERT INTO GRADE_ITEM (grade_item_id, course_code, name, weight) VALUES
(1,'CS101','Quiz',20.00),(2,'CS101','Midterm',30.00),(3,'CS101','Final',50.00),
(4,'CS205','Quiz',20.00),(5,'CS205','Midterm',30.00),(6,'CS205','Final',50.00),
(7,'IS210','Quiz',20.00),(8,'IS210','Midterm',30.00),(9,'IS210','Final',50.00);


INSERT INTO GRADE_RESULT (result_id, grade_item_id, enrollment_id, score) VALUES
(1,1,1,85.0),(2,2,1,78.0),(3,3,1,90.0),   -- Student 1 in CS101
(4,4,2,82.0),(5,5,2,75.0),(6,6,2,88.0),   -- Student 1 in CS205
(7,4,3,70.0),(8,5,3,72.0),(9,6,3,80.0),   -- Student 2 in CS205 (Completed)
(10,7,4,88.0),(11,8,4,92.0),(12,9,4,94.0),-- Student 2 in IS210 (Completed)
(13,4,5,77.0),(14,5,5,68.0),(15,6,5,79.0);-- Student 3 in CS205

# OPTIONAL EXTRA TABLES 
INSERT INTO NON_ACAD_STAFF (staff_id, name, job_title, dept_id) VALUES
(1,'Fatima Ali','HR Officer',2),
(2,'Khalid Yousef','Librarian',3);

INSERT INTO DISCIPLINARY_RECORD (record_id, student_id, incident_date, description, outcome) VALUES
(1,1,'2024-03-12','Library Fine','Paid');

INSERT INTO EXPERTISE (expertise_id, lecturer_id, area) VALUES
(1,1,'Databases'),(2,1,'ML'),(3,2,'Databases'),(4,3,'HCI');

INSERT INTO QUALIFICATION (qual_id, lecturer_id, qualification) VALUES
(1,1,'PhD in CS'),(2,2,'PhD in IS'),(3,3,'MSc in HCI');
