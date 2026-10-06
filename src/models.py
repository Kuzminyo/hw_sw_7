from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"Group(id={self.id}, name={self.name!r})"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150))
    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("groups.id", ondelete="SET NULL")
    )

    group: Mapped["Group | None"] = relationship(back_populates="students")
    grades: Mapped[list["Grade"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.fullname!r}, group_id={self.group_id})"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150))

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")

    def __repr__(self):
        return f"Teacher(id={self.id}, fullname={self.fullname!r})"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(175))
    teacher_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL")
    )

    teacher: Mapped["Teacher | None"] = relationship(back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Subject(id={self.id}, name={self.name!r}, teacher_id={self.teacher_id})"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(Integer)
    grade_date: Mapped[date] = mapped_column(Date)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE")
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE")
    )

    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")

    def __repr__(self):
        return (
            f"Grade(id={self.id}, grade={self.grade}, grade_date={self.grade_date}, "
            f"student_id={self.student_id}, subject_id={self.subject_id})"
        )
