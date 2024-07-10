from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question
from database import get_db
from domain.question import question_schema, question_crud
from starlette import status

from domain.user.user_router import get_current_user
from models import User

#라우팅은 요청받은 URL을 해석하여 그에 맞는 함수를 실행하여 그 결과를 리턴하는 행위이다. 

router = APIRouter(
    prefix="/api/question",
)

# # 만약 Question 스키마에서 content 항목을 제거하면 질문 목록 API의 출력 항목에도 content가 제거된다. 실제 리턴되는 _question_list를 수정할 필요가 없이 스키마를 제한해주면 된다. 
# @router.get("/list", response_model=list[question_schema.Question])
# # db: Session 문장의 의미는 db 객체가 Session 타입임을 나타낸다.
# # Depends에서 contextmanager를 적용하도록 설계되어 있기 때문에 get_db 위의 어노테이션은 제거해준다. 
# def question_list(db: Session = Depends(get_db)): # with 문 대신에 question_list가 매개변수로 객체를 주입받았다. 
#     # way 1
#     # db = SessionLocal()
#     # _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     # db.close() # 세션을 종료하는 것이 아니라 사용한 세션을 커넥션 풀에 반환하는 함수이다. 

#     # way 2
#     # with get_db() as db:
#     #     _question_list = db.query(Question).order_by(Question.create_date.desc()).all()

#     _question_list = question_crud.get_question_list(db) # question_crud.py 파일로 crud 기능 함수를 분리
#     return _question_list

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db :Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create",  response_model=question_schema.Question)
def question_create(_question_create: question_schema.QuestionCreate,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    created_question = question_crud.create_question(db=db, question_create=_question_create, user=current_user)
    return created_question

@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                    page: int = 0, size: int = 10):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'question_list': _question_list
    }

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question, question_update=_question_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)