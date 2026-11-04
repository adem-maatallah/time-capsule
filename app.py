from datetime import date
from flask import Flask, jsonify, request, render_template
import database

app = Flask(__name__)
database.init_db()


def is_locked(capsule):
    return date.today() < date.fromisoformat(capsule["open_date"])


def public_view(capsule):
    """Capsule info that is safe to show even while locked (no message)."""
    days_left = (date.fromisoformat(capsule["open_date"]) - date.today()).days
    return {
        "id": capsule["id"],
        "title": capsule["title"],
        "author": capsule["author"],
        "open_date": capsule["open_date"],
        "created_at": capsule["created_at"],
        "locked": is_locked(capsule),
        "days_left": max(days_left, 0),
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/capsules", methods=["GET"])
def list_capsules():
    capsules = database.get_all_capsules()
    return jsonify([public_view(c) for c in capsules]), 200


@app.route("/api/capsules", methods=["POST"])
def add_capsule():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    title = str(data.get("title", "")).strip()
    message = str(data.get("message", "")).strip()
    author = str(data.get("author", "")).strip()
    open_date = str(data.get("open_date", "")).strip()

    if not title or not message or not author or not open_date:
        return jsonify({"error": "title, message, author and open_date are all required."}), 400

    try:
        parsed_date = date.fromisoformat(open_date)
    except ValueError:
        return jsonify({"error": "open_date must be in the format YYYY-MM-DD."}), 400

    if parsed_date <= date.today():
        return jsonify({"error": "open_date must be in the future."}), 400

    new_id = database.create_capsule(title, message, author, open_date)
    capsule = database.get_capsule(new_id)
    return jsonify(public_view(capsule)), 201


@app.route("/api/capsules/<int:capsule_id>", methods=["GET"])
def open_capsule(capsule_id):
    capsule = database.get_capsule(capsule_id)
    if capsule is None:
        return jsonify({"error": "Capsule not found."}), 404

    if is_locked(capsule):
        return jsonify({**public_view(capsule), "error": "This capsule is still locked."}), 423

    return jsonify({**public_view(capsule), "message": capsule["message"]}), 200


@app.route("/api/capsules/<int:capsule_id>", methods=["DELETE"])
def remove_capsule(capsule_id):
    if not database.delete_capsule(capsule_id):
        return jsonify({"error": "Capsule not found."}), 404
    return jsonify({"result": "Capsule deleted."}), 200


if __name__ == "__main__":
    app.run(debug=True)