# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from datetime import date

app = FastAPI()

# This is the blueprint for the data your Flutter app will send
class UserSignupSchema(BaseModel):
    id: str
    fullName: str
    status: str
    dob: date
    age: int
    address: str
    phonenumber: str
    email: EmailStr

# A simple test route to make sure your backend is working
@app.get("/")
def read_root():
    return {"status": "FastAPI backend is running successfully!"}

# The endpoint your Flutter ApiService will hit
@app.post("/api/users/signup")
async def signup_user(user_data: UserSignupSchema):
    print(f"Received data for user: {user_data.fullName}")
    # TODO: Next step is connecting this to your PostgreSQL database
    return {"status": "success", "received": user_data.id}
