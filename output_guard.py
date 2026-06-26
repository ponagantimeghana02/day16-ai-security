import re
from datetime import datetime


class OutputGuard:
    def __init__(self):
        # PII patterns
        self.pii_patterns = [
            r"\b\d{12}\b",                         
            r"\b\d{10}\b",                          
            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",  
            r"\b\d{3}-\d{2}-\d{4}\b",              
        ]

        self.sensitive_keywords = [
            "password",
            "secret key",
            "api key",
            "token",
            "database password",
            "private key"
        ]

        self.toxic_words = [
            "stupid",
            "idiot",
            "hate",
            "kill",
            "dumb"
        ]

        self.unsafe_code_patterns = [
            r"os\.system",
            r"subprocess",
            r"rm -rf",
            r"eval\(",
            r"exec\("
        ]

        self.hallucination_markers = [
            "according to unknown source",
            "it is guaranteed that",
            "100% certain without evidence",
            "secret official data shows"
        ]

    def validate(self, output_text: str):

        violations = []
        risk_score = 0

        text_lower = output_text.lower()

        for pattern in self.pii_patterns:
            if re.search(pattern, output_text):
                violations.append("PII_DETECTED")
                risk_score += 40
                break

        for keyword in self.sensitive_keywords:
            if keyword in text_lower:
                violations.append("SENSITIVE_INFORMATION_LEAK")
                risk_score += 30
                break

        for word in self.toxic_words:
            if word in text_lower:
                violations.append("TOXIC_LANGUAGE")
                risk_score += 20
                break

        for pattern in self.unsafe_code_patterns:
            if re.search(pattern, output_text):
                violations.append("UNSAFE_CODE_GENERATION")
                risk_score += 35
                break

        for marker in self.hallucination_markers:
            if marker in text_lower:
                violations.append("HALLUCINATION_RISK")
                risk_score += 15
                break

       
        approved = risk_score < 50

        return {
            "approved": approved,
            "risk_score": risk_score,
            "violations": violations,
            "timestamp": datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    guard = OutputGuard()

    while True:
        user_input = input("\nEnter text (type 'exit' to stop): ")

        if user_input.lower() == "exit":
            break

        result = guard.validate(user_input)
        print(result)