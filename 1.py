from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict
from datetime import datetime

app = FastAPI()


class Order(BaseModel):
    product_name: str = Field(..., min_length=1, description="Назва продукту не може бути порожньою")
    quantity: int = Field(default=1, gt=0, description="Кількість має бути більше 0")
    price_per_item: float = Field(..., gt=0, description="Ціна має бути позитивною")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True  



class User(BaseModel):
    name: str
    email: EmailStr
    orders: List[Order] = Field(default_factory=list)


users_db: Dict[str, User] = {}

@app.post("/users", status_code=201)
def create_user(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Користувач з такою електронною поштою вже існує.")
    users_db[user.email] = user
    return {"message": "Користувача створено успішно"}



@app.get("/users", response_model=User)
def get_user(email: EmailStr = Query(..., description="Введіть валідну email-адресу користувача")):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return users_db[email]
