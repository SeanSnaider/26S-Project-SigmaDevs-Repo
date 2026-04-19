from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

asset_routes = Blueprint("asset_routes", __name__)
