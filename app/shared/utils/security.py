import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode() 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Comparar la contraseña en texto plano con la hasheada
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
