from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import User

# ==============================
# PASSWORD HASHING SETUP
# ==============================
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


# ==============================
# HASH PASSWORD
# ==============================
def hash_password(password: str):
    return pwd_context.hash(password)


# ==============================
# VERIFY PASSWORD
# ==============================
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ==============================
# REGISTER USER
# ==============================
def register_user(db: Session, full_name: str, email: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        return None

    hashed_pw = hash_password(password)

    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==============================
# AUTHENTICATE LOGIN
# ==============================
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user