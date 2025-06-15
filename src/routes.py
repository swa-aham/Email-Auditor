from flask import Blueprint, request, jsonify
from src.email_parser import parse_eml
from src.rules_engine import RulesEngine
from src.report_generator import generate_report

routes = Blueprint("routes", __name__)


def setup_routes(app):
    app.register_blueprint(routes)


@routes.route("/upload", methods=["POST"])
def upload_email():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".eml"):
        email_content = parse_eml(file)
        rules_engine = RulesEngine()
        rule_results = rules_engine.evaluate_email(email_content)
        report = generate_report(email_content, rule_results)
        return jsonify(report), 200

    return jsonify({"error": "Invalid file format. Please upload a .eml file."}), 400


@routes.route("/report/<report_id>", methods=["GET"])
def get_report(report_id):
    # TODO: Implement report storage and retrieval
    return jsonify({"error": "Report not found"}), 404
