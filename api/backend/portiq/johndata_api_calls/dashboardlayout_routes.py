from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for dashboard layout routes
dashboardlayout_routes = Blueprint("dashboardlayout_routes", __name__)


# GET /DashboardLayouts
# returns all dashboard layout templates
@dashboardlayout_routes.route("/", methods=["GET"])
def get_all_dashboard_layouts():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /DashboardLayouts')
        query = """
                SELECT layout_id, name, source, layout_dash
                FROM DashboardLayout
                """
        cursor.execute(query)
        layouts = cursor.fetchall()
        return jsonify(layouts), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_dashboard_layouts: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /DashboardLayouts/<layout_id>
# rseturn a specific dashboard layout template
@dashboardlayout_routes.route("/<int:layout_id>", methods=["GET"])
def get_dashboard_layout(layout_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /DashboardLayouts/{layout_id}')
        query = """
                SELECT layout_id, name, source, layout_dash
                FROM DashboardLayout
                WHERE layout_id = %s
                """
        cursor.execute(query, (layout_id,))
        layout = cursor.fetchone()
        if not layout:
            return jsonify({"error": "DashboardLayout not found"}), 404
        return jsonify(layout), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_dashboard_layout: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /DashboardLayouts
# will create a new dashboard layout template
@dashboardlayout_routes.route("/", methods=["POST"])
def create_dashboard_layout():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('POST /DashboardLayouts')
        data = request.get_json()
        query = """
                INSERT INTO DashboardLayout (name, source, layout_dash)
                VALUES (%s, %s, %s)
                """
        cursor.execute(query, (data["name"], data["source"], data["layout_dash"]))
        get_db().commit()
        new_id = cursor.lastrowid
        return jsonify({"layout_id": new_id, "name": data["name"], "source": data["source"], "layout_dash": data["layout_dash"]}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_dashboard_layout: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /DashboardLayouts/<layout_id>
# will edit a specific dashboard layout template
@dashboardlayout_routes.route("/<int:layout_id>", methods=["PUT"])
def update_dashboard_layout(layout_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'PUT /DashboardLayouts/{layout_id}')
        data = request.get_json()
        query = """
                UPDATE DashboardLayout
                SET name = %s,
                    source = %s,
                    layout_dash = %s
                WHERE layout_id = %s
                """
        cursor.execute(query, (data["name"], data["source"], data["layout_dash"], layout_id))
        get_db().commit()
        return jsonify({"layout_id": layout_id, "name": data["name"], "source": data["source"], "layout_dash": data["layout_dash"]}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_dashboard_layout: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /DashboardLayouts/<layout_id>
# will delete a specific dashboard layout template
@dashboardlayout_routes.route("/<int:layout_id>", methods=["DELETE"])
def delete_dashboard_layout(layout_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /DashboardLayouts/{layout_id}')
        query = """
                DELETE FROM DashboardLayout
                WHERE layout_id = %s
                """
        cursor.execute(query, (layout_id,))
        get_db().commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_dashboard_layout: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
