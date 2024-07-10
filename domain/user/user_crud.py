from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                    password=pwd_context.hash(user_create.password1), # 비밀번호는 탈취되더라도 복호화할 수 없는 값으로 암호화해서 저장해야 한다.
                    email=user_create.email)
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
