# Email Audit Service

## Overview
The Email Audit Service is designed to process email threads in .eml format, evaluate them for compliance using a dynamic set of rules, and generate actionable feedback. This service aims to enhance email communication by providing insights into professionalism, clarity, and timeliness.

## Features
- **Dynamic Rules Engine**: A flexible engine that allows for the addition, updating, or removal of rules without altering the core code.
- **Email Parsing**: Extracts relevant data from .eml files, including metadata, body content, and attachments.
- **Audit Report Generation**: Produces detailed reports with scores, feedback, and suggestions for improvement based on the evaluation of emails.

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd email-audit-service
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.10 or higher installed. Then, install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   You can run the application directly using:
   ```
   python app.py
   ```
   Alternatively, you can use Docker for containerization:
   ```
   docker-compose up
   ```

## Usage
- **Upload .eml Files**: Send a POST request to `/upload` with the .eml file to be processed.
- **Retrieve Audit Reports**: Access the audit report by sending a GET request to `/report/<report_id>`.

## Directory Structure
```
email-audit-service
├── app.py                  # Main entry point of the application
├── requirements.txt        # Project dependencies
├── Dockerfile              # Docker image instructions
├── docker-compose.yml      # Docker Compose configuration
├── README.md               # Project documentation
├── src                     # Source code
│   ├── __init__.py        # Marks the directory as a Python package
│   ├── routes.py          # Defines application routes
│   ├── email_parser.py     # Functions for parsing .eml files
│   ├── rules_engine.py      # Implements the dynamic rules engine
│   ├── report_generator.py   # Generates the audit report
│   └── templates           # HTML templates for report generation
│       └── report.html     # Template for the audit report
├── config                  # Configuration files
│   └── rules.json         # Dynamic rules for email evaluation
└── tests                   # Unit tests
    ├── test_email_parser.py # Tests for email parsing functionality
    ├── test_rules_engine.py  # Tests for the rules engine
    └── example_emails      # Example .eml files for testing
        ├── sample1.eml
        └── sample2.eml
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.