# 127.0.0.1:5000/api/login
# 127.0.0.1:5000/api/facility
# 127.0.0.1:5000/api/classroom
# 127.0.0.1:5000/api/teacher
# 127.0.0.1:5000/api/child

import flask
from flask import jsonify, request
from mysql.connector import Error
from sql import create_connection, execute_read_query, execute_query
import creds, functions

app = flask.Flask(__name__)
app.config["DEBUG"] = True

myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

# Login API
au = {'username': 'username', 'password': 'password'}
@app.route('/api/login', methods=['POST'])
def login():
    username = request.headers['username'] # get header parameter
    pw = request.headers['password']
    if username == au['username'] and pw == au['password']:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"})



# Facility CRUD Operations
@app.route('/api/facility', methods=['GET'])
def view_all_facilities():
    try:
        sql = "SELECT name FROM facility"
        facilities = execute_read_query(conn, sql)
        return jsonify(facilities)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/facility', methods=['POST'])
def add_facility():
    try:
        data = request.json
        if 'name' not in data:
            raise ValueError("Missing 'name' in request")
        sql = "INSERT INTO facility (name) VALUES ('%s')" % (data['name'])
        execute_query(conn, sql)
        return jsonify({"message": "Facility added successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/facility/<int:id>', methods=['PUT'])
def update_facility(id):
    try:
        data = request.json
        if 'name' not in data:
            raise ValueError("Missing 'name' in request")
        sql = "UPDATE facility SET name = %s WHERE id = %s" % (data['name'], id)
        execute_query(conn, sql)
        return jsonify({"message": "Facility updated successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/facility/<int:id>', methods=['DELETE'])
def delete_facility(id):
    try:
        sql = "DELETE FROM facility WHERE id = %s" % (id)
        execute_query(conn, sql)
        return jsonify({"message": "Facility deleted successfully"})
    except Error as e:
        return functions.handle_database_error(e)







# Classroom CRUD Operations
@app.route('/api/classroom', methods=['GET'])
def view_all_classrooms():
    try:
        sql = "SELECT capacity, name, facility FROM classroom"
        classrooms = execute_read_query(conn, sql)
        return jsonify(classrooms)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/classroom', methods=['POST'])
def add_classroom():
    try:
        data = request.json
        if 'name' not in data or 'capacity' not in data or 'facility' not in data:
            raise ValueError("Missing data in request")
        sql = "INSERT INTO classroom (name, capacity, facility) VALUES ('%s', '%s', '%s')" % (data['name'], data['capacity'], data['facility'])
        execute_query(conn, sql)
        return jsonify({"message": "Classroom added successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/classroom/<int:id>', methods=['PUT'])
def update_classroom(id):
    try:
        data = request.json
        if 'name' not in data or 'capacity' not in data or 'facility' not in data:
            raise ValueError("Missing data in request")
        sql = "UPDATE classroom SET name = %s, capacity = %s, facility = %s WHERE id = %s" % (data['name'], data['capacity'], data['facility'], id)
        execute_query(conn, sql)
        return jsonify({"message": "Classroom updated successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/classroom/<int:id>', methods=['DELETE'])
def delete_classroom(id):
    try:
        sql = "DELETE FROM classroom WHERE id = %s" % (id)
        execute_query(conn, sql)
        return jsonify({"message": "Classroom deleted successfully"})
    except Error as e:
        return functions.handle_database_error(e)






# Teacher CRUD Operations
@app.route('/api/teacher', methods=['GET'])
def view_all_teachers():
    try:
        sql = "SELECT firstname, lastname, room FROM teacher"
        teachers = execute_read_query(conn, sql)
        return jsonify(teachers)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/teacher', methods=['POST'])
def add_teacher():
    try:
        data = request.json
        if 'firstname' not in data or 'lastname' not in data or 'room' not in data:
            raise ValueError("Missing data in request")
        sql = "INSERT INTO teacher (firstname, lastname, room) VALUES ('%s', '%s', '%s')" % (data['firstname'], data['lastname'], data['room'])
        execute_query(conn, sql)
        return jsonify({"message": "Teacher added successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/teacher/<int:id>', methods=['PUT'])
def update_teacher(id):
    try:
        data = request.json
        if 'firstname' not in data or 'lastname' not in data or 'room' not in data:
            raise ValueError("Missing data in request")
        sql = "UPDATE teacher SET firstname = %s, lastname = %s, room = %s WHERE id = %s" % (data['firstname'], data['lastname'], data['room'], id)
        execute_query(conn, sql)
        return jsonify({"message": "Teacher updated successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        sql = "DELETE FROM teacher WHERE id = %s" % (id)
        execute_query(conn, sql)
        return jsonify({"message": "Teacher deleted successfully"})
    except Error as e:
        return functions.handle_database_error(e)






# Child CRUD Operations
@app.route('/api/child', methods=['GET'])
def view_all_children():
    try:
        sql = "SELECT firstname, lastname, age, room FROM child"
        children = execute_read_query(conn, sql)
        return jsonify(children)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/child', methods=['POST'])
def add_child():
    try:
        data = request.json
        if 'firstname' not in data or 'lastname' not in data or 'age' not in data or 'room' not in data:
            raise ValueError("Missing data in request")

        # Check if adding this child violates teacher-child constraints
        if not functions.can_add_child_to_classroom(data['room']):
            raise ValueError("Cannot add more children to this classroom based on teacher-to-child ratio or capacity")

        sql = "INSERT INTO child (firstname, lastname, age, room) VALUES ('%s', '%s', '%s', '%s')" % (data['firstname'], data['lastname'], data['age'], data['room'])
        execute_query(conn, sql)
        return jsonify({"message": "Child added successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)
        
@app.route('/api/child/<int:id>', methods=['PUT'])
def update_child(id):
    try:
        data = request.json
        required_fields = ['firstname', 'lastname', 'age', 'room']
        if not all(field in data for field in required_fields):
            raise ValueError("Missing data in request")

        # Fetch the current room assignment for the child to check if it's being changed.
        current_room_sql = "SELECT room FROM child WHERE id = %s" % (id)
        current_room_result = execute_read_query(conn, current_room_sql)
        if not current_room_result:
            raise ValueError("Child not found")

        new_room_id = data['room']
        current_room_id = current_room_result[0]['room']

        # If the room assignment is being changed, check if the new classroom can accommodate another child.
        if new_room_id != current_room_id and not functions.can_add_child_to_classroom(new_room_id):
            raise ValueError("Cannot move child to the specified classroom based on teacher-to-child ratio or capacity")

        sql = "UPDATE child SET firstname = %s, lastname = %s, age = %s, room = %s WHERE id = %s" % (data['firstname'], data['lastname'], data['age'], data['room'], id)
        execute_query(conn, sql)
        return jsonify({"message": "Child updated successfully"})
    except ValueError as ve:
        return functions.handle_bad_request(ve)
    except Error as e:
        return functions.handle_database_error(e)

@app.route('/api/child/<int:id>', methods=['DELETE'])
def delete_child(id):
    try:
        sql = "DELETE FROM child WHERE id = %s" % (id)
        execute_query(conn, sql)
        return jsonify({"message": "Child deleted successfully"})
    except Error as e:
        return functions.handle_database_error(e)



app.run()