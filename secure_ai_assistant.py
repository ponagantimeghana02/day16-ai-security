"""
Secure Enterprise AI Assistant

Features:
✔ Authentication
✔ Role-Based Access Control (RBAC)
✔ Prompt Injection Detection
✔ Input Guardrails
✔ Policy Enforcement
✔ Secure RAG
✔ Safe Output Validation
✔ Audit Logging

Architecture

User
 ↓
Authentication
 ↓
Input Guard
 ↓
Policy Engine
 ↓
Secure RAG
 ↓
LLM
 ↓
Output Guard
 ↓
Audit Logger
 ↓
Response
"""

import re
from datetime import datetime

#########################################################
# USERS
#########################################################

USERS = {
    "alice": {
        "password": "hr123",
        "role": "HR"
    },
    "bob": {
        "password": "finance123",
        "role": "Payroll"
    },
    "admin": {
        "password": "admin123",
        "role": "Admin"
    }
}

#########################################################
# DOCUMENTS (RAG)
#########################################################

DOCUMENTS = [

    {
        "title": "Leave Policy",
        "department": "HR",
        "verified": True,
        "content": "Employees receive 20 annual paid leaves."
    },

    {
        "title": "Onboarding Guide",
        "department": "HR",
        "verified": True,
        "content": "New employees complete onboarding in 30 days."
    },

    {
        "title": "Salary Records",
        "department": "Payroll",
        "verified": True,
        "content": "Employee salary information."
    }

]

#########################################################
# AUTHENTICATION
#########################################################

class Authentication:

    @staticmethod
    def login(username, password):

        user = USERS.get(username)

        if not user:
            raise Exception("Unknown User")

        if user["password"] != password:
            raise Exception("Invalid Password")

        return user

#########################################################
# POLICY ENGINE
#########################################################

class PolicyEngine:

    POLICIES = {

        "HR": [
            "HR"
        ],

        "Payroll": [
            "Payroll"
        ],

        "Admin": [
            "HR",
            "Payroll"
        ]
    }

    @classmethod
    def authorize(cls, role, department):

        return department in cls.POLICIES.get(role, [])

#########################################################
# PROMPT INJECTION DETECTOR
#########################################################

class PromptGuard:

    BLOCKED = [

        "ignore previous instructions",
        "forget your instructions",
        "developer mode",
        "reveal system prompt",
        "jailbreak",
        "bypass",
        "override policy"

    ]

    @classmethod
    def validate(cls, prompt):

        p = prompt.lower()

        for attack in cls.BLOCKED:

            if attack in p:
                raise Exception(
                    "Prompt Injection Detected"
                )

#########################################################
# INPUT GUARD
#########################################################

class InputGuard:

    MAX_LENGTH = 500

    @staticmethod
    def validate(prompt):

        if len(prompt) > InputGuard.MAX_LENGTH:
            raise Exception("Prompt Too Long")

        if "<script>" in prompt.lower():
            raise Exception("Invalid Characters")

#########################################################
# SECURE RAG
#########################################################

class SecureRAG:

    @staticmethod
    def retrieve(role, prompt):

        docs = []

        for doc in DOCUMENTS:

            if not doc["verified"]:
                continue

            if not PolicyEngine.authorize(
                    role,
                    doc["department"]):
                continue

            if re.search(prompt,
                         doc["content"],
                         re.IGNORECASE):

                docs.append(doc)

        return docs

#########################################################
# MOCK LLM
#########################################################

class EnterpriseLLM:

    @staticmethod
    def generate(query, docs):

        if not docs:
            return "No relevant documents."

        answer = ""

        for d in docs:

            answer += f"{d['title']}\n"
            answer += f"{d['content']}\n\n"

        return answer

#########################################################
# OUTPUT GUARD
#########################################################

class OutputGuard:

    BLOCKED = [

        "salary",
        "password",
        "secret",
        "confidential"

    ]

    @classmethod
    def validate(cls, output):

        lower = output.lower()

        for word in cls.BLOCKED:

            if word in lower:
                return "[BLOCKED OUTPUT]"

        return output

#########################################################
# AUDIT LOGGER
#########################################################

class AuditLogger:

    @staticmethod
    def log(

        username,
        role,
        prompt,
        docs,
        response

    ):

        print("\n========== AUDIT ==========")

        print("Timestamp:",
              datetime.now())

        print("User:",
              username)

        print("Role:",
              role)

        print("Prompt:",
              prompt)

        print("Retrieved:",
              [d["title"] for d in docs])

        print("Response:",
              response)

        print("===========================\n")

#########################################################
# SECURE AI ASSISTANT
#########################################################

class SecureEnterpriseAI:

    def run(

        self,
        username,
        password,
        prompt

    ):

        user = Authentication.login(
            username,
            password
        )

        role = user["role"]

        InputGuard.validate(prompt)

        PromptGuard.validate(prompt)

        docs = SecureRAG.retrieve(
            role,
            prompt
        )

        response = EnterpriseLLM.generate(
            prompt,
            docs
        )

        response = OutputGuard.validate(
            response
        )

        AuditLogger.log(

            username,
            role,
            prompt,
            docs,
            response

        )

        return response

#########################################################
# DEMO
#########################################################

if __name__ == "__main__":

    assistant = SecureEnterpriseAI()

    try:

        answer = assistant.run(

            username="alice",
            password="hr123",
            prompt="leave"

        )

        print(answer)

    except Exception as e:

        print(e)