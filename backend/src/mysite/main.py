from flask import Flask, request, jsonify
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
import mysql.connector
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app, resources={r"/api/*": {"origins": "*"}})
#CORS(app)

db_config = {
    "host": "host.docker.internal",
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

@app.route("/api/data", methods=["OPTIONS"])
def options():
    response = jsonify({"message": "CORS preflight successful"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


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

asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    
    # Uruchomienie ASGI (np. z użyciem Uvicorn)
    import uvicorn
    uvicorn.run(asgi_app, host="0.0.0.0", port=5000)
    #app.run(host="0.0.0.0", port=5000)
