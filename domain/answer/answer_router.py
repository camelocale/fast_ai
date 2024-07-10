from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user
from models import User
import logging

router = APIRouter(
    prefix="/api/answer",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 리턴할 응답이 없는 경우, 응답 코드 204를 리턴하여 응답없음을 나타낼 수 있다. 
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int, _answer_create: answer_schema.AnswerCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(db, question=question, answer_create=_answer_create, user=current_user)

@router.post("/generate/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_generate(question_id: int, _answer_create: answer_schema.AnswerCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    # question = question_crud.get_question(db, question_id=question_id)
    # if not question:
    #     raise HTTPException(status_code=404, detail="Question not found")

    # async def stream_results() -> AsyncGenerator[bytes, None]:
    #     try:
    #         split_text_list = sentence_split(og_prompt)
    #         print(split_text_list)
    #         prompt = create_prompt(split_text_list[0], src_lang, tgt_lang)
    #         for i in range(len(split_text_list)):
    #             len_text = 0
    #             prompt = update_user_prompt(prompt, split_text_list, i, src_lang, tgt_lang)
    #             results_generator = make_generator(prompt)
    #             len_text = 0
    #             async for request_output in results_generator:
    #                 text_outputs = [
    #                     output.text.strip() for output in request_output.outputs
    #                 ]
    #                 print(text_outputs[0][len_text:], end="", flush=True)
    #                 len_text = len(text_outputs[0])
    #                 yield text_outputs[0]
    #             prompt = update_assistant_prompt(prompt, text_outputs[0])
    #     except Exception as e:
    #         print(f"Error result: {e}")
    #         yield json.dumps({"text":[]})
    def stream_results():
        for chunk in answer_crud.generate_answer(_answer_create.content):
            yield chunk

    return StreamingResponse(stream_results())
    # _answer_create.content = result
    # answer_crud.create_answer(db, question=question, answer_create=_answer_create, user=current_user)


@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    answer_crud.update_answer(db=db, db_answer=db_answer,
                                answer_update=_answer_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                    db: Session = Depends(get_db), 
                    current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    answer_crud.delete_answer(db=db, db_answer=db_answer)