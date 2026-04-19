from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Asset routes
asset_routes = Blueprint("asset_routes", __name__)


# GETs all assets for that position
@asset_routes.route("/<int:position_id>",methods=["GET"])
def GetAllAssets(position_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET all assets for position")
    cursor.execute("SELECT * FROM Asset WHERE pos_id = %s",(position_id,))
    assets = cursor.fetchall()
    current_app.logger.info(f"Succesfully got assets for position")
    return jsonify(assets), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting all assets for position {position_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# GETs one specific asset
@asset_routes.route("/<int:position_id>/<int:asset_id>",methods=["GET"])
def GetAsset(position_id, asset_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET one asset from position")
    cursor.execute(
      "SELECT * FROM Asset WHERE pos_id = %s AND asset_id = %s",
      (position_id, asset_id),
    )
    asset = cursor.fetchone()

    if not asset:
      return jsonify({"error": "Asset not found"}), 404

    current_app.logger.info("Got the asset")
    return jsonify(asset), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting asset")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# POST, create a new asset for that position and requrires: asset_type, ticker, total_market, asset_name, exchange
@asset_routes.route("/<int:position_id>/<int:asset_id>",methods=["POST"])
def CreateAsset(position_id, asset_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"POST asset")
    data = request.get_json()

    required_fields = ["asset_type","ticker","total_market","asset_name","exchange"]
    for field in required_fields:
      if field not in data:
        return jsonify({"error": f"Missing required field: {field}"}), 400

    query = """
      INSERT INTO Asset (asset_id, pos_id, asset_type, ticker, total_market, asset_name, exchange)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query,(
      asset_id,
      position_id,
      data["asset_type"],
      data["ticker"],
      data["total_market"],
      data["asset_name"],
      data["exchange"],
    ))
    get_db().commit()

    current_app.logger.info(f"Created asset")
    return jsonify({"message": "Asset created successfully"}), 201
  except Error as e:
    current_app.logger.error(f"The error {e} occured while creating asset")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# PUT update the asset of the position
@asset_routes.route("/<int:position_id>/<int:asset_id>",methods=["PUT"])
def UpdateAsset(position_id, asset_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"PUT asset")
    data = request.get_json()

    cursor.execute(
      "SELECT asset_id FROM Asset WHERE pos_id = %s AND asset_id = %s",
      (position_id, asset_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Asset not found"}), 404

    allowed_fields = ["asset_type","ticker","total_market","asset_name","exchange"]
    update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
    params = [data[f] for f in allowed_fields if f in data]

    if not update_fields:
      return jsonify({"error": "No valid fields to update"}), 400

    params.extend([position_id, asset_id])
    query = f"UPDATE Asset SET {', '.join(update_fields)} WHERE pos_id = %s AND asset_id = %s"
    cursor.execute(query,params)
    get_db().commit()

    current_app.logger.info(f"Updated asset")
    return jsonify({"message": "Asset updated successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while updating asset")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# DELETE hard delete an asset of a position
@asset_routes.route("/<int:position_id>/<int:asset_id>",methods=["DELETE"])
def DeleteAsset(position_id, asset_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"DELETE asset")

    cursor.execute(
      "SELECT asset_id FROM Asset WHERE pos_id = %s AND asset_id = %s",
      (position_id, asset_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Asset not found"}), 404

    cursor.execute(
      "DELETE FROM Asset WHERE pos_id = %s AND asset_id = %s",
      (position_id, asset_id),
    )
    get_db().commit()

    current_app.logger.info(f"Deleted asset")
    return jsonify({"message": "Asset deleted successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while deleting asset")
    return jsonify(str(e)), 500
  finally:
    cursor.close()
