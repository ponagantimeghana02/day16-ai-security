permissions={

"HR":[
"leave",
"onboarding"
],

"Payroll":[
"salary"
],

"Admin":[
"*"
]

}


def authorize(role,resource):

    if "*" in permissions[role]:
        return True

    return resource in permissions[role]