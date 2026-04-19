from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error
import os

users = Blueprint("users", __name__)


# Get all users and their assigned roles.
# Returns a list of usernames paired with their role name.
# Example: GET /user/users
@users.route("/users", methods=["GET"])
def get_all_users_role():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT u.username as 'usernames', r.name as 'role names', r.RoleID as 'role id'
               FROM Users AS u
               JOIN Role AS r ON u.userID = r.user_id""")
        user_roles_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(user_roles_list)} users with their roles')

        if not user_roles_list:
            return jsonify({"error": "No users or roles found"}), 404
        return jsonify(user_roles_list), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Encrypt all users' passwordHash and birth_date fields using AES encryption.
# Should be called once after mock data is generated.
# Example: PUT /user/users
@users.route("/users", methods=["PUT"])
def update_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        
        # Encryption key loaded from environment — used for AES encrypt/decrypt operations.
        key = os.getenv("ENCRYPTION_KEY")

        cursor.execute(
            """UPDATE Users
               SET passwordHash = AES_ENCRYPT(passwordHash, %s),
                   is_encrypted = true
               WHERE is_encrypted = false""",
            (key,))

        get_db().commit()
        return jsonify({"message": "Users encrypted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get decrypted passwordHash and birth_date for a specific user by ID.
# Example: GET /user/users/1
@users.route("/users/<int:user_id>", methods=["GET"])
def get_decrypt_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        
        # Encryption key loaded from environment — used for AES encrypt/decrypt operations.
        key = os.getenv("ENCRYPTION_KEY")
        
        cursor.execute(
            """SELECT AES_DECRYPT(Users.passwordHash, %s) AS passwordHash,
                      AES_DECRYPT(Users.birth_date, %s) AS birth_date
               FROM Users
               WHERE Users.userID = %s""",
            (key, key, user_id))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a user by ID.
# Example: DELETE /user/users/1
@users.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """DELETE FROM Users
               WHERE Users.userID = %s""",
            (user_id,))

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        get_db().commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
