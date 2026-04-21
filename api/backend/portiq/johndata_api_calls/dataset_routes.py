from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# generic routing blueprint for the dataset routes
dataset_routes = Blueprint("dataset_routes", __name__)

# GET /datasets
# Return all datasets for all users
@dataset_routes.route("/", methods=["GET"])
def get_all_datasets():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /datasets')
        query = """
                SELECT dataset_id, name, type, user_id
                FROM Dataset
                """
        cursor.execute(query)
        dataset = cursor.fetchall()
        return jsonify(dataset), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_datasets: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /Datasets/<user_id>
# returns all datasets for a specific user
@dataset_routes.route("/<int:user_id>", methods=["GET"])
def get_dataset(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
       current_app.logger.info(f"GET /datasets/{user_id}")
       query = """
                SELECT dataset_id, name, type, user_id
                from Dataset
                WHERE user_id = %s
                """
       
       cursor.execute(query, (user_id,))
       dataset = cursor.fetchall()

       return jsonify(dataset), 200
    
    except Error as e:
        current_app.logger.error(f"Database error in get_dataset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /Datasets/<user_id>/<id>
# returns all datasets for a specific user given an id
@dataset_routes.route("/<int:user_id>/<int:dataset_id>", methods=["GET"])
def get_single_dataset(user_id, dataset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
       current_app.logger.info(f"GET /datasets/{user_id}/{dataset_id}")
       query = """
                SELECT dataset_id, name, type, user_id
                from Dataset
                WHERE user_id = %s AND dataset_id = %s
                """
       
       cursor.execute(query, (user_id, dataset_id))
       dataset = cursor.fetchone()

       if not dataset:
           return jsonify({"error":"Dataset not found"}), 404
       return jsonify(dataset), 200
    
    except Error as e:
        current_app.logger.error(f"Database error in get_single_dataset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# POST STUFF


# POST /Datasets/<user_id>
# posts a specific dataset for a given user
@dataset_routes.route("/<int:user_id>", methods=["POST"])
def post_dataset(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        query = """
                INSERT INTO Dataset 
                (name, type, user_id)
                VALUES (%s, %s, %s)
                """
        cursor.execute(query, (data["name"], data["type"], user_id))
        get_db().commit()
        new_id = cursor.lastrowid
        return jsonify({"id": new_id, "name": data["name"], "type": data["type"], "user_id": user_id}), 201
    except Error as e:
        current_app.logger.error(f"Database error in post_dataset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# PUT STUFF

# PUT /Datasets/<user_id>/<id>
# edits a specific dataset given whatever parameters are inputted
@dataset_routes.route("/<int:user_id>/<int:dataset_id>", methods=["PUT"])
def put_dataset(user_id, dataset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        query = """
                UPDATE Dataset
                SET name = %s,
                    type = %s
                WHERE user_id = %s AND dataset_id = %s
                """
        cursor.execute(query, (data["name"], data["type"], user_id, dataset_id))
        get_db().commit()
        return jsonify({"id": dataset_id, "name": data["name"], "type": data["type"], "user_id": user_id}), 200
    except Error as e:
        current_app.logger.error(f"Database error in put_dataset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE ROUTE

# DELETE /Datasets/<user_id>/<dataset_id>
# will delete a specific dataset from datasets
@dataset_routes.route("/<int:user_id>/<int:dataset_id>", methods=["DELETE"])
def delete_single_dataset(user_id, dataset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
                DELETE FROM Dataset
                WHERE user_id = %s AND dataset_id = %s
                """
        cursor.execute(query, (user_id, dataset_id))
        get_db().commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_single_dataset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /Datasets/<user_id>
# will delete a specific set datasets for a given user
@dataset_routes.route("/<int:user_id>", methods=["DELETE"])
def delete_users_dataset(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
                DELETE FROM Dataset
                WHERE user_id = %s
                """
        cursor.execute(query, (user_id,))
        get_db().commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_users_dataset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


