from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Blueprint for asset routes
asset_routes = Blueprint("asset_routes", __name__)


# GET /assets
# Return all assets
@asset_routes.route("/", methods=["GET"])
def get_all_assets():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /assets')
        query = """
                SELECT asset_id, ticker, asset_name, asset_type, exchange, total_market
                from Asset
                """
        cursor.execute(query)
        assets = cursor.fetchall()
        return jsonify(assets), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_assets: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /assets/<asset_id>
# Return one asset
@asset_routes.route("/<int:asset_id>", methods=["GET"])
def get_asset(asset_id):
    cursor = get_db().cursor(dictionary=True)
    try:
       current_app.logger.info(f"GET /assets/{asset_id}")
       query = """
                SELECT asset_id, ticker, asset_name, asset_type, exchange, total_market
                from Asset
                WHERE asset_id = %s
                """
       
       cursor.execute(query, (asset_id,))
       asset = cursor.fetchone()

       if not asset:
           return jsonify({"error":"Asset not found"}), 404
       return jsonify(asset), 200
    
    except Error as e:
        current_app.logger.error(f"Database error in get_asset: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()