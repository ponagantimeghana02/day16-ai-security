def calculate(prompt):

    score=0

    attacks=[

    "ignore",

    "jailbreak",

    "bypass",

    "developer"

    ]

    for attack in attacks:

        if attack in prompt.lower():

            score+=25

    return score