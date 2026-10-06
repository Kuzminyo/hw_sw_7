import argparse
from datetime import date

from sqlalchemy.exc import IntegrityError

from src.db import Session
from src.models import Grade, Group, Student, Subject, Teacher

# назва моделі -> (клас, {аргумент CLI -> атрибут моделі})
MODELS = {
    "Group": (Group, {"name": "name"}),
    "Teacher": (Teacher, {"name": "fullname"}),
    "Student": (Student, {"name": "fullname", "group_id": "group_id"}),
    "Subject": (Subject, {"name": "name", "teacher_id": "teacher_id"}),
    "Grade": (
        Grade,
        {
            "grade": "grade",
            "date": "grade_date",
            "student_id": "student_id",
            "subject_id": "subject_id",
        },
    ),
}

REQUIRED_ON_CREATE = {
    "Group": ["name"],
    "Teacher": ["name"],
    "Student": ["name"],
    "Subject": ["name"],
    "Grade": ["grade", "student_id", "subject_id"],
}


def parse_args():
    parser = argparse.ArgumentParser(description="CLI для CRUD-операцій з базою даних університету")
    parser.add_argument(
        "-a", "--action", required=True, choices=["create", "list", "update", "remove"]
    )
    parser.add_argument("-m", "--model", required=True, choices=list(MODELS))
    parser.add_argument("--id", type=int, help="id запису (для update/remove)")
    parser.add_argument("-n", "--name", help="назва / повне ім'я")
    parser.add_argument("--group_id", type=int)
    parser.add_argument("--teacher_id", type=int)
    parser.add_argument("--student_id", type=int)
    parser.add_argument("--subject_id", type=int)
    parser.add_argument("-g", "--grade", type=int)
    parser.add_argument(
        "-d", "--date", type=date.fromisoformat, help="дата оцінки, YYYY-MM-DD"
    )
    return parser.parse_args()


def collect_fields(args, model_name):
    """Повертає {атрибут моделі: значення} для переданих аргументів."""
    _, mapping = MODELS[model_name]
    return {
        attr: getattr(args, arg)
        for arg, attr in mapping.items()
        if getattr(args, arg) is not None
    }


def create(session, args):
    model, _ = MODELS[args.model]
    missing = [f for f in REQUIRED_ON_CREATE[args.model] if getattr(args, f) is None]
    if missing:
        return f"Missing required arguments for {args.model}: {', '.join(missing)}"
    fields = collect_fields(args, args.model)
    if args.model == "Grade":
        fields.setdefault("grade_date", date.today())
    obj = model(**fields)
    session.add(obj)
    session.commit()
    return f"Created: {obj}"


def list_all(session, args):
    model, _ = MODELS[args.model]
    rows = session.query(model).order_by(model.id).all()
    return "\n".join(map(repr, rows)) or f"No {args.model} records"


def get_or_none(session, args):
    model, _ = MODELS[args.model]
    if args.id is None:
        return None, "--id is required"
    obj = session.get(model, args.id)
    if obj is None:
        return None, f"{args.model} with id={args.id} not found"
    return obj, None


def update(session, args):
    obj, error = get_or_none(session, args)
    if error:
        return error
    fields = collect_fields(args, args.model)
    if not fields:
        return "Nothing to update"
    for attr, value in fields.items():
        setattr(obj, attr, value)
    session.commit()
    return f"Updated: {obj}"


def remove(session, args):
    obj, error = get_or_none(session, args)
    if error:
        return error
    session.delete(obj)
    session.commit()
    return f"Removed: {obj}"


ACTIONS = {"create": create, "list": list_all, "update": update, "remove": remove}


def main():
    args = parse_args()
    with Session() as session:
        try:
            print(ACTIONS[args.action](session, args))
        except IntegrityError as e:
            session.rollback()
            print(f"Database error: {e.orig}")


if __name__ == "__main__":
    main()
