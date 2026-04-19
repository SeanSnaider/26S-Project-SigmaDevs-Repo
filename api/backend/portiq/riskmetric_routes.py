from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

riskmetric_routes = Blueprint("riskmetric_routes", __name__)
