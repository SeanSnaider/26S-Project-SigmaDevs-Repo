from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for visualization routes
visualization_routes = Blueprint("visualization_routes", __name__)


# GET /Visualizations
# Return all visualizations across all users
@visualization_routes.route("/", methods=["GET"])
def get_all_visualizations():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /Visualizations')
        query = """
                SELECT visualization_id, title, chart_type, VizDataSet
                FROM Visualization
                """
        cursor.execute(query)
        visualizations = cursor.fetchall()
        return jsonify(visualizations), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_visualizations: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /Visualizations/<user_id>
# Return all visualizations for a specific user (joined through Dataset)
@visualization_routes.route("/<int:user_id>", methods=["GET"])
def get_user_visualizations(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /Visualizations/{user_id}')
        query = """
                SELECT v.visualization_id, v.title, v.chart_type, v.VizDataSet
                FROM Visualization v
                JOIN Dataset d ON v.VizDataSet = d.dataset_id
                WHERE d.user_id = %s
                """
        cursor.execute(query, (user_id,))
        visualizations = cursor.fetchall()
        return jsonify(visualizations), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_user_visualizations: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /Visualizations/<user_id>/<visualization_id>
# Return a specific visualization for a user
@visualization_routes.route("/<int:user_id>/<int:visualization_id>", methods=["GET"])
def get_visualization(user_id, visualization_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /Visualizations/{user_id}/{visualization_id}')
        query = """
                SELECT v.visualization_id, v.title, v.chart_type, v.VizDataSet
                FROM Visualization v
                JOIN Dataset d ON v.VizDataSet = d.dataset_id
                WHERE d.user_id = %s AND v.visualization_id = %s
                """
        cursor.execute(query, (user_id, visualization_id))
        visualization = cursor.fetchone()
        if not visualization:
            return jsonify({"error": "Visualization not found"}), 404
        return jsonify(visualization), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_visualization: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /Visualizations/<user_id>
# Create a new visualization for a user
@visualization_routes.route("/<int:user_id>", methods=["POST"])
def create_visualization(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'POST /Visualizations/{user_id}')
        data = request.get_json()
        query = """
                INSERT INTO Visualization (title, chart_type, VizDataSet)
                VALUES (%s, %s, %s)
                """
        cursor.execute(query, (data["title"], data["chart_type"], data["VizDataSet"]))
        get_db().commit()
        new_id = cursor.lastrowid
        return jsonify({"visualization_id": new_id, "title": data["title"], "chart_type": data["chart_type"], "VizDataSet": data["VizDataSet"]}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_visualization: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /Visualizations/<user_id>/<visualization_id>
# Edit a specific visualization
@visualization_routes.route("/<int:user_id>/<int:visualization_id>", methods=["PUT"])
def update_visualization(user_id, visualization_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'PUT /Visualizations/{user_id}/{visualization_id}')
        data = request.get_json()
        query = """
                UPDATE Visualization
                SET title = %s,
                    chart_type = %s,
                    VizDataSet = %s
                WHERE visualization_id = %s
                """
        cursor.execute(query, (data["title"], data["chart_type"], data["VizDataSet"], visualization_id))
        get_db().commit()
        return jsonify({"visualization_id": visualization_id, "title": data["title"], "chart_type": data["chart_type"], "VizDataSet": data["VizDataSet"]}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_visualization: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /Visualizations/<user_id>/<visualization_id>
# Delete a specific visualization
@visualization_routes.route("/<int:user_id>/<int:visualization_id>", methods=["DELETE"])
def delete_visualization(user_id, visualization_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /Visualizations/{user_id}/{visualization_id}')
        query = """
                DELETE FROM Visualization
                WHERE visualization_id = %s
                """
        cursor.execute(query, (visualization_id,))
        get_db().commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_visualization: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /Visualizations/<user_id>
# Delete all visualizations for a user (via Dataset subquery)
@visualization_routes.route("/<int:user_id>", methods=["DELETE"])
def delete_user_visualizations(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /Visualizations/{user_id}')
        query = """
                DELETE FROM Visualization
                WHERE VizDataSet IN (
                    SELECT dataset_id FROM Dataset WHERE user_id = %s
                )
                """
        cursor.execute(query, (user_id,))
        get_db().commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_user_visualizations: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
