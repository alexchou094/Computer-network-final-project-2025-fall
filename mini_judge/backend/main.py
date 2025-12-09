from flask import Flask, jsonify, request

from .analyzer import analyze_code
from .runner import run_submission


def create_app() -> Flask:
    app = Flask(__name__)

    @app.post("/api/analyze")
    def analyze():
        payload = request.get_json(force=True, silent=True) or {}
        code = payload.get("code", "")
        hints = analyze_code(code)
        return jsonify({"hints": hints})

    @app.post("/api/run")
    def run():
        payload = request.get_json(force=True, silent=True) or {}
        code = payload.get("code", "")
        expected_output = payload.get("expectedOutput")
        result = run_submission(code, expected_output)
        return jsonify(result)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
