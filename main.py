
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# Load your OpenAI key here (you will set this on Render later)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    grade: int
    subject: str
    question: str

@app.post("/chat")
async def chat(input: ChatInput):
    prompt = f"You are a helpful tutor for Grade {input.grade} in {input.subject}. Answer this question simply: {input.question}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a kind and intelligent tutor."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
