import bcrypt


def hash_password(password: str):
    return (bcrypt.hashpw(password.encode(), bcrypt.gensalt())).decode()


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
