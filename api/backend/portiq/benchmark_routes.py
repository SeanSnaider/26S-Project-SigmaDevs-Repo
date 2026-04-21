from flask import Blueprint, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Benchmark routes
benchmark_routes = Blueprint("benchmark_routes", __name__)


# GETs all benchmarks for that strategy
@benchmark_routes.route("/<int:strategy_id>",methods=["GET"])
def GetAllBenchmarks(strategy_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET all benchmarks for strategy")
    cursor.execute("SELECT * FROM Benchmark WHERE strat_bench = %s",(strategy_id,))
    benchmarks = cursor.fetchall()
    current_app.logger.info(f"Succesfully got benchmarks for strategy")
    return jsonify(benchmarks), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting all benchmarks for strategy {strategy_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# GETs one specific benchmark
@benchmark_routes.route("/<int:strategy_id>/<int:benchmark_id>",methods=["GET"])
def GetBenchmark(strategy_id, benchmark_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET one benchmark from strategy")
    cursor.execute(
      "SELECT * FROM Benchmark WHERE strat_bench = %s AND benchmark_id = %s",
      (strategy_id, benchmark_id),
    )
    benchmark = cursor.fetchone()

    if not benchmark:
      return jsonify({"error": "Benchmark not found"}), 404

    current_app.logger.info("Got the benchmark")
    return jsonify(benchmark), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting benchmark")
    return jsonify(str(e)), 500
  finally:
    cursor.close()
