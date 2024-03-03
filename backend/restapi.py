import flask
from flask import jsonify, request
from sql import create_connection, execute_read_query, execute_query
import creds

# http://127.0.0.1:5000/api/facility
# http://127.0.0.1:5000/api/classroom
# http://127.0.0.1:5000/api/teacher
# http://127.0.0.1:5000/api/child

app = flask.Flask(__name__)
app.config["DEBUG"] = True

myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)


# A teacher can never watch more than 10 children at once.
# If a classroom has a capacity of 20, but only 1 teacher is working that classroom, then even though the capacity is 20, only 10 children can be assigned to that classroom.
# Only if a second teacher is assigned to that room, one should be able to assign children up to the capacity of 20.

# TODO: create dictionary with username/password and validate through that
def can_add_child_to_classroom(classroom_id):
    # Count the number of teachers in the classroom
    teachers_sql = "SELECT COUNT(*) FROM teacher WHERE room = {}".format(classroom_id)
    teachers_count = execute_read_query(conn, teachers_sql)[0]['COUNT(*)']
    
    # Count the current number of children in the classroom
    children_sql = "SELECT COUNT(*) FROM child WHERE room = {}".format(classroom_id)
    children_count = execute_read_query(conn, children_sql)[0]['COUNT(*)']
    
    # Calculate the max number of children allowed based on the number of teachers
    max_children_allowed = 10 * teachers_count
    
    # Check if adding another child would exceed this limit
    if children_count < max_children_allowed:
        return True  # Can add another child
    else:
        return False  # Cannot add more children without exceeding the limit


# login API
@app.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth and auth.username == 'admin' and auth.password == 'password':
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Login failed"})


# CRUD Operation examples for all tables
# Facility CRUD Operations
@app.route('/api/facility', methods=['GET'])
def view_all_facilities():
    sql = "SELECT * FROM facility" # TODO: SELECT only columns needed, not ID
    query = execute_read_query(conn, sql)
    return jsonify(query)

@app.route('/api/facility', methods=['POST'])
def add_facility():
    data = request.json
    sql = "INSERT INTO facility (name) VALUES ('{}')".format(data['name'])
    execute_query(conn, sql)
    return jsonify({"message": "Facility added successfully"})

@app.route('/api/facility/<int:id>', methods=['PUT'])
def update_facility(id):
    data = request.json
    sql = "UPDATE facility SET name = '{}' WHERE id = {}".format(data['name'], id)
    execute_query(conn, sql)
    return jsonify({"message": "Facility updated successfully"})

@app.route('/api/facility/<int:id>', methods=['DELETE'])
def delete_facility(id):
    sql = "DELETE FROM facility WHERE id = {}".format(id)
    execute_query(conn, sql)
    return jsonify({"message": "Facility deleted successfully"})


# Classroom CRUD Operations
@app.route('/api/classroom', methods=['GET'])
def view_all_classrooms():
    sql = "SELECT * FROM classroom" # TODO: SELECT only columns needed, not ID
    query = execute_read_query(conn, sql)
    return jsonify(query)

@app.route('/api/classroom', methods=['POST'])
def add_classroom():
    data = request.json
    sql = "INSERT INTO classroom (capacity, name, facility) VALUES ('{}', '{}', '{}')".format(data['capacity'], data['name'], data['facility']) # facility entered in postman has to be ID not name
    execute_query(conn, sql)
    return jsonify({"message": "Classroom added successfully"})

@app.route('/api/classroom/<int:id>', methods=['PUT'])
def update_classroom(id):
    data = request.json
    sql = "UPDATE classroom SET capacity = '{}', name = '{}', facility = '{}' WHERE id = {}".format(data['capacity'], data['name'], data['facility'], id) # facility entered in postman has to be ID not name
    execute_query(conn, sql)
    return jsonify({"message": "Classroom updated successfully"})

@app.route('/api/classroom/<int:id>', methods=['DELETE'])
def delete_classroom(id):
    sql = "DELETE FROM classroom WHERE id = {}".format(id)
    execute_query(conn, sql)
    return jsonify({"message": "Classroom deleted successfully"})


# Teacher CRUD Operations
@app.route('/api/teacher', methods=['GET'])
def view_all_teachers():
    sql = "SELECT * FROM teacher" # TODO: SELECT only columns needed, not ID
    query = execute_read_query(conn, sql)
    return jsonify(query)

@app.route('/api/teacher', methods=['POST'])
def add_teacher():
    data = request.json
    sql = "INSERT INTO teacher (firstname, lastname, room) VALUES ('{}', '{}', '{}')".format(data['firstname'], data['lastname'], data['room']) # room entered in postman has to be ID not name
    execute_query(conn, sql)
    return jsonify({"message": "Teacher added successfully"})

@app.route('/api/teacher/<int:id>', methods=['PUT'])
def update_teacher(id):
    data = request.json
    sql = "UPDATE teacher SET firstname = '{}', lastname = '{}', room = '{}' WHERE id = {}".format(data['firstname'], data['lastname'], data['room'], id) # room entered in postman has to be ID not name
    execute_query(conn, sql)
    return jsonify({"message": "Teacher updated successfully"})

@app.route('/api/teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    sql = "DELETE FROM teacher WHERE id = {}".format(id)
    execute_query(conn, sql)
    return jsonify({"message": "Teacher deleted successfully"})


# Child CRUD Operations
@app.route('/api/child', methods=['GET'])
def view_all_children():
    sql = "SELECT * FROM child" # TODO: SELECT only columns needed, not ID
    query = execute_read_query(conn, sql)
    return jsonify(query)

@app.route('/api/child', methods=['POST'])
def add_child():
    data = request.json
    sql = "INSERT INTO child (firstname, lastname, age, room) VALUES ('{}', '{}', '{}', '{}')".format(data['firstname'], data['lastname'], data['age'], data['room']) # room entered in postman has to be ID not name
    execute_query(conn, sql)
    return jsonify({"message": "Child added successfully"})

@app.route('/api/child/<int:id>', methods=['PUT'])
def update_child(id):
    data = request.json
    sql = "UPDATE child SET firstname = '{}', lastname = '{}', age = '{}', room = '{}' WHERE id = {}".format(data['firstname'], data['lastname'], data['age'], data['room'], id) # room entered in postman has to be ID not name
    execute_query(conn, sql)
    return jsonify({"message": "Child updated successfully"})

@app.route('/api/child/<int:id>', methods=['DELETE'])
def delete_child(id):
    sql = "DELETE FROM child WHERE id = {}".format(id)
    execute_query(conn, sql)
    return jsonify({"message": "Child deleted successfully"})

app.run()