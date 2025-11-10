from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

app = Flask(__name__)

engine = create_engine('postgresql://postgres@localhost:5432/studentdata')
# Setup your DB engine (replace with your actual DB URL)
def db_engine():
    return create_engine('postgresql://postgres@localhost:5432/mydatabase')

# 1. Get all students
@app.route('/students', methods=['GET'])
def getAllStudents():
    engine = db_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM students"))
        students = [dict((row._mapping)) for row in result]
    return jsonify(students), 200

# 2. Add a new student
@app.route('/students', methods=['POST'])
def addStudent():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    enrollment_date = data.get('enrollment_date')  # expect 'YYYY-MM-DD'

    engine = db_engine()
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (:fn, :ln, :email, :enroll)"),
            {"fn": first_name, "ln": last_name, "email": email, "enroll": enrollment_date}
        )
        conn.commit()

    return jsonify({"message": "Student added"}), 200

# 3. Update student's email
@app.route('/students/<int:student_id>/email', methods=['PUT'])
def updateStudentEmail(student_id):
    data = request.json
    new_email = data.get('new_email')

    engine = db_engine()
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE students SET email = :email WHERE student_id = :id"),
            {"email": new_email, "id": student_id}
        )
        conn.commit()

    return jsonify({"message": "Email updated"}), 200

# 4. Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def deleteStudent(student_id):
    engine = db_engine()
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM students WHERE student_id = :id"),
            {"id": student_id}
        )
        conn.commit()

    return jsonify({"message": "Student deleted"}), 200

@app.route('/test_api')
def test_api():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
