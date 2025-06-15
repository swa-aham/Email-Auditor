import unittest
from src.rules_engine import RuleEngine

class TestRulesEngine(unittest.TestCase):

    def setUp(self):
        self.engine = RuleEngine()
        self.test_email_content = {
            "subject": "Test Email",
            "sender": "test@example.com",
            "recipient": "recipient@example.com",
            "date": "2023-10-01T12:00:00Z",
            "body": "Dear Recipient,\n\nThis is a test email.\n\nBest regards,\nSender",
            "attachments": []
        }

    def test_professional_greeting(self):
        rule = self.engine.get_rule("Greeting")
        result = rule.apply(self.test_email_content["body"])
        self.assertEqual(result["status"], "pass")
        self.assertGreater(result["score"], 0)

    def test_timely_response(self):
        rule = self.engine.get_rule("Timeliness")
        result = rule.apply(self.test_email_content)
        self.assertEqual(result["status"], "pass")
        self.assertGreater(result["score"], 0)

    def test_clarity_and_grammar(self):
        rule = self.engine.get_rule("Clarity")
        result = rule.apply(self.test_email_content["body"])
        self.assertEqual(result["status"], "pass")
        self.assertGreater(result["score"], 0)

if __name__ == '__main__':
    unittest.main()