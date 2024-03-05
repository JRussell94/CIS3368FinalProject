import flask
from flask import jsonify, request
from mysql.connector import Error
from sql import create_connection, execute_read_query, execute_query
import creds

app = flask.Flask(__name__)
app.config["DEBUG"] = True

myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

# A teacher can never watch more than 10 children at once.
# If a classroom has a capacity of 20, but only 1 teacher is working that classroom, then even though the capacity is 20, only 10 children can be assigned to that classroom.
# Only if a second teacher is assigned to that room, one should be able to assign children up to the capacity of 20.

# Could be imported 
def can_add_child_to_classroom(classroom_id):
    try:
        # Count the number of teachers in the classroom
        teacher_count_sql = "SELECT COUNT(*) as count FROM teacher WHERE room = %s"
        teacher_count_result = execute_read_query(conn, teacher_count_sql, (classroom_id,))
        teacher_count = teacher_count_result[0]['count']

        # Calculate max children allowed based on teacher count
        max_children_allowed = 10 * teacher_count

        # Count the current number of children in the classroom
        child_count_sql = "SELECT COUNT(*) as count FROM child WHERE room = %s"
        child_count_result = execute_read_query(conn, child_count_sql, (classroom_id,))
        current_child_count = child_count_result[0]['count']

        # Check classroom capacity
        capacity_sql = "SELECT capacity FROM classroom WHERE id = %s"
        capacity_result = execute_read_query(conn, capacity_sql, (classroom_id,))
        classroom_capacity = capacity_result[0]['capacity']

        # Ensure adding another child does not exceed max_children_allowed or classroom_capacity
        if current_child_count < min(max_children_allowed, classroom_capacity):
            return True
        else:
            return False
    except Error as e:
        print(f"Database error during capacity check: {e}")
        return False  # Safely assume failure on error

# Error handling utility functions
def handle_database_error(e):
    return jsonify({"error": "Database error", "message": str(e)})

def handle_bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e)})

# Login API

authorizedusers = [
    {
        #default user
        'username': 'username',
        'password': 'password'
    }
]


@app.route('/api/login', methods=['POST'])
def login():
    username = request.headers['username'] # get header parameter
    pw = request.headers['password']
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'password':
            return jsonify({"message": "Login successful"})
    else:
            return jsonify({"message": "Login failed"})


# Facility CRUD Operations
@app.route('/api/facility', methods=['GET'])
def view_all_facilities():
    try:
        sql = "SELECT * FROM facility"
        facilities = execute_read_query(conn, sql)
        return jsonify(facilities)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/facility', methods=['POST'])
def add_facility():
    try:
        data = request.json
        if 'name' not in data:
            raise ValueError("Missing 'name' in request")
        sql = "INSERT INTO facility (name) VALUES (%s)"
        execute_query(conn, sql, (data['name'],))
        return jsonify({"message": "Facility added successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/facility/<int:id>', methods=['PUT'])
def update_facility(id):
    try:
        data = request.json
        if 'name' not in data:
            raise ValueError("Missing 'name' in request")
        sql = "UPDATE facility SET name = %s WHERE id = %s"
        execute_query(conn, sql, (data['name'], id))
        return jsonify({"message": "Facility updated successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/facility/<int:id>', methods=['DELETE'])
def delete_facility(id):
    try:
        sql = "DELETE FROM facility WHERE id = %s"
        execute_query(conn, sql, (id,))
        return jsonify({"message": "Facility deleted successfully"})
    except Error as e:
        return handle_database_error(e)

# Classroom CRUD Operations
@app.route('/api/classroom', methods=['GET'])
def view_all_classrooms():
    try:
        sql = "SELECT * FROM classroom"
        classrooms = execute_read_query(conn, sql)
        return jsonify(classrooms)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/classroom', methods=['POST'])
def add_classroom():
    try:
        data = request.json
        if 'name' not in data or 'capacity' not in data or 'facility' not in data:
            raise ValueError("Missing data in request")
        sql = "INSERT INTO classroom (name, capacity, facility) VALUES (%s, %s, %s)"
        execute_query(conn, sql, (data['name'], data['capacity'], data['facility']))
        return jsonify({"message": "Classroom added successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/classroom/<int:id>', methods=['PUT'])
def update_classroom(id):
    try:
        data = request.json
        if 'name' not in data or 'capacity' not in data or 'facility' not in data:
            raise ValueError("Missing data in request")
        sql = "UPDATE classroom SET name = %s, capacity = %s, facility = %s WHERE id = %s"
        execute_query(conn, sql, (data['name'], data['capacity'], data['facility'], id))
        return jsonify({"message": "Classroom updated successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/classroom/<int:id>', methods=['DELETE'])
def delete_classroom(id):
    try:
        sql = "DELETE FROM classroom WHERE id = %s"
        execute_query(conn, sql, (id,))
        return jsonify({"message": "Classroom deleted successfully"})
    except Error as e:
        return handle_database_error(e)

# Teacher CRUD Operations
@app.route('/api/teacher', methods=['GET'])
def view_all_teachers():
    try:
        sql = "SELECT * FROM teacher"
        teachers = execute_read_query(conn, sql)
        return jsonify(teachers)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/teacher', methods=['POST'])
def add_teacher():
    try:
        data = request.json
        if 'firstname' not in data or 'lastname' not in data or 'room' not in data:
            raise ValueError("Missing data in request")
        sql = "INSERT INTO teacher (firstname, lastname, room) VALUES (%s, %s, %s)"
        execute_query(conn, sql, (data['firstname'], data['lastname'], data['room']))
        return jsonify({"message": "Teacher added successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/teacher/<int:id>', methods=['PUT'])
def update_teacher(id):
    try:
        data = request.json
        if 'firstname' not in data or 'lastname' not in data or 'room' not in data:
            raise ValueError("Missing data in request")
        sql = "UPDATE teacher SET firstname = %s, lastname = %s, room = %s WHERE id = %s"
        execute_query(conn, sql, (data['firstname'], data['lastname'], data['room'], id))
        return jsonify({"message": "Teacher updated successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        sql = "DELETE FROM teacher WHERE id = %s"
        execute_query(conn, sql, (id,))
        return jsonify({"message": "Teacher deleted successfully"})
    except Error as e:
        return handle_database_error(e)

# Child CRUD Operations
@app.route('/api/child', methods=['GET'])
def view_all_children():
    try:
        sql = "SELECT * FROM child"
        children = execute_read_query(conn, sql)
        return jsonify(children)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/child', methods=['POST'])
def add_child():
    try:
        data = request.json
        required_fields = ['firstname', 'lastname', 'age', 'room']
        if not all(field in data for field in required_fields):
            raise ValueError("Missing data in request")

        # Check if adding this child violates teacher-child constraints
        if not can_add_child_to_classroom(data['room']):
            raise ValueError("Cannot add more children to this classroom based on teacher-to-child ratio or capacity")

        sql = "INSERT INTO child (firstname, lastname, age, room) VALUES (%s, %s, %s, %s)"
        execute_query(conn, sql, (data['firstname'], data['lastname'], data['age'], data['room']))
        return jsonify({"message": "Child added successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)
        
@app.route('/api/child/<int:id>', methods=['PUT'])
def update_child(id):
    try:
        data = request.json
        required_fields = ['firstname', 'lastname', 'age', 'room']
        if not all(field in data for field in required_fields):
            raise ValueError("Missing data in request")

        # Fetch the current room assignment for the child to check if it's being changed.
        current_room_sql = "SELECT room FROM child WHERE id = %s"
        current_room_result = execute_read_query(conn, current_room_sql, (id,))
        if not current_room_result:
            raise ValueError("Child not found")

        new_room_id = data['room']
        current_room_id = current_room_result[0]['room']

        # If the room assignment is being changed, check if the new classroom can accommodate another child.
        if new_room_id != current_room_id and not can_add_child_to_classroom(new_room_id):
            raise ValueError("Cannot move child to the specified classroom based on teacher-to-child ratio or capacity")

        sql = "UPDATE child SET firstname = %s, lastname = %s, age = %s, room = %s WHERE id = %s"
        execute_query(conn, sql, (data['firstname'], data['lastname'], data['age'], data['room'], id))
        return jsonify({"message": "Child updated successfully"})
    except ValueError as ve:
        return handle_bad_request(ve)
    except Error as e:
        return handle_database_error(e)

@app.route('/api/child/<int:id>', methods=['DELETE'])
def delete_child(id):
    try:
        sql = "DELETE FROM child WHERE id = %s"
        execute_query(conn, sql, (id,))
        return jsonify({"message": "Child deleted successfully"})
    except Error as e:
        return handle_database_error(e)


app.run()
