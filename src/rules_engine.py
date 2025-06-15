import json
import os
from datetime import datetime
from typing import Dict, List, Any
import re


class Rule:
    def __init__(self, config: Dict[str, Any]):
        self.name = config["name"]
        self.description = config["description"]
        self.weight = config["weight"]
        self.config = config

    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class ProfessionalGreetingRule(Rule):
    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        greeting_patterns = self.config.get("keywords", [])
        body = email_content["body"].lower()

        for pattern in greeting_patterns:
            if pattern.lower() in body[:100]:  # Check first 100 chars
                return {
                    "status": "pass",
                    "score": self.weight * 100,
                    "justification": f"Found professional greeting: {pattern}",
                }

        return {
            "status": "fail",
            "score": 0,
            "justification": "No professional greeting found",
        }


class ResponseTimeRule(Rule):
    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        max_hours = self.config.get("max_hours", 48)
        email_date = email_content["date"]

        if isinstance(email_date, str):
            email_date = datetime.fromisoformat(email_date.replace("Z", "+00:00"))

        time_diff = datetime.now() - email_date
        hours_diff = time_diff.total_seconds() / 3600

        if hours_diff <= max_hours:
            return {
                "status": "pass",
                "score": self.weight * 100,
                "justification": f"Response time within {max_hours} hours",
            }

        return {
            "status": "fail",
            "score": 0,
            "justification": f"Response time exceeded {max_hours} hours",
        }


class GrammarClarityRule(Rule):
    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        body = email_content["body"]
        words = len(body.split())
        sentences = len(re.split(r"[.!?]+", body))

        min_words = self.config.get("min_words", 10)
        max_sentences = self.config.get("max_sentences", 5)

        if words < min_words:
            return {
                "status": "fail",
                "score": 0,
                "justification": f"Email too short (minimum {min_words} words required)",
            }

        if sentences > max_sentences:
            score = self.weight * 50  # Partial score
            return {
                "status": "partial",
                "score": score,
                "justification": f"Email has too many sentences (maximum {max_sentences} recommended)",
            }

        return {
            "status": "pass",
            "score": self.weight * 100,
            "justification": "Email length and clarity are good",
        }


class RulesEngine:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Rule]:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "rules.json"
        )
        with open(config_path, "r") as f:
            config = json.load(f)

        rule_classes = {
            "professional_greeting": ProfessionalGreetingRule,
            "response_time": ResponseTimeRule,
            "grammar_clarity": GrammarClarityRule,
        }

        rules = []
        for rule_config in config["rules"]:
            rule_class = rule_classes.get(rule_config["name"])
            if rule_class:
                rules.append(rule_class(rule_config))

        return rules

    def evaluate_email(self, email_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for rule in self.rules:
            result = rule.apply(email_content)
            result["rule"] = rule.name
            results.append(result)
        return results
