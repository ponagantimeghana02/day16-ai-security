import re
import json
from datetime import datetime


class PromptInjectionDetector:
    def __init__(self):
        self.patterns = {
            "IGNORE_INSTRUCTIONS": [
                r"ignore (all|previous|earlier) instructions",
                r"disregard (all|previous|earlier) instructions"
            ],
            "SYSTEM_PROMPT_LEAK": [
                r"reveal (your )?system prompt",
                r"show (your )?system prompt",
                r"what is your system prompt"
            ],
            "RESTRICTION_BYPASS": [
                r"bypass (all )?restrictions",
                r"ignore safety",
                r"disable safety",
                r"turn off filters"
            ],
            "ROLE_OVERRIDE": [
                r"you are now",
                r"act as if you are",
                r"pretend you are",
                r"switch role to"
            ],
            "JAILBREAK": [
                r"DAN mode",
                r"developer mode",
                r"unfiltered mode",
                r"no restrictions"
            ],
            "OBFUSCATION": [
                r"i\s*g\s*n\s*o\s*r\s*e",
                r"r\.e\.v\.e\.a\.l",
                r"(?i).*ignore.*instructions.*"
            ]
        }

    def detect(self, prompt: str):
        prompt_lower = prompt.lower()

        for attack_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, prompt_lower):
                    return {
                        "risk": "HIGH",
                        "attack": "Prompt Injection",
                        "type": attack_type,
                        "action": "Blocked",
                        "input": prompt,
                        "timestamp": datetime.utcnow().isoformat()
                    }

        return {
            "risk": "LOW",
            "attack": None,
            "action": "Allowed",
            "input": prompt,
            "timestamp": datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    detector = PromptInjectionDetector()

    test_input = input("Enter prompt: ")

    result = detector.detect(test_input)

    print("\n🔐 Prompt Injection Detection Result\n")
    print(json.dumps(result, indent=2))

    report = f"""
# Prompt Attack Report

Time: {result['timestamp']}

## Input
{test_input}

## Result
Risk: {result['risk']}
Attack Type: {result['type'] if result.get('type') else 'None'}
Action: {result['action']}

## Summary
This system detected and blocked malicious prompt injection attempts.
"""

    with open("prompt_attack_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n📄 Report generated: prompt_attack_report.md\n")