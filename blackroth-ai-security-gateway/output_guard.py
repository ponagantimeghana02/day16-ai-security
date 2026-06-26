blocked=[

"password",

"api key",

"salary"

]

def validate(response):

    lower=response.lower()

    for word in blocked:

        if word in lower:

            return "[BLOCKED RESPONSE]"

    return response