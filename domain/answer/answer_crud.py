from datetime import datetime
from sqlalchemy.orm import Session
from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import Question, Answer, User
import requests
import json


def create_answer(db: Session, question: Question, answer_create: AnswerCreate, user: User):
    db_answer = Answer(question=question,
                        content=answer_create.content,
                        create_date=datetime.now(),
                        user=user)
    db.add(db_answer)
    db.commit()

def generate_answer(prompt: str):
    ### implemetation
    vllm_host = "http://localhost:8000"
    url = f"{vllm_host}/generate"
    
    def chat(messages):
        # headers = {'Content-Type': 'application/json'}
        data = {
            "prompt": messages,
            "stream": True,
            "src_lang": "Auto",
            "tgt_lang": "Korean",
        }
        r = requests.post(url, json=data, stream=True)
        return r

    response = chat(prompt)
    for line in response.iter_content(chunk_size=4096):
        yield line.decode('utf-8')

def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

def update_answer(db: Session, db_answer: Answer,
                    answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()

def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()
