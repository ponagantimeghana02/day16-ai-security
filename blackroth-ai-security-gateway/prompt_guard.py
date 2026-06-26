blocked=[

"ignore previous instructions",

"reveal prompt",

"developer mode",

"jailbreak",

"bypass"

]

def validate(prompt):

    text=prompt.lower()

    for attack in blocked:

        if attack in text:

            raise Exception("Prompt Injection Detected")

    return True