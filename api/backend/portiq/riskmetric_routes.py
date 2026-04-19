from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# A Blueprint for RiskMetric routes
riskmetric_routes = Blueprint("riskmetric_routes", __name__)


# GET /riskmetrics
# Return all risk metric records
@riskmetric_routes.route("/", methods=["GET"])
def get_all_risk_metrics():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /riskmetrics')

        query = """
                SELECT riskmetric_id, sharpe_ratio, volatility, drawdown, calculated_at, risk_strat
                from RiskMetric
                """
        cursor.execute(query)
        risk_metrics = cursor.fetchall()
        return jsonify(risk_metrics), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_risk_metrics: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /riskmetrics/<strategy_id>
# Return risk metrics for one strategy
@riskmetric_routes.route("/<int:strategy_id>", methods=["GET"])
def get_risk_metric(strategy_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /riskmetrics/{strategy_id}")

        query = """
                Select riskmetric_id, sharpe_ratio, volatility, drawdown, calculated_at, risk_strat
                from RiskMetric
                WHERE risk_strat = %s 
                """
        cursor.execute(query, (strategy_id,))
        risk_metric = cursor.fetchall()
        if not risk_metric:
            return jsonify({"error": "Risk Metrics not found"}), 404
        return jsonify(risk_metric), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_risk_metric: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
