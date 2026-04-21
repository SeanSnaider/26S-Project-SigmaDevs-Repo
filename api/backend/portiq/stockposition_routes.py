from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for StockPosition routes
stockposition_routes = Blueprint("stockposition_routes", __name__)


# GETs all positions for that portifolio
@stockposition_routes.route("/<int:portifolio_id>",methods=["GET"])
def GetAllStockPositions(portifolio_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET all positions for portifolio")
    cursor.execute("SELECT * FROM StockPosition WHERE port_id = %s",(portifolio_id,))
    positions = cursor.fetchall()
    current_app.logger.info(f"Succesfully got positions for portifolio")
    return jsonify(positions), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting all positions for portifolio {portifolio_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# GETs one specific position
@stockposition_routes.route("/<int:portifolio_id>/<int:position_id>",methods=["GET"])
def GetStockPosition(portifolio_id, position_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET one position from portifolio")
    cursor.execute(
      "SELECT * FROM StockPosition WHERE port_id = %s AND position_id = %s",
      (portifolio_id, position_id),
    )
    position = cursor.fetchone()

    if not position:
      return jsonify({"error": "Stock position not found"}), 404

    current_app.logger.info("Got the position")
    return jsonify(position), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting position")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# POST, create a new position for that portifolio and requrires: avg_cost, unrealized_PNL, price_target, acquired_date, market_value, qty_held
@stockposition_routes.route("/<int:portifolio_id>/<int:position_id>",methods=["POST"])
def CreateStockPosition(portifolio_id, position_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"POST position")
    data = request.get_json()

    required_fields = ["avg_cost","unrealized_PNL","price_target","acquired_date","market_value","qty_held"]
    for field in required_fields:
      if field not in data:
        return jsonify({"error": f"Missing required field: {field}"}), 400

    query = """
      INSERT INTO StockPosition (position_id, port_id, avg_cost, unrealized_PNL, price_target, acquired_date, market_value, qty_held)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query,(
      position_id,
      portifolio_id,
      data["avg_cost"],
      data["unrealized_PNL"],
      data["price_target"],
      data["acquired_date"],
      data["market_value"],
      data["qty_held"],
    ))
    get_db().commit()

    current_app.logger.info(f"Created position")
    return jsonify({"message": "Stock position created successfully"}), 201
  except Error as e:
    current_app.logger.error(f"The error {e} occured while creating position")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# PUT update the position of the portifolio
@stockposition_routes.route("/<int:portifolio_id>/<int:position_id>",methods=["PUT"])
def UpdateStockPosition(portifolio_id, position_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"PUT position")
    data = request.get_json()

    cursor.execute(
      "SELECT position_id FROM StockPosition WHERE port_id = %s AND position_id = %s",
      (portifolio_id, position_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Stock position not found"}), 404

    allowed_fields = ["avg_cost","unrealized_PNL","price_target","acquired_date","market_value","qty_held"]
    update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
    params = [data[f] for f in allowed_fields if f in data]

    if not update_fields:
      return jsonify({"error": "No valid fields to update"}), 400

    params.extend([portifolio_id, position_id])
    query = f"UPDATE StockPosition SET {', '.join(update_fields)} WHERE port_id = %s AND position_id = %s"
    cursor.execute(query,params)
    get_db().commit()

    current_app.logger.info(f"Updated position")
    return jsonify({"message": "Stock position updated successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while updating position")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# DELETE hard delete a position of a portiflio
@stockposition_routes.route("/<int:portifolio_id>/<int:position_id>",methods=["DELETE"])
def DeleteStockPosition(portifolio_id, position_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"DELETE position")

    cursor.execute(
      "SELECT position_id FROM StockPosition WHERE port_id = %s AND position_id = %s",
      (portifolio_id, position_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Stock position not found"}), 404

    cursor.execute(
      "DELETE FROM StockPosition WHERE port_id = %s AND position_id = %s",
      (portifolio_id, position_id),
    )
    get_db().commit()

    current_app.logger.info(f"Deleted position")
    return jsonify({"message": "Stock position deleted successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while deleting position")
    return jsonify(str(e)), 500
  finally:
    cursor.close()
