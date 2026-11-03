
from app import create_app
from models import db, User, Note
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():
    # Create database tables if they don't exist
    db.create_all()

    # Create sample users
    sample_users = [
        {
            "username": "katelyn",
            "password": "password123"
        },
        {
            "username": "testuser",
            "password": "password123"
        }
    ]

    for user_data in sample_users:
        user = User.query.filter_by(
            username=user_data["username"]
        ).first()

        if not user:
            user = User(
                username=user_data["username"],
                password_hash=generate_password_hash(
                    user_data["password"]
                )
            )
            db.session.add(user)

    db.session.commit()

    # Create sample notes
    katelyn = User.query.filter_by(username="katelyn").first()

    if katelyn and not Note.query.filter_by(user_id=katelyn.id).first():
        notes = [
            Note(
                title="My First Note",
                content="Welcome to my productivity application.",
                user_id=katelyn.id
            ),
            Note(
                title="Daily Goals",
                content="Complete my assignments and practice Python.",
                user_id=katelyn.id
            ),
            Note(
                title="Project Tasks",
                content="Finish authentication, CRUD operations and pagination.",
                user_id=katelyn.id
            )
        ]

        db.session.add_all(notes)

    db.session.commit()

    print("Database seeded successfully!")
    print("Sample users:")
    print("Username: katelyn | Password: password123")
    print("Username: testuser | Password: password123")
