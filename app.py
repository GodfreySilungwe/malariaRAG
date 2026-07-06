from flask import Flask, request, jsonify
from flask_cors import CORS
import malaria_rag

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(force=True)
    question = payload.get("question")
    if not question:
        return jsonify({"error": "question is required"}), 400

    result = malaria_rag.answer_and_sources(question)
    return jsonify(result)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "PraxaApp RAG backend - send POST /chat {question}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
