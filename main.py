import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI, OpenAIError

app = FastAPI(title="Bible AI", description="Get Bible verses using AI", version="1.0.0")

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Request body
class BibleQuery(BaseModel):
    query: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Bible AI is running!"}

# Bible endpoint
@app.post("/bible")
async def get_bible_verse(bible_query: BibleQuery, request: Request):
    query = bible_query.query

    # Log request
    print(f"Received query: {query}")

    try:
        # Make real OpenAI API request
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # Recommended cost-effective model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides Bible verses and explanations."},
                {"role": "user", "content": query},
            ],
            max_tokens=150
        )

        answer = response.choices[0].message.content.strip()
        return {"mode": "real", "answer": answer}

    except OpenAIError as e:
        # Fallback to test mode on any error (like quota exceeded)
        print(f"Error occurred: {e}")
        return JSONResponse(
            status_code=200,
            content={
                "mode": "test",
                "answer": "TEST MODE: “I can do all things through Christ who strengthens me.” — Philippians 4:13"
            }
        )





