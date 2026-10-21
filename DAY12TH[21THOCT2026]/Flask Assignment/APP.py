from flask import Flask
from flask import jsonify,request

app = Flask(__name__)
students = [
        {"id": 1, "name": "Rhea Kapoor", "course": "python", "score": 82},
        {"id": 2, "name": "Zain Malik", "course": "SQL", "score": 76},
        {"id": 3, "name": "Devika Rao", "course": "Cloud", "score": 91}
    ]
# 1. GET all students
# Create:
# GET /students
# It should return all student records as JSON

@app.route("/students")
def get_students():
    # students = [
    #     {"id": 1, "name": "Rhea Kapoor","course":"python","score":82},
    #     {"id": 2, "name": "Zain Malik","course":"SQL","score":76},
    #     {"id": 3, "name": "Devika Rao","course":"Cloud","score":91}
    # ]

    return jsonify(students)

# 2. GET student by ID
# Create:
# GET /students/<id>
# Example:
# GET /students/2
# Return the matching student.
# If no student exists, return:
# {
# }
#   "message": "Student not found"
# with status code 404


@app.route("/students/<int:student_id>")
def get_student(student_id):
    # students = [
    #     {"id": 1, "name": "Rhea Kapoor", "course": "python", "score": 82},
    #     {"id": 2, "name": "Zain Malik", "course": "SQL", "score": 76},
    #     {"id": 3, "name": "Devika Rao", "course": "Cloud", "score": 91}
    # ]

    for student in students:
        if student["id"] == student_id:
            return jsonify(student)

    return jsonify({"message": "Student not found"}), 404

# 3. POST — Add a student
# Create:
# POST /students
# Request body example:
# {
#   "id": 4,
#   "name": "Kabir Sen",
#   "course": "Docker",
#   "score": 88
# }
# Add the new student to the list.
# Return:
# {
# }
#   "message": "Student added successfully"
@app.route("/students",methods=['POST'])
def add_student():
    # students = [
    #     {"id": 1, "name": "Rhea Kapoor", "course": "python", "score": 82},
    #     {"id": 2, "name": "Zain Malik", "course": "SQL", "score": 76},
    #     {"id": 3, "name": "Devika Rao", "course": "Cloud", "score": 91}
    # ]
    student=request.get_json()
    students.append(student)
    return jsonify({"message":"student  successfully added"})


# 4. PUT — Update a student
# Create:
# PUT /students/<id>
# Example request:
# {
# }
#   "name": "Kabir Sen",
#   "course": "Docker",
#   "score": 93
# Update the matching student.
# Return:
# {
# }
#   "message": "Student updated successfully"
# If the ID does not exist, return 404
@app.route("/students/<int:student_id>",methods=['PUT'])
def update_student(student_id):

    data=request.get_json()
    for student in students:
        if student["id"] == student_id:
            student["name"] = data.get("name",student["name"])
            student["course"] = data.get("course",student["course"])
            student["score"] = data.get("score",student["score"])
            return jsonify({"message":"student successfully updated"})
        return jsonify({"message":"student not found"}),404

#delete

@app.route("/students/<int:student_id>",methods=['DELETE'])
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return jsonify({"message":"student successfully deleted"})
        return jsonify({"message":"student not found"}),404


if __name__ == "__main__":
    app.run(debug=True)