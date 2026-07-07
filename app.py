import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import malaria_rag

# Get the absolute path to the frontend build directory
frontend_path = os.path.join(os.path.dirname(__file__), 'frontend', 'build')

app = Flask(__name__, static_folder=frontend_path, static_url_path='')
CORS(app)

# Configuration
DEBUG = os.getenv("FLASK_ENV") == "development"
PORT = int(os.getenv("PORT", 5000))


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for deployment services."""
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    """Main chat endpoint for RAG queries."""
    payload = request.get_json(force=True)
    question = payload.get("question")
    if not question:
        return jsonify({"error": "question is required"}), 400

    result = malaria_rag.answer_and_sources(question)
    return jsonify(result)


@app.route("/", methods=["GET"])
def serve_index():
    """Serve the React frontend for browser requests and JSON metadata for API clients."""
    if request.accept_mimetypes.accept_html and os.path.exists(os.path.join(frontend_path, 'index.html')):
        return send_from_directory(frontend_path, 'index.html')
    return jsonify({
        "message": "MalariaAI RAG - React frontend not built yet",
        "api_endpoints": {
            "health": "GET /health",
            "chat": "POST /chat {question}"
        }
    })


@app.route("/<path:path>", methods=["GET"])
def serve_static(path):
    """Serve React frontend static files when requested by a browser."""
    filepath = os.path.join(frontend_path, path)
    if os.path.isfile(filepath):
        return send_from_directory(frontend_path, path)
    if request.accept_mimetypes.accept_html and os.path.exists(os.path.join(frontend_path, 'index.html')):
        return send_from_directory(frontend_path, 'index.html')
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=DEBUG
    )
