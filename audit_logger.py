"""
AI Audit & Compliance Logger

Features:
- User Activity Logging
- Audit Trail
- CSV Export
- Compliance Report Generation
- Risk Scoring
- Policy Decision Logging
"""

import csv
from datetime import datetime

# --------------------------------------------------
# Audit Logger
# --------------------------------------------------

class AuditLogger:

    def __init__(self):

        self.logs = []

    def log(
        self,
        user_id,
        prompt,
        tool_used,
        retrieved_documents,
        model_response,
        risk_score,
        policy_decision
    ):

        record = {

            "User ID": user_id,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Prompt": prompt,
            "Tool Used": tool_used,
            "Retrieved Documents": ", ".join(retrieved_documents),
            "Model Response": model_response,
            "Risk Score": risk_score,
            "Policy Decision": policy_decision

        }

        self.logs.append(record)

    # ----------------------------------------------
    # Export CSV
    # ----------------------------------------------

    def export_csv(self, filename="audit_logs.csv"):

        if not self.logs:
            print("No logs available.")
            return

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.logs[0].keys()
            )

            writer.writeheader()

            writer.writerows(self.logs)

        print(f"{filename} generated successfully.")

    # ----------------------------------------------
    # Compliance Report
    # ----------------------------------------------

    def generate_report(self, filename="compliance_report.md"):

        total_requests = len(self.logs)

        allowed = sum(
            1 for log in self.logs
            if log["Policy Decision"] == "ALLOW"
        )

        denied = sum(
            1 for log in self.logs
            if log["Policy Decision"] == "DENY"
        )

        high_risk = sum(
            1 for log in self.logs
            if log["Risk Score"] >= 8
        )

        medium_risk = sum(
            1 for log in self.logs
            if 5 <= log["Risk Score"] < 8
        )

        low_risk = sum(
            1 for log in self.logs
            if log["Risk Score"] < 5
        )

        with open(filename, "w", encoding="utf-8") as file:

            file.write("# AI Audit & Compliance Report\n\n")

            file.write(f"Generated: {datetime.now()}\n\n")

            file.write("## Summary\n\n")

            file.write(f"- Total Requests : {total_requests}\n")
            file.write(f"- Allowed Requests : {allowed}\n")
            file.write(f"- Denied Requests : {denied}\n")
            file.write(f"- High Risk Requests : {high_risk}\n")
            file.write(f"- Medium Risk Requests : {medium_risk}\n")
            file.write(f"- Low Risk Requests : {low_risk}\n\n")

            file.write("## Compliance Checklist\n\n")

            file.write("|Requirement|Status|\n")
            file.write("|---|---|\n")
            file.write("|User ID Logged|✅|\n")
            file.write("|Timestamp Logged|✅|\n")
            file.write("|Prompt Logged|✅|\n")
            file.write("|Tool Usage Logged|✅|\n")
            file.write("|Retrieved Documents Logged|✅|\n")
            file.write("|Model Response Logged|✅|\n")
            file.write("|Risk Score Logged|✅|\n")
            file.write("|Policy Decision Logged|✅|\n")
            file.write("|CSV Export|✅|\n")

        print(f"{filename} generated successfully.")


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    audit = AuditLogger()

    audit.log(
        user_id="EMP001",
        prompt="Show leave policy",
        tool_used="HR Knowledge Base",
        retrieved_documents=[
            "leave_policy.pdf",
            "employee_handbook.pdf"
        ],
        model_response="Employees receive 20 annual leave days.",
        risk_score=2,
        policy_decision="ALLOW"
    )

    audit.log(
        user_id="EMP002",
        prompt="Show salary records",
        tool_used="Payroll Database",
        retrieved_documents=[
            "salary_records.xlsx"
        ],
        model_response="Access denied.",
        risk_score=9,
        policy_decision="DENY"
    )

    audit.log(
        user_id="SUP001",
        prompt="Check customer ticket status",
        tool_used="Customer Support Tool",
        retrieved_documents=[
            "ticket_1045.json"
        ],
        model_response="Ticket is currently in progress.",
        risk_score=3,
        policy_decision="ALLOW"
    )

    audit.export_csv()

    audit.generate_report()

    print("Audit completed successfully.")