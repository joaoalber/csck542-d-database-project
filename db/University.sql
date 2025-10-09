CREATE USER IF NOT EXISTS 'dev_user'@'localhost' IDENTIFIED BY '123456';
ALTER USER 'dev_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
CREATE DATABASE IF NOT EXISTS University;
GRANT ALL PRIVILEGES ON University.* TO 'dev_user'@'localhost';
FLUSH PRIVILEGES;

USE University;

CREATE TABLE DEPARTMENT (
    dept_id INT PRIMARY KEY,
    name VARCHAR(100),
    faculty VARCHAR(100),
    research_areas TEXT
);

CREATE TABLE COMMITTEE (
    committee_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE PROGRAM (
    program_id INT PRIMARY KEY,
    name VARCHAR(100),
    degree_awarded VARCHAR(100),
    duration_years INT
);

CREATE TABLE STUDENT_ORG (
    org_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE LECTURER (
    lecturer_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    committee_id INT,
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id),
    FOREIGN KEY (committee_id) REFERENCES COMMITTEE(committee_id)
);

CREATE TABLE RESEARCH_GROUP (
    group_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    head_lecturer_id INT,
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id),
    FOREIGN KEY (head_lecturer_id) REFERENCES LECTURER(lecturer_id)
);

CREATE TABLE RESEARCH_PROJECT (
    project_id INT PRIMARY KEY,
    title VARCHAR(150),
    pi_lecturer_id INT,
    funding_sources VARCHAR(255),
    FOREIGN KEY (pi_lecturer_id) REFERENCES LECTURER(lecturer_id)
);

CREATE TABLE PUBLICATION (
    publication_id INT PRIMARY KEY,
    title VARCHAR(150),
    pub_date DATE,
    lecturer_id INT,
    project_id INT,
    FOREIGN KEY (lecturer_id) REFERENCES LECTURER(lecturer_id),
    FOREIGN KEY (project_id) REFERENCES RESEARCH_PROJECT(project_id)
);

CREATE TABLE NON_ACAD_STAFF (
    staff_id INT PRIMARY KEY,
    name VARCHAR(100),
    job_title VARCHAR(100),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id)
);

CREATE TABLE COURSE (
    course_code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    dept_id INT,
    level INT,
    credits INT,
    lecturer_id INT,
    status VARCHAR(50),
    schedule VARCHAR(100),
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id),
    FOREIGN KEY (lecturer_id) REFERENCES LECTURER(lecturer_id)
);

CREATE TABLE STUDENT (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    contact_info VARCHAR(150),
    program_id INT,
    year_of_study INT,
    graduation_status VARCHAR(50),
    advisor_id INT,
    org_id INT,
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id),
    FOREIGN KEY (advisor_id) REFERENCES LECTURER(lecturer_id),
    FOREIGN KEY (org_id) REFERENCES STUDENT_ORG(org_id)
);

CREATE TABLE ENROLLMENT (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    course_code VARCHAR(20),
    status VARCHAR(50),
    final_grade INT,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (course_code) REFERENCES COURSE(course_code)
);

CREATE TABLE GRADE_ITEM (
    grade_item_id INT PRIMARY KEY,
    course_code VARCHAR(20),
    name VARCHAR(100),
    weight DECIMAL(5,2),
    FOREIGN KEY (course_code) REFERENCES COURSE(course_code)
);

CREATE TABLE GRADE_RESULT (
    result_id INT PRIMARY KEY,
    grade_item_id INT,
    enrollment_id INT,
    score DECIMAL(5,2),
    FOREIGN KEY (grade_item_id) REFERENCES GRADE_ITEM(grade_item_id),
    FOREIGN KEY (enrollment_id) REFERENCES ENROLLMENT(enrollment_id)
);

CREATE TABLE DISCIPLINARY_RECORD (
    record_id INT PRIMARY KEY,
    student_id INT,
    incident_date DATE,
    description TEXT,
    outcome VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

CREATE TABLE EXPERTISE (
    expertise_id INT PRIMARY KEY,
    lecturer_id INT,
    area VARCHAR(100),
    FOREIGN KEY (lecturer_id) REFERENCES LECTURER(lecturer_id)
);

CREATE TABLE QUALIFICATION (
    qual_id INT PRIMARY KEY,
    lecturer_id INT,
    qualification VARCHAR(100),
    FOREIGN KEY (lecturer_id) REFERENCES LECTURER(lecturer_id)
);
