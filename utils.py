from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


def hash_password(plain_password : str) -> str :
    
    return pwd_context.hash(plain_password)


def verify_password(attempted_password : str, actual_hashed_password : str) -> bool :

    return pwd_context.verify(attempted_password, actual_hashed_password)





