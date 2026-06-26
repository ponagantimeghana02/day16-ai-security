import logging
from datetime import datetime

# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------

logging.basicConfig(
    filename="rag_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------------------------
# Mock Users Database
# ---------------------------------------------------

USERS = {
    "alice": {
        "password": "hr123",
        "role": "HR"
    },
    "bob": {
        "password": "finance123",
        "role": "Finance"
    },
    "charlie": {
        "password": "employee123",
        "role": "Employee"
    }
}


# ---------------------------------------------------
# Mock Document Store
# ---------------------------------------------------

DOCUMENTS = [
    {
        "title": "HR Policies",
        "content": "Employees are entitled to 20 annual leaves.",
        "department": "HR",
        "source": "Internal HR Portal",
        "verified": True
    },
    {
        "title": "Finance Salary Records",
        "content": "Salary details of all employees.",
        "department": "Finance",
        "source": "Finance Database",
        "verified": True
    },
    {
        "title": "Employee Handbook",
        "content": "Company code of conduct.",
        "department": "General",
        "source": "Company Portal",
        "verified": True
    },
    {
        "title": "Draft Budget",
        "content": "Budget planning document.",
        "department": "Finance",
        "source": "Unknown",
        "verified": False
    }
]


# ---------------------------------------------------
# Authentication
# ---------------------------------------------------

class Authentication:

    @staticmethod
    def login(username, password):

        user = USERS.get(username)

        if user and user["password"] == password:
            print("Authentication Successful\n")
            return user

        raise Exception("Authentication Failed")


# ---------------------------------------------------
# Role Based Access Control
# ---------------------------------------------------

class RBAC:

    ROLE_ACCESS = {
        "HR": ["HR", "General"],
        "Finance": ["Finance", "General"],
        "Employee": ["General"]
    }

    @classmethod
    def has_access(cls, role, department):

        return department in cls.ROLE_ACCESS.get(role, [])


# ---------------------------------------------------
# Metadata Filtering
# ---------------------------------------------------

class MetadataFilter:

    @staticmethod
    def filter_documents(role):

        allowed_docs = []

        for doc in DOCUMENTS:

            if RBAC.has_access(role, doc["department"]):
                allowed_docs.append(doc)

        return allowed_docs


# ---------------------------------------------------
# Source Validation
# ---------------------------------------------------

class SourceValidator:

    @staticmethod
    def validate(doc):

        return doc["verified"]


# ---------------------------------------------------
# Query Auditing
# ---------------------------------------------------

class QueryAuditor:

    @staticmethod
    def log(username, role, query):

        logging.info(
            f"User={username} | Role={role} | Query={query}"
        )


# ---------------------------------------------------
# Output Validation
# ---------------------------------------------------

class OutputValidator:

    BLOCKED_WORDS = [
        "salary",
        "confidential",
        "budget"
    ]

    @classmethod
    def validate(cls, answer):

        text = answer.lower()

        for word in cls.BLOCKED_WORDS:

            if word in text:
                return "Output blocked due to sensitive information."

        return answer


# ---------------------------------------------------
# Secure RAG Pipeline
# ---------------------------------------------------

class SecureRAG:

    def __init__(self):

        self.documents = DOCUMENTS

    def retrieve(self, role, query):

        docs = MetadataFilter.filter_documents(role)

        retrieved = []

        for doc in docs:

            if query.lower() in doc["content"].lower() \
                    or query.lower() in doc["title"].lower():

                if SourceValidator.validate(doc):
                    retrieved.append(doc)

        return retrieved

    def generate_answer(self, docs):

        if not docs:
            return "No relevant documents found."

        answer = "\n\n".join(
            f"{doc['title']}\n{doc['content']}"
            for doc in docs
        )

        return OutputValidator.validate(answer)

    def ask(self, username, role, query):

        QueryAuditor.log(username, role, query)

        docs = self.retrieve(role, query)

        return self.generate_answer(docs)


# ---------------------------------------------------
# Example Usage
# ---------------------------------------------------

if __name__ == "__main__":

    try:

        user = Authentication.login(
            "alice",
            "hr123"
        )

        rag = SecureRAG()

        question = "leave"

        response = rag.ask(
            username="alice",
            role=user["role"],
            query=question
        )

        print("User Role:", user["role"])
        print("\nQuestion:", question)
        print("\nResponse:\n")
        print(response)

    except Exception as e:
        print(e)