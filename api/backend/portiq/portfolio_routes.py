from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

portfolio_routes = Blueprint("portfolio_routes", __name__)
