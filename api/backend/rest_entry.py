from flask import Flask
from dotenv import load_dotenv
import os
import logging

from backend.db_connection import init_app as init_db
from backend.simple.simple_routes import simple_routes
from backend.portiq.asset_routes import asset_routes
from backend.portiq.benchmark_routes import benchmark_routes
from backend.portiq.portfolio_routes import portfolio_routes
from backend.portiq.riskmetric_routes import riskmetric_routes
from backend.portiq.strategy_routes import strategy_routes
from backend.portiq.trade_routes import trade_routes

def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    # Load environment variables from the .env file so they are
    # accessible via os.getenv() below.
    load_dotenv()

    # Secret key used by Flask for securely signing session cookies.
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Database connection settings — values come from the .env file.
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME").strip()

    # Register the cleanup hook for the database connection.
    app.logger.info("create_app(): initializing database connection")
    init_db(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each.
    app.logger.info("create_app(): registering blueprints")
    app.register_blueprint(simple_routes)
    app.register_blueprint(asset_routes, url_prefix="/assets")
    app.register_blueprint(benchmark_routes, url_prefix="/benchmarks")
    app.register_blueprint(portfolio_routes, url_prefix="/portfolios")
    app.register_blueprint(riskmetric_routes, url_prefix="/riskmetrics")
    app.register_blueprint(strategy_routes, url_prefix="/strategies")
    app.register_blueprint(trade_routes, url_prefix="/trades")
    
    return app
