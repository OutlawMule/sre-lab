from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "students.json"

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE,"r") as f:
        return json.load(f)

def save_students(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

@app.route("/students", methods=["GET"])
def get_students():
    students = load_students()
    return jsonify(students)

@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    if not data or "name" not in data or "grade" not in data:
        return jsonify({"error":"name and grade required"}),400

    students = load_students()

    new_student = {
        "id": len(students)+1,
        "name": data["name"],
        "grade": data["grade"]
    }

    students.append(new_student)
    save_students(students)

    return jsonify(new_student),201


@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    students = load_students()

    for student in students:
        if student["id"] == id:
            return jsonify(student)

    return jsonify({"error":"Student not found"}),404


if __name__ == "__main__":
    app.run(debug=True)

    @app.route("/students/search", methods=["GET"])
    def search_students():

        name = request.args.get("name")

        students = load_students()

        result = [s for s in students if name.lower() in s["name"].lower()]

        return jsonify(result)