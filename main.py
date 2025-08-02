import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = FastAPI()

# Initialize OpenAI client with API key from .env
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Toggle this to True to avoid real API calls
TEST_MODE = False

# Pydantic model for POST /bible
class BibleRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "Bible AI is running!"}

@app.post("/bible")
async def bible_ai(request: BibleRequest):
    query = request.query

    # If test mode is enabled, return a dummy response
    if TEST_MODE:
        return {
            "mode": "test",
            "answer": f"TEST MODE: This is a dummy AI answer for '{query}'"
        }

    try:
        # Real OpenAI API call
        response = client.responses.create(
            model="gpt-4.1-mini",  # Use gpt-4.1-mini for cost efficiency
            input=f"Give a Bible-based response for: {query}"
        )

        answer = response.output[0].content[0].text

        return {
            "mode": "real",
            "answer": answer
        }

    except Exception as e:
        return {
            "error": str(e)
        }




