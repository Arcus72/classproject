from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(_name_)

# Dane do połączenia z bazą MySQL pobrane z docker-compose
db_config = {
    "host": os.getenv("MYSQL_HOST", "mysql"),
    "user": os.getenv("MYSQL_USER", "user"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "database": os.getenv("MYSQL_DATABASE", "mydatabase")
}

# Funkcja do nawiązywania połączenia
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Endpoint dodający dane do bazy
@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    message = data.get("message", "")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"response": f"Dodano do bazy: {message}"}), 201

# Endpoint pobierający dane z bazy
@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM messages")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({"messages": [msg[0] for msg in messages]})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)
