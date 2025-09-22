# chatbot
A FastAPI-based chatbot platform with Google Gemini AI integration, built to support multiple users, authentication, and chat history storage.


# Features
👤 User signup & login with JWT authentication
🔐 Secure password storage with bcrypt
🤖 AI chatbot powered by Google Gemini (gemini-1.5-flash)
💾 Chat history stored in SQLite/PostgreSQL
🖥️ Simple UI with Jinja2 templates (index, signup, chat)
📜 REST API for chat + history retrieval


# Tech Stack
Backend: FastAPI (Python 3.10+), Uvicorn
Database: SQLAlchemy ORM (SQLite / PostgreSQL)
Auth: JWT (python-jose), Passlib (bcrypt)
AI: Google Generative AI SDK
Frontend: Jinja2 templates


# Setup & Run
1️⃣ Clone Repository
git clone https://github.com/yourusername/chatbot-platform.git
cd chatbot-platform


2️⃣ **Create Environment & Install Dependencies**
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt


3️⃣ **Configure Environment Variables**
Create a .env file in the root (based on .env.example):
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

**Google Generative AI Key**
GEMINI_API_KEY=your-api-key

**Database URL**
DATABASE_URL=sqlite:///./chatbot.db

4️⃣ Run the App
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Open in browser:

UI → http://localhost:8000

API Docs → http://localhost:8000/docs


🧪 **API Endpoints**
**Method**	**Endpoint**	**Description**
POST	      /signup	     Register a new user
POST	      /token	     Login & receive JWT
POST	      /chat	      Send message & get AI response
GET	       /history	    Fetch user’s chat history

 **Architecture Overview**
FastAPI app serves APIs and web templates.
Auth system secures users with JWT.
Database (SQLAlchemy) stores users and chat logs.
In-memory store keeps active session memory.
AI model (Gemini) handles message generation.

Frontend (Jinja2) provides signup/login/chat UI.
