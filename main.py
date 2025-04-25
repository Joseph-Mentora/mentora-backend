from utils.curriculum_loader import load_curriculum
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# Load your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS settings to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model for chat requests
class ChatInput(BaseModel):
    grade: str
    subject: str
    question: str

@app.post("/chat")
async def chat(input: ChatInput):
    # Default tone
    prompt_intro = f"You are a helpful tutor for Grade {input.grade} in {input.subject}."

    # Special case: Kindergarten English
    if input.grade.lower() in ["k", "kindergarten", "0"]:
        if input.subject.lower() == "english":
            curriculum = load_curriculum("kindergarten")
            tone = curriculum.get("chatbot_guidance", {}).get("tone", "")
            prompt_intro = f"{tone} You are a Kindergarten tutor for English."

    # Build the final prompt
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
