from flask import Blueprint, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

llm = Blueprint("llm", __name__)


# Get chat sessions belonging to the CIO (Katrina, user_id=3).
# Example: GET /llm/calls
@llm.route("/calls", methods=["GET"])
def get_llm_calls():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT c.session_id, c.status, c.messages, u.username
               FROM ChatSession AS c
               JOIN Users AS u ON u.userID = c.user_id
               WHERE c.user_id = 3
               ORDER BY c.session_id DESC""")
        sessions = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(sessions)} chat sessions')
        return jsonify(sessions), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
