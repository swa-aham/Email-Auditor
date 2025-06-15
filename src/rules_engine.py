import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import re


class Rule:
    def __init__(self, config: Dict[str, Any]):
        self.name = config["name"]
        self.description = config["description"]
        self.weight = config.get("weight", 1.0)
        self.config = config

    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class ProfessionalGreetingRule(Rule):
    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        greeting_patterns = self.config.get("keywords", [])
        body = email_content.get("body", "").lower()

        # Check first 200 characters for greeting
        opening_text = body[:200]
        
        for pattern in greeting_patterns:
            if pattern.lower() in opening_text:
                return {
                    "status": "pass",
                    "score": int(self.weight * 100),
                    "justification": f"Found professional greeting: '{pattern}'",
                }

        return {
            "status": "fail",
            "score": 0,
            "justification": "No professional greeting found at the beginning of the email",
        }


class ResponseTimeRule(Rule):
    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        max_hours = self.config.get("max_hours", 48)
        email_date = email_content.get("date")

        if not email_date:
            return {
                "status": "fail",
                "score": 0,
                "justification": "Email date not available for evaluation",
            }

        # If email_date is a string, try to parse it
        if isinstance(email_date, str):
            try:
                email_date = datetime.fromisoformat(email_date.replace("Z", "+00:00"))
            except:
                return {
                    "status": "fail",
                    "score": 0,
                    "justification": "Invalid email date format",
                }

        # Calculate time difference
        current_time = datetime.now()
        if email_date.tzinfo:
            # If email has timezone info, make current_time timezone aware
            from datetime import timezone
            current_time = current_time.replace(tzinfo=timezone.utc)
            
        time_diff = current_time - email_date
        hours_diff = time_diff.total_seconds() / 3600

        if hours_diff <= max_hours:
            return {
                "status": "pass",
                "score": int(self.weight * 100),
                "justification": f"Email sent within {max_hours} hours ({hours_diff:.1f} hours ago)",
            }

        return {
            "status": "fail",
            "score": int(self.weight * 50),  # Partial score for late response
            "justification": f"Email sent {hours_diff:.1f} hours ago, exceeding {max_hours} hour limit",
        }


class GrammarClarityRule(Rule):
    def apply(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        body = email_content.get("body", "")
        
        if not body.strip():
            return {
                "status": "fail",
                "score": 0,
                "justification": "Email body is empty",
            }

        words = body.split()
        word_count = len(words)
        
        # Count sentences more accurately
        sentences = re.split(r'[.!?]+', body.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        min_words = self.config.get("min_words", 10)
        max_sentences = self.config.get("max_sentences", 20)

        issues = []
        score = int(self.weight * 100)

        # Check minimum words
        if word_count < min_words:
            return {
                "status": "fail",
                "score": 0,
                "justification": f"Email too short: {word_count} words (minimum {min_words} required)",
            }

        # Check sentence count
        if sentence_count > max_sentences:
            score = int(self.weight * 70)  # Reduce score for too many sentences
            issues.append(f"too many sentences ({sentence_count}, max recommended: {max_sentences})")

        # Basic grammar checks
        if body.count('..') > 2:  # Too many ellipses
            score = max(score - 10, 0)
            issues.append("excessive use of ellipses")
            
        if body.count('!!') > 1:  # Too many exclamation marks
            score = max(score - 10, 0)
            issues.append("excessive use of exclamation marks")

        # Check for common words that indicate good structure
        good_words = ['please', 'thank', 'regards', 'sincerely', 'best']
        has_polite_words = any(word in body.lower() for word in good_words)
        
        if not has_polite_words:
            score = max(score - 15, 0)
            issues.append("lacks polite language")

        if issues:
            status = "partial" if score > 50 else "fail"
            justification = f"Issues found: {', '.join(issues)}"
        else:
            status = "pass"
            justification = f"Good clarity and structure ({word_count} words, {sentence_count} sentences)"

        return {
            "status": status,
            "score": score,
            "justification": justification,
        }


class RulesEngine:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Rule]:
        """Load rules from configuration file"""
        try:
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
                rule_name = rule_config.get("name")
                rule_class = rule_classes.get(rule_name)
                if rule_class:
                    rules.append(rule_class(rule_config))
                else:
                    print(f"Warning: Unknown rule type '{rule_name}' in configuration")

            return rules
        except Exception as e:
            print(f"Error loading rules: {str(e)}")
            return []

    def evaluate_email(self, email_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate email against all loaded rules"""
        results = []
        for rule in self.rules:
            try:
                result = rule.apply(email_content)
                result["rule"] = rule.name.replace("_", " ").title()
                result["description"] = rule.description
                result["weight"] = rule.weight
                results.append(result)
            except Exception as e:
                # If a rule fails, add an error result
                results.append({
                    "rule": rule.name.replace("_", " ").title(),
                    "description": rule.description,
                    "weight": rule.weight,
                    "status": "error",
                    "score": 0,
                    "justification": f"Rule evaluation failed: {str(e)}"
                })
        return results

    def add_rule(self, rule: Rule):
        """Add a new rule to the engine"""
        self.rules.append(rule)

    def remove_rule(self, rule_name: str):
        """Remove a rule by name"""
        self.rules = [rule for rule in self.rules if rule.name != rule_name]

    def get_rule_names(self) -> List[str]:
        """Get list of all rule names"""
        return [rule.name for rule in self.rules]