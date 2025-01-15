import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta


conn = sqlite3.connect("university.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    grade INTEGER,
    date TEXT,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
);
""")


fake = Faker()


group_names = ["Group A", "Group B", "Group C"]
for name in group_names:
    cursor.execute("INSERT INTO groups (name) VALUES (?);", (name,))

group_ids = [row[0] for row in cursor.execute("SELECT id FROM groups;").fetchall()]


students = []
for _ in range(50):
    name = fake.name()
    group_id = random.choice(group_ids)
    students.append((name, group_id))
cursor.executemany("INSERT INTO students (name, group_id) VALUES (?, ?);", students)


teachers = []
for _ in range(5):
    name = fake.name()
    teachers.append((name,))
cursor.executemany("INSERT INTO teachers (name) VALUES (?);", teachers)

teacher_ids = [row[0] for row in cursor.execute("SELECT id FROM teachers;").fetchall()]


subject_names = ["Math", "Physics", "Chemistry", "Biology", "History", "Literature", "Computer Science", "Art"]
subjects = []
for name in subject_names:
    teacher_id = random.choice(teacher_ids)
    subjects.append((name, teacher_id))
cursor.executemany("INSERT INTO subjects (name, teacher_id) VALUES (?, ?);", subjects)

subject_ids = [row[0] for row in cursor.execute("SELECT id FROM subjects;").fetchall()]


grades = []
for student_id in range(1, 51):
    for subject_id in subject_ids:
        for _ in range(random.randint(10, 20)):
            grade = random.randint(60, 100)
            date = fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
            grades.append((student_id, subject_id, grade, date))
cursor.executemany("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?);", grades)


conn.commit()
conn.close()

print("Database and data successfully created!")
