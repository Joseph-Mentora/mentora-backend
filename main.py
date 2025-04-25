from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# Load your OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create the FastAPI app
app = FastAPI()

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["https://mentora.cloud"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what kind of input the chatbot expects
class ChatInput(BaseModel):
    grade: int
    subject: str
    question: str

# Define the chatbot endpoint
@app.post("/chat")
async def chat(input: ChatInput):
    prompt = f"You are a helpful tutor for Grade {input.grade} in {input.subject}. Answer this question simply: {input.question}"

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
            return {"answer": "I'm still thinking… can you try that question a different way?"}
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
