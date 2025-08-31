from flask import Flask, jsonify, request

app = Flask(__name__)

# 簡單的 GET API
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, Flask API!"})

# 帶參數的 API
@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify({"you_sent": data})
