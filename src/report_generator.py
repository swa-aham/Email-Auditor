from jinja2 import Environment, FileSystemLoader
import json

class ReportGenerator:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_json_report(self, audit_results):
        report = {
            "thread_score": audit_results["thread_score"],
            "feedback": audit_results["feedback"],
            "summary": audit_results["summary"]
        }
        return json.dumps(report, indent=4)

    def generate_html_report(self, audit_results):
        template = self.env.get_template('report.html')
        return template.render(audit_results=audit_results)