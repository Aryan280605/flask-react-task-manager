from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/tasks")
def get_tasks():
    return jsonify([{"id": 1, "title": "Test task"}])

if __name__ == "_main_":
    app.run(port=5000)