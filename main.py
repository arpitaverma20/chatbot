from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import SessionLocal, User, Chat
from auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# In-memory chat state per user
chat_memory = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Frontend Pages ----------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/chat-ui", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# ---------- API Endpoints ----------

@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = get_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/", status_code=303)  # redirect to login


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/chat")
def chat(message: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    username = current_user.username

    try:
        response = model.generate_content(message)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"⚠️ Gemini API Error: {e}"

    # Save in in-memory session
    if username not in chat_memory:
        chat_memory[username] = []
    chat_memory[username].append({"message": message, "response": bot_reply})

    # Persist to DB
    chat_entry = Chat(user_id=current_user.id, message=message, response=bot_reply)
    db.add(chat_entry)
    db.commit()

    return {"response": bot_reply, "history": chat_memory[username]}


@app.get("/history")
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).all()
    return {"history": [{"message": c.message, "response": c.response, "timestamp": c.timestamp} for c in chats]}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app)
