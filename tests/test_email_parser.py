import unittest
from src.email_parser import parse_eml

class TestEmailParser(unittest.TestCase):

    def setUp(self):
        self.valid_eml_path = 'tests/example_emails/sample1.eml'
        self.invalid_eml_path = 'tests/example_emails/invalid.eml'  # Assuming this file does not exist

    def test_parse_valid_eml(self):
        email_data = parse_eml(self.valid_eml_path)
        self.assertIsNotNone(email_data)
        self.assertIn('subject', email_data)
        self.assertIn('sender', email_data)
        self.assertIn('recipient', email_data)
        self.assertIn('date', email_data)
        self.assertIn('body', email_data)

    def test_parse_invalid_eml(self):
        with self.assertRaises(FileNotFoundError):
            parse_eml(self.invalid_eml_path)

    def test_email_body_content(self):
        email_data = parse_eml(self.valid_eml_path)
        self.assertTrue(len(email_data['body']) > 0)

if __name__ == '__main__':
    unittest.main()