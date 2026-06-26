"""
Enterprise Policy Engine

Features:
- Policy Enforcement
- Role-Based Access Control (RBAC)
- Agent Authorization
- Tool Execution Validation
- Audit Logging
"""

import logging
from datetime import datetime

# -----------------------------------------------------
# Logging Configuration
# -----------------------------------------------------

logging.basicConfig(
    filename="policy_engine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------------------------
# Enterprise Policies
# -----------------------------------------------------

POLICIES = {

    "HR Agent": {
        "can_access": [
            "leave_policy",
            "onboarding"
        ]
    },

    "Payroll Agent": {
        "can_access": [
            "salary_records"
        ]
    },

    "Customer Support Agent": {
        "can_access": [
            "faq",
            "customer_profile",
            "ticket_status"
        ]
    },

    "Admin Agent": {
        "can_access": [
            "*"
        ]
    }

}

# -----------------------------------------------------
# Sample Enterprise Tools
# -----------------------------------------------------

TOOLS = {

    "leave_policy":
        lambda: "Leave Policy Document",

    "onboarding":
        lambda: "Employee Onboarding Guide",

    "salary_records":
        lambda: "Salary Records Database",

    "faq":
        lambda: "Customer FAQ",

    "customer_profile":
        lambda: "Customer Profile",

    "ticket_status":
        lambda: "Ticket Status"

}


# -----------------------------------------------------
# Policy Engine
# -----------------------------------------------------

class PolicyEngine:

    def __init__(self):
        self.policies = POLICIES

    def authorize(self, agent, resource):

        if agent not in self.policies:
            return False

        permissions = self.policies[agent]["can_access"]

        if "*" in permissions:
            return True

        return resource in permissions


# -----------------------------------------------------
# Policy Enforcement Point (PEP)
# -----------------------------------------------------

class PolicyEnforcer:

    def __init__(self):
        self.engine = PolicyEngine()

    def execute_tool(self, agent, tool_name):

        logging.info(
            f"{agent} requested access to '{tool_name}'"
        )

        if not self.engine.authorize(agent, tool_name):

            logging.warning(
                f"ACCESS DENIED -> {agent} -> {tool_name}"
            )

            raise PermissionError(
                f"{agent} is NOT authorized to access '{tool_name}'"
            )

        logging.info(
            f"ACCESS GRANTED -> {agent} -> {tool_name}"
        )

        if tool_name not in TOOLS:
            raise ValueError("Tool does not exist.")

        result = TOOLS[tool_name]()

        return result


# -----------------------------------------------------
# Demonstration
# -----------------------------------------------------

if __name__ == "__main__":

    enforcer = PolicyEnforcer()

    tests = [

        ("HR Agent", "leave_policy"),
        ("HR Agent", "salary_records"),
        ("Payroll Agent", "salary_records"),
        ("Payroll Agent", "faq"),
        ("Customer Support Agent", "ticket_status"),
        ("Customer Support Agent", "salary_records"),
        ("Admin Agent", "salary_records"),
        ("Admin Agent", "leave_policy")

    ]

    for agent, tool in tests:

        print("=" * 60)

        print(f"Agent : {agent}")
        print(f"Tool  : {tool}")

        try:

            output = enforcer.execute_tool(agent, tool)

            print("Status : ACCESS GRANTED")
            print("Output :", output)

        except Exception as e:

            print("Status : ACCESS DENIED")
            print("Reason :", e)