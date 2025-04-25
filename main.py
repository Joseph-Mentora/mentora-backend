from utils.curriculum_loader import load_curriculum
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
    # Default tone
    prompt_intro = f"You are a helpful tutor for Grade {input.grade} in {input.subject}."

    # Load custom tone if Kindergarten + English
    if str(input.grade).lower() in ["k", "kindergarten", "0"] or input.grade == 0:
        if input.subject.lower() == "english":
            curriculum = load_curriculum("kindergarten")
            tone = curriculum.get("chatbot_guidance", {}).get("tone", "")
            prompt_intro = f"{tone} You are a Kindergarten tutor for English."

    # Full prompt
    prompt = f"{prompt_intro} Answer this question simply: {input.question}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a kind and intelligent tutor."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
if not answer:
    answer = "Hmm, I’m not sure how to answer that yet — can you try asking another way?"
print("Final answer:", answer)
return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
