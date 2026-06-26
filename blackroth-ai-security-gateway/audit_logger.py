import csv
import os
from datetime import datetime

FILE="logs/audit_logs.csv"

os.makedirs("logs",exist_ok=True)

def log(user,prompt,response,risk):

    exists=os.path.exists(FILE)

    with open(FILE,"a",newline="",encoding="utf8") as f:

        writer=csv.writer(f)

        if not exists:

            writer.writerow([
                "Time",
                "User",
                "Prompt",
                "Response",
                "Risk"
            ])

        writer.writerow([

            datetime.now(),

            user,

            prompt,

            response,

            risk

        ])