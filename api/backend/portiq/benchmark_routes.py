from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# A Blueprint for Benchmark routes
benchmark_routes = Blueprint("benchmark_routes", __name__)


# GET /benchmarks
# Return all benchmarks
@benchmark_routes.route("/", methods=["GET"])
def get_all_benchmarks():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /benchmarks')

        query = """
                SELECT benchmark_id, benchmark_name, ticker, current_value, sector
                From Benchmark
                """
        cursor.execute(query)
        benchmarks = cursor.fetchall()
        return jsonify(benchmarks), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_benchmarks: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /benchmarks/<benchmark_id>
# Returns one benchmark
@benchmark_routes.route("/<int:benchmark_id>", methods=["GET"])
def get_benchmark(benchmark_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /benchmarks/{benchmark_id}")

        query = """
                Select *
                from Benchmark
                where benchmark_id = %s
                """
        cursor.execute(query, (benchmark_id,))
        benchmark = cursor.fetchone()
        if not benchmark:
            return jsonify({"error": "Benchmark not found"}), 404
        return jsonify(benchmark), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_benchmark: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
