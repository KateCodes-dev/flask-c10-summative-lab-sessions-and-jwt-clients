from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db, User, Note


jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "your-secret-key-change-this"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    if test_config:
        app.config.update(test_config)

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    # SIGNUP
    @app.route("/signup", methods=["POST"])
    def signup():
        data = request.get_json() or {}

        username = data.get("username")
        password = data.get("password")
        confirmation = data.get("password_confirmation")

        errors = []

        if not username or not password or not confirmation:
            errors.append("All fields are required")

        if password and confirmation and password != confirmation:
            errors.append("Passwords do not match")

        if username and User.query.filter_by(username=username).first():
            errors.append("Username already exists")

        if errors:
            return jsonify({"errors": errors}), 422

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username
            },
            "token": token,
            "access_token": token
        }), 201

    # LOGIN
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json() or {}

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not password or not check_password_hash(
            user.password_hash, password
        ):
            return jsonify({
                "error": "Invalid username or password"
            }), 401

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "access_token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }), 200

    # GET CURRENT USER
    @app.route("/me", methods=["GET"])
    @jwt_required()
    def me():
        current_user_id = int(get_jwt_identity())

        user = db.session.get(User, current_user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        return jsonify({
            "id": user.id,
            "username": user.username
        }), 200

    # CREATE NOTE
    @app.route("/notes", methods=["POST"])
    @jwt_required()
    def create_note():
        current_user_id = int(get_jwt_identity())

        data = request.get_json() or {}

        title = data.get("title")
        content = data.get("content")

        if not title or not content:
            return jsonify({
                "error": "Title and content are required"
            }), 400

        note = Note(
            title=title,
            content=content,
            user_id=current_user_id
        )

        db.session.add(note)
        db.session.commit()

        return jsonify({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "user_id": note.user_id
        }), 201

    # GET ALL NOTES WITH PAGINATION
    @app.route("/notes", methods=["GET"])
    @jwt_required()
    def get_notes():
        current_user_id = int(get_jwt_identity())

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if page < 1 or per_page < 1:
            return jsonify({
                "error": "Invalid pagination parameters"
            }), 400

        pagination = Note.query.filter_by(
            user_id=current_user_id
        ).order_by(Note.id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        notes = [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "user_id": note.user_id
            }
            for note in pagination.items
        ]

        return jsonify({
            "notes": notes,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages
            }
        }), 200

    # UPDATE NOTE
    @app.route("/notes/<int:note_id>", methods=["PATCH", "PUT"])
    @jwt_required()
    def update_note(note_id):
        current_user_id = int(get_jwt_identity())

        note = Note.query.filter_by(
            id=note_id,
            user_id=current_user_id
        ).first()

        if not note:
            return jsonify({
                "error": "Note not found"
            }), 404

        data = request.get_json() or {}

        if "title" in data:
            note.title = data["title"]

        if "content" in data:
            note.content = data["content"]

        db.session.commit()

        return jsonify({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "user_id": note.user_id
        }), 200

    # DELETE NOTE
    @app.route("/notes/<int:note_id>", methods=["DELETE"])
    @jwt_required()
    def delete_note(note_id):
        current_user_id = int(get_jwt_identity())

        note = Note.query.filter_by(
            id=note_id,
            user_id=current_user_id
        ).first()

        if not note:
            return jsonify({
                "error": "Note not found"
            }), 404

        db.session.delete(note)
        db.session.commit()

        return "", 204

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
