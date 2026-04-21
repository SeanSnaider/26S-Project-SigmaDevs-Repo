from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for DailySummary routes
dailysummary_routes = Blueprint("dailysummary_routes", __name__)


# GETs all summaries for that user
@dailysummary_routes.route("/<int:user_id>",methods=["GET"])
def GetAllDailySummaries(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET all summaries for user")
    cursor.execute("SELECT * FROM DailySummary WHERE user_id = %s",(user_id,))
    summaries = cursor.fetchall()
    current_app.logger.info(f"Succesfully got summaries for user")
    return jsonify(summaries), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting all summaries for user {user_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# POST, create a new summary for that user and requrires: generated_at, summary_date, summary
@dailysummary_routes.route("/<int:user_id>",methods=["POST"])
def CreateDailySummary(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"POST summary")
    data = request.get_json()

    required_fields = ["generated_at","summary_date","summary"]
    for field in required_fields:
      if field not in data:
        return jsonify({"error": f"Missing required field: {field}"}), 400

    query = """
      INSERT INTO DailySummary (generated_at, summary_date, summary, user_id)
      VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query,(
      data["generated_at"],
      data["summary_date"],
      data["summary"],
      user_id,
    ))
    get_db().commit()

    current_app.logger.info(f"Created summary")
    return jsonify({"message": "Daily summary created successfully"}), 201
  except Error as e:
    current_app.logger.error(f"The error {e} occured while creating summary")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# PUT update summaries for the user
@dailysummary_routes.route("/<int:user_id>",methods=["PUT"])
def UpdateDailySummaries(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"PUT summaries for user")
    data = request.get_json()

    cursor.execute(
      "SELECT summaryId FROM DailySummary WHERE user_id = %s",
      (user_id,),
    )
    if not cursor.fetchone():
      return jsonify({"error": "No summaries found for user"}), 404

    allowed_fields = ["generated_at","summary_date","summary"]
    update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
    params = [data[f] for f in allowed_fields if f in data]

    if not update_fields:
      return jsonify({"error": "No valid fields to update"}), 400

    params.append(user_id)
    query = f"UPDATE DailySummary SET {', '.join(update_fields)} WHERE user_id = %s"
    cursor.execute(query,params)
    get_db().commit()

    current_app.logger.info(f"Updated summaries")
    return jsonify({"message": "Daily summaries updated successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while updating summaries")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# DELETE hard delete all summaries for a user
@dailysummary_routes.route("/<int:user_id>",methods=["DELETE"])
def DeleteAllDailySummaries(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"DELETE summaries for user")

    cursor.execute(
      "SELECT summaryId FROM DailySummary WHERE user_id = %s",
      (user_id,),
    )
    if not cursor.fetchone():
      return jsonify({"error": "No summaries found for user"}), 404

    cursor.execute(
      "DELETE FROM DailySummary WHERE user_id = %s",
      (user_id,),
    )
    get_db().commit()

    current_app.logger.info(f"Deleted summaries")
    return jsonify({"message": "Daily summaries deleted successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while deleting summaries")
    return jsonify(str(e)), 500
  finally:
    cursor.close()
