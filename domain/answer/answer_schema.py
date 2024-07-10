import datetime
from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

# get이 아닌 다른 방식(post, put, delete)의 입력 값은 pydantic 스키마로만 읽을 수 있다. 
class AnswerCreate(BaseModel):
    content: str
    @field_validator('content')

    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None # default: None

class AnswerUpdate(AnswerCreate): # AnswerCreate 스키마에 이미 content 항목이 있으므오 AnswerCreate 스키마를 상속하고 answer_id 항목만 추가했다. 
    answer_id: int

class AnswerDelete(BaseModel):
    answer_id: int