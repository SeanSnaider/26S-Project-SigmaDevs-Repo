from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# generic routing blueprint for the data cleaning methods
datacleaning_routes = Blueprint("datacleaning_routes", __name__)

# GET /datacleaning
# will return all datacleaning for all users
@datacleaning_routes.route("/", methods=["GET"])
def get_all_datacleaning():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /datacleaning')
        query = """
                SELECT method_order, parameter, method_type, method_id, CleaningDataSet
                FROM DataCleaningMethod
                """
        cursor.execute(query)
        method = cursor.fetchall()
        return jsonify(method), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_datacleaning: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /datacleaning/id
# will return a single instance of data cleaning
@datacleaning_routes.route("/<int:method_id>", methods=["GET"])
def get_specific_datacleaning(method_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /datacleaning/{method_id}')
        query = """
                SELECT method_order, parameter, method_type, method_id, CleaningDataSet
                FROM DataCleaningMethod
                WHERE method_id = %s
                """
        cursor.execute(query, (method_id, ))
        method = cursor.fetchone()
        if not method:
            return jsonify({"error": "DataCleaningMethod not found"}), 404
        return jsonify(method), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_specific_datacleaning: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# POST METHOD

# POST /DataCleaning/<user_id>
# will post a specific datacleaning method for a given user (admin)
@datacleaning_routes.route("/", methods=["POST"])
def post_datacleaning():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        query = """
                INSERT INTO DataCleaningMethod 
                (method_order, parameter, method_type, CleaningDataSet)
                VALUES (%s, %s, %s, %s)
                """
        cursor.execute(query, (data["method_order"], data["parameter"], data["method_type"], data["CleaningDataSet"]))
        get_db().commit()
        new_id = cursor.lastrowid
        return jsonify({"id": new_id, "method_order": data["method_order"], "parameter": data["parameter"], "method_type": data["method_type"], "CleaningDataSet": data["CleaningDataSet"]}), 201
    except Error as e:
        current_app.logger.error(f"Database error in post_datacleaning: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Put call

# PUT /DataCleaningmethod/<method_id>
# will edit a specific dataset given whatever parameters are inputted
@datacleaning_routes.route("/<int:method_id>", methods=["PUT"])
def put_datacleaning_method(method_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        query = """
                UPDATE DataCleaningMethod
                SET method_order = %s,
                    parameter = %s,
                    method_type = %s,
                    CleaningDataSet = %s
                WHERE method_id = %s
                """
        cursor.execute(query, (data["method_order"], data["parameter"], data["method_type"], data["CleaningDataSet"], method_id))
        get_db().commit()
        return jsonify({"id": method_id, "method_order": data["method_order"], "parameter": data["parameter"], "method_type": data["method_type"], "CleaningDataSet": data["CleaningDataSet"]}), 200
    except Error as e:
        current_app.logger.error(f"Database error in put_datacleaning_method: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# delete call


# DELETE /DataCleaningMethod/<method_id>
# will delete a specific set datacleaningmethod for a given user
@datacleaning_routes.route("/<int:method_id>", methods=["DELETE"])
def delete_users_dataset(method_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
                DELETE FROM DataCleaningMethod
                WHERE method_id = %s
                """
        cursor.execute(query, (method_id,))
        get_db().commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_users_dataset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()