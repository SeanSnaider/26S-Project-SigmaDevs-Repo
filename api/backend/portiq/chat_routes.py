from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error
import os
import google.generativeai as genai

chat_routes = Blueprint("chat_routes", __name__)


@chat_routes.route("/", methods=["POST"])
def chat():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return jsonify({"error": "API key not configured"}), 503

    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Missing message"}), 400

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT sp.market_value, sp.qty_held, sp.unrealized_PNL, sp.avg_cost,
                   a.ticker, a.asset_name
            FROM StockPosition sp
            LEFT JOIN Asset a ON a.pos_id = sp.position_id
            WHERE sp.port_id = 102
        """)
        positions = cursor.fetchall()
    except Error as e:
        current_app.logger.error(f"DB error in chat: {e}")
        positions = []
    finally:
        cursor.close()

    pos_lines = "\n".join([
        f"- {p.get('asset_name', p.get('ticker', 'Unknown'))}: "
        f"{p['qty_held']} shares, market value ${float(p['market_value']):,.2f}, "
        f"unrealized P&L ${float(p['unrealized_PNL']):,.2f}"
        for p in positions
    ]) or "No positions found."

    system_prompt = (
        f"You are a helpful financial assistant for Jane Doe, a beginner investor. "
        f"Her current portfolio positions are:\n{pos_lines}\n\n"
        f"Answer in simple, beginner-friendly language. Keep responses concise."
    )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(f"{system_prompt}\n\nJane asks: {message}")
        return jsonify({"response": response.text}), 200
    except Exception as e:
        current_app.logger.error(f"Gemini error: {e}")
        return jsonify({"error": str(e)}), 500
