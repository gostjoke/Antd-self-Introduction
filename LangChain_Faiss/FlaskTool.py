from flask import Flask, jsonify, request
from datetime import datetime
from LangChainTool import LangChainTool
app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome to the Flask API!"

# 簡單的 GET API
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, Flask API!"})

# 帶參數的 API
@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify({"you_sent": data})

@app.route("/time", methods=["GET"])
def get_time():

    now = datetime.now().isoformat()
    return jsonify({"current_time": now})

@app.route("/ask/", methods=["GET"])
def ask():
    question = request.args.get("question")
    ans = LangChainTool().Embeddings_FAISS(questions=question, texts=None)
    # ans= LangChainTool().answer_question(questions=question)
    return ans

from flask_socketio import SocketIO, send, emit
# 當有客戶端連線時

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on('connect')
def handle_connect():
    print("有客戶端連線進來了")
    emit('message', {'msg': 'WebSocket 連線成功！'})

# 當有訊息進來時
@socketio.on('message')
def handle_message(data):
    print("收到訊息:", data)
    # 廣播給所有人
    send({'msg': f"伺服器回覆: {data}"}, broadcast=True)

# 自訂事件
@socketio.on('chat')
def handle_chat(data):
    print("聊天室訊息:", data)
    # ans = LangChainTool().Embeddings_FAISS(questions=data, texts=None)
    ans = LangChainTool().answer_question(questions=data)
    emit('chat', {'msg': f"{ans}"}, broadcast=True)

if __name__ == '__main__':
    # 用 eventlet 啟動支援 WebSocket
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)