# import contextlib
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

# fastapi에 ORM을 적용하기 위해서 필요한 데이터 베이스 설정이다.
# Dependency Injection(의존성 주입)은 필요한 기능을 선언하여 사용할 수 있다는 의미이다. 

SQLALCHEMY_DATABASE_URL = "sqlite:///./fast.db"

# create_engine은 데이터 베이스에 접속하는 여러개의 객체인 connection pool을 만들어놓고 돌려가며 사용한다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스에 접근하기 위한 클래스, autocommit을 false로 해놓으면 데이터를 변경했을 때 commit 사인을 주어야 업데이트가 된다. 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

# @context.contextmanager # 해당 어노테이션을 사용함으로써 with 문과 함께 사용할 수 있다. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: # always get excuted exception is generated or not. yield의 응답이 전달된 후 실행됨.
        db.close()
