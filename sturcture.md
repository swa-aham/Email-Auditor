```
email-audit-service/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose configuration
├── README.md                   # Project documentation
├── setup_and_run.sh           # Automated setup script
├── test_api.py                 # API testing script
├── src/                        # Source code
│   ├── __init__.py
│   ├── routes.py              # API routes
│   ├── email_parser.py        # Email parsing functionality
│   ├── rules_engine.py        # Dynamic rules engine
│   ├── report_generator.py    # Report generation
│   └── templates/
│       └── report.html        # HTML report template
├── config/
│   └── rules.json            # Rules configuration
└── tests/
    ├── example_emails/
    │   ├── sample1.eml       # Test email with attachment
    │   └── sample2.eml       # Test email with HTML content
    ├── test_email_parser.py  # Parser tests
    └── test_rules_engine.py  # Rules engine tests
```