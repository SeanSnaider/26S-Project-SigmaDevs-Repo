from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

roles = Blueprint("roles", __name__)


# Get all permissions associated with a specific role by role ID.
# Example: GET /role/roles/1
@roles.route("/roles/<int:role_id>", methods=["GET"])
def get_role_perms(role_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT r.RoleID, p.Can_Read, p.Can_Write, p.Can_CREATE, p.table_id
               FROM Role AS r
               JOIN Permission AS p ON r.RoleID = p.role_id
               WHERE r.RoleID = %s""",
            (role_id,))
        perms = cursor.fetchall()

        current_app.logger.info(f'Retrieved permissions for role {role_id}')

        if not perms:
            return jsonify({"error": "Role not found"}), 404
        return jsonify(perms), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new role and assign it to a user.
# Required fields: name, RoleID, user_id
# Example: POST /role/roles
@roles.route("/roles", methods=["POST"])
def create_role():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["name", "RoleID", "user_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor.execute(
            """INSERT INTO Role (name, RoleID, user_id)
               VALUES (%s, %s, %s)""",
            (data["name"], data["RoleID"], data["user_id"]))

        get_db().commit()
        return jsonify({"message": "Role created successfully", "role_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a permission and associate it with a role.
# Required fields: permission_id, table_id, Can_Read, Can_Write, Can_CREATE
# Example: POST /role/roles/1/permissions
@roles.route("/roles/<int:role_id>/permissions", methods=["POST"])
def create_permission(role_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["permission_id", "table_id", "Can_Read", "Can_Write", "Can_CREATE"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Verify the role exists before inserting the permission
        cursor.execute("SELECT RoleID FROM Role WHERE RoleID = %s", (role_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Role not found"}), 404

        cursor.execute(
            """INSERT INTO Permission (permission_id, role_id, table_id, Can_Read, Can_Write, Can_CREATE)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (data["permission_id"], role_id, data["table_id"],
             data["Can_Read"], data["Can_Write"], data["Can_CREATE"]))

        get_db().commit()
        return jsonify({"message": "Permission created successfully", "permission_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a role by ID.
# Example: DELETE /role/roles/1
@roles.route("/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """DELETE FROM Role
               WHERE RoleID = %s""",
            (role_id,))

        if cursor.rowcount == 0:
            return jsonify({"error": "Role not found"}), 404

        get_db().commit()
        return jsonify({"message": "Role deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
