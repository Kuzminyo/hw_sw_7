# hw_sw_7 — SQLAlchemy + Alembic + PostgreSQL

Students / groups / teachers / subjects / grades database built with SQLAlchemy ORM,
Alembic migrations, Faker seeding, ORM queries and an argparse CRUD CLI.

## Structure

| File | Purpose |
|---|---|
| `src/models.py` | SQLAlchemy models: `Group`, `Student`, `Teacher`, `Subject`, `Grade` |
| `src/db.py` | Engine and `Session` (URL from `DATABASE_URL` env var) |
| `migrations/` | Alembic migrations |
| `seed.py` | Fills the DB with random data (Faker, SQLAlchemy sessions) |
| `my_select.py` | Queries `select_1` … `select_10` + extra `select_11`, `select_12` |
| `main.py` | CLI for CRUD operations on every model |

## Setup

```bash
docker run --name hw7-postgres -p 5432:5432 -e POSTGRES_PASSWORD=hw7secret -e POSTGRES_DB=hw7 -d postgres
pip install -r requirements.txt
alembic upgrade head
python seed.py
python my_select.py
```

Default connection: `postgresql+psycopg2://postgres:hw7secret@localhost:5432/hw7`.
Override with the `DATABASE_URL` environment variable (e.g. `sqlite:///hw7.db`).

## Queries (`my_select.py`)

1. Top 5 students by average grade across all subjects
2. Student with the highest average grade in a subject
3. Average grade per group in a subject
4. Average grade over the whole grades table
5. Courses taught by a teacher
6. Students in a group
7. Grades of a group's students in a subject
8. Average grade a teacher gives across their subjects
9. Courses a student attends
10. Courses a teacher teaches to a student
11. *(extra)* Average grade a teacher gives to a student
12. *(extra)* Grades of a group in a subject at the last lesson (scalar subquery)

## CLI (`main.py`)

`-a/--action`: `create`, `list`, `update`, `remove`; `-m/--model`: `Group`, `Teacher`, `Student`, `Subject`, `Grade`.

```bash
py main.py -a create -m Teacher -n 'Boris Jonson'
py main.py -a list -m Teacher
py main.py -a update -m Teacher --id 3 -n 'Andry Bezos'
py main.py -a remove -m Teacher --id 3
py main.py -a create -m Group -n 'AD-101'
py main.py -a create -m Student -n 'John Doe' --group_id 1
py main.py -a create -m Subject -n 'Art' --teacher_id 1
py main.py -a create -m Grade -g 10 --student_id 1 --subject_id 1 -d 2026-05-20
```

Other options: `--group_id`, `--teacher_id`, `--student_id`, `--subject_id`, `-g/--grade`, `-d/--date` (YYYY-MM-DD, defaults to today for grades).
