import os
from flask import send_from_directory
from flask import Flask, jsonify, request

from .rules import RULES

from .analyzer import analyze_code
from .runner import run_submission


def create_app() -> Flask:
    app = Flask(__name__)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

    @app.post("/api/analyze")
    def analyze():
        payload = request.get_json(force=True, silent=True) or {}
        code = payload.get("code", "")
        enabled_rules = payload.get("enabled_rules")
        if not isinstance(enabled_rules, list):
            enabled_rules = None

        result = analyze_code(code, enabled_rules=enabled_rules)
        return jsonify(result)

    @app.post("/api/run")
    def run():
        payload = request.get_json(force=True, silent=True) or {}
        code = payload.get("code", "")
        expected_output = payload.get("expectedOutput")
        expected_input = payload.get("expectedInput")
        result = run_submission(code, expected_output, expected_input)
        return jsonify(result)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/rules")
    def list_rules():
        return jsonify({
            rule_id: {
                "description": getattr(rule, "RULE_DESCRIPTION", ""),
                "enabled": True
            }
            for rule_id, rule in RULES.items()
        })

    @app.get("/")
    def serve_index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:filename>")
    def serve_static(filename):
        return send_from_directory(FRONTEND_DIR, filename)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
