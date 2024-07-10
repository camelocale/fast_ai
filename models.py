from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    # 모델에 의해 관리되는 테이블의 이름
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=-False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    modify_date = Column(DateTime, nullable=True)

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=-False)
    create_date = Column(DateTime, nullable=False)
    # 답변 모델에서 질문 모델을 참조하기 위해서 외부키 사용
    question_id = Column(Integer, ForeignKey("question.id"))
    # 질문에서 답변을 역참조 하기 위해서 relationship 사용, backref에 넣은 키워드로 question에서 answers를 역참조할 수 있음 
    question = relationship("Question", backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    