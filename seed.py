import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy import text

from src.db import Session
from src.models import Grade, Group, Student, Subject, Teacher

NUMBER_STUDENTS = 45
NUMBER_TEACHERS = 4
GROUP_NAMES = ["AD-101", "AD-102", "AD-103"]
SUBJECT_NAMES = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "History",
    "Programming",
    "Databases",
    "English",
]
MAX_GRADES_PER_STUDENT = 20
START_DATE = date(2025, 9, 1)
END_DATE = date(2026, 5, 31)

fake = Faker()


def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


def clear_tables(session):
    """Очищає таблиці (і скидає id), щоб скрипт можна було запускати повторно."""
    if session.bind.dialect.name == "postgresql":
        session.execute(
            text("TRUNCATE grades, subjects, students, teachers, groups RESTART IDENTITY")
        )
    else:
        for model in (Grade, Subject, Student, Teacher, Group):
            session.query(model).delete()


def seed():
    with Session() as session:
        clear_tables(session)

        groups = [Group(name=name) for name in GROUP_NAMES]
        teachers = [Teacher(fullname=fake.name()) for _ in range(NUMBER_TEACHERS)]
        # кожен викладач читає щонайменше один предмет
        subject_teachers = teachers + [
            random.choice(teachers) for _ in range(len(SUBJECT_NAMES) - len(teachers))
        ]
        random.shuffle(subject_teachers)
        subjects = [
            Subject(name=name, teacher=teacher)
            for name, teacher in zip(SUBJECT_NAMES, subject_teachers)
        ]
        students = [
            Student(fullname=fake.name(), group=random.choice(groups))
            for _ in range(NUMBER_STUDENTS)
        ]
        session.add_all(groups + teachers + subjects + students)

        grades = [
            Grade(
                student=student,
                subject=random.choice(subjects),
                grade=random.randint(1, 12),
                grade_date=random_date(START_DATE, END_DATE),
            )
            for student in students
            for _ in range(random.randint(10, MAX_GRADES_PER_STUDENT))
        ]
        session.add_all(grades)
        session.commit()

        print(
            f"Seeded: {len(groups)} groups, {len(teachers)} teachers, "
            f"{len(subjects)} subjects, {len(students)} students, {len(grades)} grades"
        )


if __name__ == "__main__":
    seed()
