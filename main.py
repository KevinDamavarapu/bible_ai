from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Allow all origins for testing; tighten later if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["https://bible-ai-frontend-your.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "Bible AI is running!"}

@app.post("/bible")
def bible(query: str = Query(..., description="Enter your Bible question here")):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Answer this based on the Bible: {query}"
        )
        return {"answer": response.output_text}
    except Exception as e:
        return {"error": str(e)}








