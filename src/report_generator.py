from jinja2 import Environment, FileSystemLoader
import json
import os

class ReportGenerator:
    def __init__(self, template_dir):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_json_report(self, audit_results):
        """Generate JSON format report"""
        report = {
            "thread_score": audit_results.get("thread_score", 0),
            "feedback": audit_results.get("feedback", []),
            "summary": audit_results.get("summary", {})
        }
        return json.dumps(report, indent=4, default=str)

    def generate_html_report(self, audit_results):
        """Generate HTML format report"""
        try:
            template = self.env.get_template('report.html')
            
            # Prepare data for template
            template_data = {
                'thread_score': audit_results.get('thread_score', 0),
                'feedback': audit_results.get('feedback', []),
                'strengths': audit_results.get('summary', {}).get('strengths', []),
                'improvements': audit_results.get('summary', {}).get('improvements', [])
            }
            
            return template.render(**template_data)
        except Exception as e:
            return f"<html><body><h1>Error generating report</h1><p>{str(e)}</p></body></html>"

    def generate_text_report(self, audit_results):
        """Generate plain text format report"""
        report_lines = []
        report_lines.append("EMAIL AUDIT REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Overall Score: {audit_results.get('thread_score', 0):.2f}%")
        report_lines.append("")
        
        # Add summary
        summary = audit_results.get('summary', {})
        strengths = summary.get('strengths', [])
        improvements = summary.get('improvements', [])
        
        if strengths:
            report_lines.append("STRENGTHS:")
            for strength in strengths:
                report_lines.append(f"  ✓ {strength}")
            report_lines.append("")
        
        if improvements:
            report_lines.append("AREAS FOR IMPROVEMENT:")
            for improvement in improvements:
                report_lines.append(f"  ✗ {improvement}")
            report_lines.append("")
        
        # Add detailed feedback
        feedback = audit_results.get('feedback', [])
        for i, email_feedback in enumerate(feedback, 1):
            report_lines.append(f"EMAIL {i} DETAILS:")
            report_lines.append(f"Subject: {email_feedback.get('email_subject', 'N/A')}")
            report_lines.append(f"Sender: {email_feedback.get('email_sender', 'N/A')}")
            report_lines.append("")
            
            rules = email_feedback.get('rules', [])
            for rule in rules:
                status_icon = "✓" if rule['status'] == 'pass' else "✗" if rule['status'] == 'fail' else "~"
                report_lines.append(f"  {status_icon} {rule['rule']}: {rule['score']}/100")
                report_lines.append(f"    {rule['justification']}")
            report_lines.append("")
        
        return "\n".join(report_lines)