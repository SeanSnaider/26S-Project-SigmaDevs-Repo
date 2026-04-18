from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Portfolio routes
portfolio_routes = Blueprint("portfolio_routes", __name__)


# GET /portfolios
# Return all portfolios
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
# Returns one portfolio with current value and P&L summary
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
