from rbac import authorize

def enforce(role,resource):

    if authorize(role,resource):

        return True

    raise Exception("Access Denied")