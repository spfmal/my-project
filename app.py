from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # CORS 허용

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"  # SQLite 파일 상대경로
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # SQLAlchemy 초기화

# Todo 모델 정의
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 데이터베이스 생성
with app.app_context():
    db.create_all()

# ✅ 할 일 목록 조회 API (GET)
@app.route("/todo", methods=["GET"])
def get_todos():
    todos = Todo.query.all()  # 모든 할 일 가져오기
    result = [
        {"id": todo.id, "title": todo.title, "completed": todo.completed, "created_at": todo.created_at}
        for todo in todos
    ]
    return jsonify(result), 200

@app.route("/todo", methods=["POST"])  # ✅ POST 요청 허용
def add_todo():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_todo = Todo(title=data["title"])
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"message": "Todo added", "id": new_todo.id}), 201

# ✅ 기본 홈 화면 (테스트용)
@app.route("/")
def home():
    return "Hello, Todo API!"

# ✅ Flask 실행
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)