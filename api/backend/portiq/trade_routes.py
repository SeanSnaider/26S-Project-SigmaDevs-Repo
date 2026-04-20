from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for trade routes
trade_routes = Blueprint("trade_routes", __name__)


# GET /trades
# Return all trades
@trade_routes.route("/", methods=["GET"])
def get_all_trades():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /trades')
        query = """
                SELECT *
                from Trade
                """
        cursor.execute(query)
        trades = cursor.fetchall()
        return jsonify(trades), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_trades: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /trades/<id>
# Return all trades
@trade_routes.route("/<int:trade_id>", methods=["GET"])
def get_trade(trade_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /trades/{trade_id}')
        query = """
                SELECT *
                from Trade
                where trade_id = %s
                """
        cursor.execute(query, (trade_id,))
        trade = cursor.fetchone()
        return jsonify(trade), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_trade: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# POST /trades/<id>
# Update a trade
@trade_routes.route("/", methods=["POST"])
def create_trade():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'POST /trades')
        data = request.get_json()
        query = """
                INSERT INTO Trade
                (trade_type, trade_date, quantity, price, trade_id, trade_asset)
                VALUES (%s,NOW(),%s,%s,%s,%s)
                """
        cursor.execute(query, (
                    data["trade_type"],
                    data["quantity"],
                    data["price"],
                    data["trade_id"],
                    data["trade_asset"]
                       ))
        get_db().commit()
        return jsonify({"message": "Trade Created"}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_trade: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# PUT /trades
# Create a new trade
@trade_routes.route("/<int:trade_id>", methods=["PUT"])
def update_trade(trade_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'PUT /trades/{trade_id}')
        data = request.get_json()
        query = """
                UPDATE Trade
                SET trade_type=%s,
                trade_date=NOW(),
                quantity=%s,
                price=%s,
                trade_asset=%s
                where trade_id = %s
                """
        cursor.execute(query, (
                    data["trade_type"],
                    data["quantity"],
                    data["price"],
                    data["trade_asset"],
                    trade_id
                ))
        get_db().commit()
        return jsonify({"message": "Trade Updated"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_trade: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /trades/<id>
# Delete a trade
@trade_routes.route("/<int:trade_id>", methods=["DELETE"])
def delete_trade(trade_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /trades/{trade_id}')
        query = """
               DELETE from Trade
               where trade_id = %s
                """
        cursor.execute(query, ( trade_id,
                       ))
        get_db().commit()
        return jsonify({"message": "Trade Deleted"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_trade: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
