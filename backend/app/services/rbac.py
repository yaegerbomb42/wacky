ROLE_LEVEL = {"viewer": 1, "operator": 2, "admin": 3}

def require_role(user_role: str, min_role: str) -> bool:
    return ROLE_LEVEL.get(user_role, 0) >= ROLE_LEVEL.get(min_role, 999)
