from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "shoplist"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    message = data.get("message", "")
    print(message)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO items (name) VALUES ('{message}')")
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"response": f"Dodano do bazy: {message}"}), 201


@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(messages)


@app.route("/api/data/<string:id>", methods=["DELETE"])
def delete_data(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id= %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"Deleted item: {id}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
