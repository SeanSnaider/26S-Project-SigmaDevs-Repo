from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

portfolio_routes = Blueprint("portfolio_routes", __name__)


# GETs all portifolios for that user
@portfolio_routes.route("/user/<int:user_id>",methods=["GET"])
def GetAllPortifolios(user_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET portifolios for user")
    cursor.execute("SELECT * FROM Portfolio WHERE user_id = %s",(user_id,))
    portifolios = cursor.fetchall()
    current_app.logger.info(f"Got {len(portifolios)} portifolios for user")
    return jsonify(portifolios), 200
  except Error as e:
    current_app.logger.error(f"An error {e} occured while getting all portifolios for user")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# GETs one specific portifolio
@portfolio_routes.route("/user/<int:user_id>/<int:portifolio_id>",methods=["GET"])
def GetPortifolio(user_id, portifolio_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"Trying GET portifolio")
    cursor.execute(
      "SELECT * FROM Portfolio WHERE user_id = %s AND portfolio_id = %s",
      (user_id, portifolio_id),
    )
    portifolio = cursor.fetchone()

    if not portifolio:
      return jsonify({"error": "Portfolio not found"}), 404

    current_app.logger.info("Got the portifolio")
    return jsonify(portifolio), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting portifolio")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# POST, create a new portifolio for that user and requrires: portfolio_name, created_at, total_value, confidence, currency
@portfolio_routes.route("/user/<int:user_id>/<int:portifolio_id>",methods=["POST"])
def CreatePortifolio(user_id, portifolio_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"Trying POST portifolio")
    data = request.get_json()

    required_fields = ["portfolio_name","created_at","total_value","confidence","currency"]
    for field in required_fields:
      if field not in data:
        return jsonify({"error": f"Missing required field: {field}"}), 400

    query = """
      INSERT INTO Portfolio (portfolio_id, user_id, portfolio_name, created_at, total_value, confidence, currency)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query,(
      portifolio_id,
      user_id,
      data["portfolio_name"],
      data["created_at"],
      data["total_value"],
      data["confidence"],
      data["currency"],
    ))
    get_db().commit()

    current_app.logger.info(f"Created portifolio successfully")
    return jsonify({"message": "Portfolio created successfully", "portfolio_id": portifolio_id}), 201
  except Error as e:
    current_app.logger.error(f"The error {e} occured while creating portifolio")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# PUT update the portifolio of the user
@portfolio_routes.route("/user/<int:user_id>/<int:portifolio_id>",methods=["PUT"])
def UpdatePortifolio(user_id, portifolio_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"PUT portifolio {portifolio_id} for user {user_id}")
    data = request.get_json()

    cursor.execute(
      "SELECT portfolio_id FROM Portfolio WHERE user_id = %s AND portfolio_id = %s",
      (user_id, portifolio_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Portfolio not found"}), 404

    allowed_fields = ["portfolio_name","created_at","total_value","confidence","currency"]
    update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
    params = [data[f] for f in allowed_fields if f in data]

    if not update_fields:
      return jsonify({"error": "No valid fields to update"}), 400

    params.extend([user_id, portifolio_id])
    query = f"UPDATE Portfolio SET {', '.join(update_fields)} WHERE user_id = %s AND portfolio_id = %s"
    cursor.execute(query,params)
    get_db().commit()

    current_app.logger.info(f"Trying Updated portifolio")
    return jsonify({"message": "Portfolio updated successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while updating portifolio")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# DELETE hard delete a portiflio of a user
@portfolio_routes.route("/user/<int:user_id>/<int:portifolio_id>",methods=["DELETE"])
def DeletePortifolio(user_id, portifolio_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"Trying DELETE portifolio")

    cursor.execute(
      "SELECT portfolio_id FROM Portfolio WHERE user_id = %s AND portfolio_id = %s",
      (user_id, portifolio_id),
    )
    if not cursor.fetchone():
      return jsonify({"error": "Portfolio not found"}), 404

    cursor.execute(
      "DELETE FROM Portfolio WHERE user_id = %s AND portfolio_id = %s",
      (user_id, portifolio_id),
    )
    get_db().commit()

    current_app.logger.info(f"Deleted portifolio {portifolio_id} for user {user_id}")
    return jsonify({"message": "Portfolio deleted successfully"}), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while deleting portifolio {portifolio_id} for user {user_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# GET /portfolios
@portfolio_routes.route("/", methods=["GET"])
def get_all_portfolios():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /portfolios')
        query = """
                SELECT portfolio_id, portfolio_name, created_at, total_value, confidence, currency, user_id
                FROM Portfolio
                """
        cursor.execute(query)
        portfolios = cursor.fetchall()
        return jsonify(portfolios), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_portfolios: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /portfolios/<portfolio_id>
@portfolio_routes.route("/<int:portfolio_id>", methods=["GET"])
def get_portfolio(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /portfolios/{portfolio_id}")
        query = """
                SELECT p.portfolio_id, p.portfolio_name, p.total_value, p.confidence, p.currency,
                SUM(pr.daily_PNL) AS total_daily_PNL,
                SUM(pr.cumulative_PNL) AS total_cumulative_PNL
                FROM Portfolio p
                LEFT JOIN Strategy s
                    ON p.portfolio_id = s.port_strat
                LEFT JOIN PerformanceRecord pr
                    ON s.strategy_id = pr.strat_perf
                WHERE p.portfolio_id = %s
                GROUP BY p.portfolio_id, p.portfolio_name, p.total_value, p.confidence, p.currency
                """
        cursor.execute(query, (portfolio_id,))
        portfolio = cursor.fetchone()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        return jsonify(portfolio), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_portfolio: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
