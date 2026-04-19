from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for ChatSession routes
chatsession_routes = Blueprint("chatsession_routes", __name__)


# GETs all sessions for that user
@chatsession_routes.route("/<int:user_id>",methods=["GET"])
def GetAllChatSessions(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET all sessions for user")
    cursor.execute("SELECT * FROM ChatSession WHERE user_id = %s",(user_id,))
    sessions = cursor.fetchall()
    current_app.logger.info(f"Succesfully got sessions for user")
    return jsonify(sessions), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting all sessions for user {user_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# POST, create a new session for that user and requrires: status, messages
@chatsession_routes.route("/<int:user_id>",methods=["POST"])
def CreateChatSession(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"POST session")
    data = request.get_json()

    required_fields = ["status","messages"]
    for field in required_fields:
      if field not in data:
        return jsonify({"error": f"Missing required field: {field}"}), 400

    query = """
      INSERT INTO ChatSession (status, messages, user_id)
      VALUES (%s, %s, %s)
    """
    cursor.execute(query,(
      data["status"],
      data["messages"],
      user_id,
    ))
    get_db().commit()

    current_app.logger.info(f"Created session")
    return jsonify({"message": "Chat session created successfully"}), 201
  except Error as e:
    current_app.logger.error(f"The error {e} occured while creating session")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# DELETE hard delete all sessions for a user
@chatsession_routes.route("/<int:user_id>",methods=["DELETE"])
def DeleteAllChatSessions(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"DELETE all sessions for user")

    cursor.execute(
      "SELECT session_id FROM ChatSession WHERE user_id = %s",
      (user_id,),
    )
    if not cursor.fetchone():
      return jsonify({"error": "No sessions found for user"}), 404

    cursor.execute(
      "DELETE FROM ChatSession WHERE user_id = %s",
      (user_id,),
    )
    get_db().commit()

    current_app.logger.info(f"Deleted all sessions")
    return jsonify({"message": "All chat sessions deleted successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while deleting all sessions for user {user_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# GETs one specific session
@chatsession_routes.route("/<int:user_id>/<int:session_id>",methods=["GET"])
def GetChatSession(user_id, session_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET one session from user")
    cursor.execute(
      "SELECT * FROM ChatSession WHERE user_id = %s AND session_id = %s",
      (user_id, session_id),
    )
    session = cursor.fetchone()

    if not session:
      return jsonify({"error": "Chat session not found"}), 404

    current_app.logger.info("Got the session")
    return jsonify(session), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting session")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# PUT update the session of the user
@chatsession_routes.route("/<int:user_id>/<int:session_id>",methods=["PUT"])
def UpdateChatSession(user_id, session_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"PUT session")
    data = request.get_json()

    cursor.execute(
      "SELECT session_id FROM ChatSession WHERE user_id = %s AND session_id = %s",
      (user_id, session_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Chat session not found"}), 404

    allowed_fields = ["status","messages"]
    update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
    params = [data[f] for f in allowed_fields if f in data]

    if not update_fields:
      return jsonify({"error": "No valid fields to update"}), 400

    params.extend([user_id, session_id])
    query = f"UPDATE ChatSession SET {', '.join(update_fields)} WHERE user_id = %s AND session_id = %s"
    cursor.execute(query,params)
    get_db().commit()

    current_app.logger.info(f"Updated session")
    return jsonify({"message": "Chat session updated successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while updating session")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# DELETE hard delete a session of a user
@chatsession_routes.route("/<int:user_id>/<int:session_id>",methods=["DELETE"])
def DeleteChatSession(user_id, session_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"DELETE session")

    cursor.execute(
      "SELECT session_id FROM ChatSession WHERE user_id = %s AND session_id = %s",
      (user_id, session_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Chat session not found"}), 404

    cursor.execute(
      "DELETE FROM ChatSession WHERE user_id = %s AND session_id = %s",
      (user_id, session_id),
    )
    get_db().commit()

    current_app.logger.info(f"Deleted session")
    return jsonify({"message": "Chat session deleted successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while deleting session")
    return jsonify(str(e)), 500
  finally:
    cursor.close()
