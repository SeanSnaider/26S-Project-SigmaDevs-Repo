from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

strategy_routes = Blueprint("strategy_routes", __name__)
