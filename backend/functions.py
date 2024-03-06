import flask
from flask import jsonify, request
from mysql.connector import Error
from sql import create_connection, execute_read_query, execute_query
import creds

myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

# A teacher can never watch more than 10 children at once.
# If a classroom has a capacity of 20, but only 1 teacher is working that classroom, then even though the capacity is 20, only 10 children can be assigned to that classroom.
# Only if a second teacher is assigned to that room, one should be able to assign children up to the capacity of 20.

def can_add_child_to_classroom(classroom_id):
    try:
        # Count the number of teachers in the classroom
        teacher_count_sql = "SELECT COUNT(*) as count FROM teacher WHERE room = %s" % (classroom_id)
        teacher_count_result = execute_read_query(conn, teacher_count_sql)
        teacher_count = teacher_count_result[0]['count']

        # Calculate max children allowed based on teacher count
        max_children_allowed = 10 * teacher_count

        # Count the current number of children in the classroom
        child_count_sql = "SELECT COUNT(*) as count FROM child WHERE room = %s" % (classroom_id)
        child_count_result = execute_read_query(conn, child_count_sql)
        current_child_count = child_count_result[0]['count']

        # Check classroom capacity
        capacity_sql = "SELECT capacity FROM classroom WHERE id = %s" % (classroom_id)
        capacity_result = execute_read_query(conn, capacity_sql)
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