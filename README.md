# hw_sw_7 — SQLAlchemy + Alembic + PostgreSQL

База даних студентів, груп, викладачів, предметів і оцінок на SQLAlchemy ORM:
міграції Alembic, наповнення через Faker, ORM-запити та CLI для CRUD-операцій на argparse.

## Структура

| Файл | Призначення |
|---|---|
| `src/models.py` | Моделі SQLAlchemy: `Group`, `Student`, `Teacher`, `Subject`, `Grade` |
| `src/db.py` | Engine і `Session` (URL зі змінної оточення `DATABASE_URL`) |
| `migrations/` | Міграції Alembic |
| `seed.py` | Наповнення бази випадковими даними (Faker, сесії SQLAlchemy) |
| `my_select.py` | Запити `select_1` … `select_10` + додаткові `select_11`, `select_12` |
| `main.py` | CLI для CRUD-операцій з усіма моделями |

## Запуск

```bash
docker run --name hw7-postgres -p 5432:5432 -e POSTGRES_PASSWORD=hw7secret -e POSTGRES_DB=hw7 -d postgres
pip install -r requirements.txt
alembic upgrade head
python seed.py
python my_select.py
```

Підключення за замовчуванням: `postgresql+psycopg2://postgres:hw7secret@localhost:5432/hw7`.
Його можна змінити змінною оточення `DATABASE_URL` (наприклад, `sqlite:///hw7.db`).

## Запити (`my_select.py`)

1. 5 студентів із найбільшим середнім балом з усіх предметів
2. Студент із найвищим середнім балом з певного предмета
3. Середній бал у групах з певного предмета
4. Середній бал на потоці (по всій таблиці оцінок)
5. Курси, які читає певний викладач
6. Список студентів у певній групі
7. Оцінки студентів в окремій групі з певного предмета
8. Середній бал, який ставить певний викладач зі своїх предметів
9. Список курсів, які відвідує певний студент
10. Список курсів, які певному студенту читає певний викладач
11. *(додатково)* Середній бал, який певний викладач ставить певному студентові
12. *(додатково)* Оцінки студентів у певній групі з певного предмета на останньому занятті (scalar-select)

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

Інші параметри: `--group_id`, `--teacher_id`, `--student_id`, `--subject_id`, `-g/--grade`, `-d/--date` (формат YYYY-MM-DD; для оцінки за замовчуванням — сьогоднішня дата).
