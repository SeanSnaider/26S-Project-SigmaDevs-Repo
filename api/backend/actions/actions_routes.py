from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

actions = Blueprint("actions", __name__)


# Get the most recent dataset load action and the user who performed it.
# Matches any action_type starting with 'LOAD_'.
# Example: GET /action/actions
@actions.route("/actions", methods=["GET"])
def get_recent_load():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT u.username, a.action_type, a.date
               FROM Action AS a
               JOIN Users AS u ON u.userID = a.user_id
               WHERE a.action_type LIKE 'LOAD_%'
               ORDER BY a.date DESC
               LIMIT 1""")
        action = cursor.fetchone()

        current_app.logger.info('Retrieved most recent load action')

        if not action:
            return jsonify({"error": "No load action found"}), 404
        return jsonify(action), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get the most recent app deployment action and the user who performed it.
# Matches any action_type starting with 'DEPLOYED_'.
# Example: GET /action/deployments
@actions.route("/deployments", methods=["GET"])
def get_recent_deployment():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT u.username, a.action_type, a.date
               FROM Action AS a
               JOIN Users AS u ON u.userID = a.user_id
               WHERE a.action_type LIKE 'DEPLOYED_%'
               ORDER BY a.date DESC
               LIMIT 1""")
        action = cursor.fetchone()

        current_app.logger.info('Retrieved most recent deployment action')

        if not action:
            return jsonify({"error": "No deployment action found"}), 404
        return jsonify(action), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
