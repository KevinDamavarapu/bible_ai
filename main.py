from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Allow CORS for mobile/browser testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "Bible AI is running!"}

@app.post("/bible")
def bible(query: str = Query(..., description="Enter your Bible question here")):
    """
    Ask Bible AI a question. Now accepts plain text in Swagger UI.
    """
    try:
        # Call OpenAI for a real response
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Answer this based on the Bible: {query}"
        )

        answer = response.output_text
        return {"mode": "real", "answer": answer}

    except Exception as e:
        return {"mode": "error", "error": str(e)}





