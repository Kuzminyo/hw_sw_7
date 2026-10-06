from pprint import pprint

from sqlalchemy import and_, desc, func, select

from src.db import Session
from src.models import Grade, Group, Student, Subject, Teacher


def select_1(session):
    """5 студентів із найбільшим середнім балом з усіх предметів."""
    return (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2(session, subject_id: int):
    """Студент із найвищим середнім балом з певного предмета."""
    return (
        session.query(
            Subject.name,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Subject.id == subject_id)
        .group_by(Student.id, Subject.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )


def select_3(session, subject_id: int):
    """Середній бал у групах з певного предмета."""
    return (
        session.query(
            Group.name,
            Subject.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(Subject.id == subject_id)
        .group_by(Group.id, Subject.name)
        .order_by(desc("avg_grade"))
        .all()
    )


def select_4(session):
    """Середній бал на потоці (по всій таблиці оцінок)."""
    return session.query(func.round(func.avg(Grade.grade), 2).label("avg_grade")).all()


def select_5(session, teacher_id: int):
    """Курси, які читає певний викладач."""
    return (
        session.query(Teacher.fullname, Subject.name)
        .select_from(Subject)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .order_by(Subject.name)
        .all()
    )


def select_6(session, group_id: int):
    """Список студентів у певній групі."""
    return (
        session.query(Group.name, Student.id, Student.fullname)
        .select_from(Student)
        .join(Group)
        .filter(Group.id == group_id)
        .order_by(Student.fullname)
        .all()
    )


def select_7(session, group_id: int, subject_id: int):
    """Оцінки студентів в окремій групі з певного предмета."""
    return (
        session.query(
            Group.name, Subject.name, Student.fullname, Grade.grade, Grade.grade_date
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(and_(Group.id == group_id, Subject.id == subject_id))
        .order_by(Student.fullname, Grade.grade_date)
        .all()
    )


def select_8(session, teacher_id: int):
    """Середній бал, який ставить певний викладач зі своїх предметів."""
    return (
        session.query(
            Teacher.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .group_by(Teacher.id)
        .all()
    )


def select_9(session, student_id: int):
    """Список курсів, які відвідує певний студент."""
    return (
        session.query(Student.fullname, Subject.name)
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Student.id == student_id)
        .distinct()
        .order_by(Subject.name)
        .all()
    )


def select_10(session, student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач."""
    return (
        session.query(Student.fullname, Teacher.fullname, Subject.name)
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Teacher)
        .filter(and_(Student.id == student_id, Teacher.id == teacher_id))
        .distinct()
        .order_by(Subject.name)
        .all()
    )


# ---------- Додаткове завдання ----------


def select_11(session, teacher_id: int, student_id: int):
    """Середній бал, який певний викладач ставить певному студентові."""
    return (
        session.query(
            Teacher.fullname,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Teacher)
        .filter(and_(Teacher.id == teacher_id, Student.id == student_id))
        .group_by(Teacher.id, Student.id)
        .all()
    )


def select_12(session, group_id: int, subject_id: int):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    # scalar-select: дата останнього заняття цієї групи з цього предмета
    last_date = (
        select(func.max(Grade.grade_date))
        .join(Student)
        .where(and_(Student.group_id == group_id, Grade.subject_id == subject_id))
        .scalar_subquery()
    )
    return (
        session.query(
            Group.name, Subject.name, Student.fullname, Grade.grade, Grade.grade_date
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(
            and_(
                Group.id == group_id,
                Subject.id == subject_id,
                Grade.grade_date == last_date,
            )
        )
        .order_by(Student.fullname)
        .all()
    )


if __name__ == "__main__":
    with Session() as session:
        queries = [
            ("select_1", select_1, ()),
            ("select_2 (subject_id=1)", select_2, (1,)),
            ("select_3 (subject_id=1)", select_3, (1,)),
            ("select_4", select_4, ()),
            ("select_5 (teacher_id=1)", select_5, (1,)),
            ("select_6 (group_id=1)", select_6, (1,)),
            ("select_7 (group_id=1, subject_id=1)", select_7, (1, 1)),
            ("select_8 (teacher_id=1)", select_8, (1,)),
            ("select_9 (student_id=1)", select_9, (1,)),
            ("select_10 (student_id=1, teacher_id=1)", select_10, (1, 1)),
            ("select_11 (teacher_id=1, student_id=1)", select_11, (1, 1)),
            ("select_12 (group_id=1, subject_id=1)", select_12, (1, 1)),
        ]
        for title, fn, args in queries:
            print(f"\n=== {title}: {fn.__doc__}")
            pprint(fn(session, *args))
