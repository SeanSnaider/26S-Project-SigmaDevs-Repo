from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for AnalystRating routes
analystrating_routes = Blueprint("analystrating_routes", __name__)


# GETs all ratings for that asset
@analystrating_routes.route("/<int:asset_id>",methods=["GET"])
def GetAllAnalystRatings(asset_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET all ratings for asset")
    cursor.execute("SELECT * FROM AnalystRating WHERE asset_rating = %s",(asset_id,))
    ratings = cursor.fetchall()
    current_app.logger.info(f"Succesfully got ratings for asset")
    return jsonify(ratings), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting all ratings for asset {asset_id}")
    return jsonify(str(e)), 500
  finally:
    cursor.close()


# GETs one specific rating
@analystrating_routes.route("/<int:asset_id>/<int:rate_id>",methods=["GET"])
def GetAnalystRating(asset_id, rate_id):
  cursor = get_db().cursor(dictionary=True)
  try:
    current_app.logger.info(f"GET one rating from asset")
    cursor.execute(
      "SELECT * FROM AnalystRating WHERE asset_rating = %s AND rate_id = %s",
      (asset_id, rate_id),
    )
    rating = cursor.fetchone()

    if not rating:
      return jsonify({"error": "Analyst rating not found"}), 404

    current_app.logger.info("Got the rating")
    return jsonify(rating), 200
  except Error as e:
    current_app.logger.error(f"The error {e} occured while getting rating")
    return jsonify(str(e)), 500
  finally:
    cursor.close()
