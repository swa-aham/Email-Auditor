from flask import Blueprint, request, jsonify
import os
import tempfile
from src.email_parser import parse_eml
from src.rules_engine import RulesEngine
from src.report_generator import ReportGenerator
import uuid
import json

routes = Blueprint("routes", __name__)

# In-memory storage for reports (in production, use a database)
reports_storage = {}

def setup_routes(app):
    app.register_blueprint(routes)

def generate_report(email_content, rule_results):
    """Generate audit report from email content and rule results"""
    total_score = 0
    max_possible_score = 0
    
    # Calculate scores
    for result in rule_results:
        total_score += result["score"]
        max_possible_score += 100  # Assuming max score per rule is 100
    
    # Calculate percentage score
    thread_score = (total_score / max_possible_score * 100) if max_possible_score > 0 else 0
    
    # Generate feedback
    feedback = [{
        "email_subject": email_content.get("subject", "No Subject"),
        "email_sender": email_content.get("sender", "Unknown"),
        "rules": rule_results
    }]
    
    # Determine strengths and improvements
    strengths = []
    improvements = []
    
    for result in rule_results:
        if result["status"] == "pass":
            strengths.append(result["rule"])
        else:
            improvements.append(result["rule"])
    
    return {
        "thread_score": round(thread_score, 2),
        "feedback": feedback,
        "summary": {
            "strengths": strengths,
            "improvements": improvements
        }
    }

@routes.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Email Audit Service is running"}), 200

@routes.route("/upload", methods=["POST"])
def upload_email():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".eml"):
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.eml') as temp_file:
                file.save(temp_file.name)
                
                # Parse the email
                email_content = parse_eml(temp_file.name)
                
                # Clean up the temporary file
                os.unlink(temp_file.name)
                
            # Evaluate email with rules engine
            rules_engine = RulesEngine()
            rule_results = rules_engine.evaluate_email(email_content)
            
            # Generate report
            report = generate_report(email_content, rule_results)
            
            # Store report with unique ID
            report_id = str(uuid.uuid4())
            reports_storage[report_id] = report
            
            # Add report ID to response
            response = report.copy()
            response["report_id"] = report_id
            
            return jsonify(response), 200
            
        except Exception as e:
            return jsonify({"error": f"Error processing email: {str(e)}"}), 500

    return jsonify({"error": "Invalid file format. Please upload a .eml file."}), 400

@routes.route("/report/<report_id>", methods=["GET"])
def get_report(report_id):
    if report_id in reports_storage:
        return jsonify(reports_storage[report_id]), 200
    else:
        return jsonify({"error": "Report not found"}), 404

@routes.route("/report/<report_id>/html", methods=["GET"])
def get_html_report(report_id):
    if report_id in reports_storage:
        report_data = reports_storage[report_id]
        
        # Generate HTML report
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        report_generator = ReportGenerator(template_dir)
        html_report = report_generator.generate_html_report(report_data)
        
        return html_report, 200, {'Content-Type': 'text/html'}
    else:
        return jsonify({"error": "Report not found"}), 404

@routes.route("/reports", methods=["GET"])
def list_reports():
    """List all stored reports"""
    report_list = []
    for report_id, report in reports_storage.items():
        report_list.append({
            "report_id": report_id,
            "thread_score": report["thread_score"],
            "timestamp": "N/A"  # In production, add timestamp
        })
    return jsonify({"reports": report_list}), 200