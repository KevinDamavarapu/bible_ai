from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow all origins for testing; tighten later for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def link_bible_references(text: str) -> str:
    """
    Detect Bible references in text and convert them into clickable YouVersion links (NIV).
    Example: John 3:16 → https://www.bible.com/bible/111/JHN.3.16.NIV
    """
    # Regex for Bible references like "John 3:16" or "1 Corinthians 13:4-7"
    pattern = r'([1-3]?\s?[A-Za-z]+)\s(\d+):(\d+(-\d+)?)'

    def repl(match):
        book = match.group(1).strip().replace(" ", "")
        chapter = match.group(2)
        verse = match.group(3)
        url = f"https://www.bible.com/bible/111/{book}.{chapter}.{verse}.NIV"
        return f"[{match.group(0)}]({url})"

    return re.sub(pattern, repl, text)

@app.get("/")
def home():
    return {"message": "Bible AI is running!"}

@app.post("/bible")
def bible(query: str = Query(..., description="Enter your Bible question here")):
    try:
        # System prompt to keep answers simple, clear, and NIV-based
        system_prompt = (
            "You are Bible AI, a helpful assistant that answers questions only based on the Bible. "
            "Use the New International Version (NIV) when quoting scripture. "
            "Always provide direct scripture references where relevant."
        )

        # Ask model for main answer
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )

        answer_text = response.output_text
        answer_text = link_bible_references(answer_text)

        # Ask model for related questions
        related_prompt = (
            f"Based on the user's question: '{query}', generate 3 short and clear related questions "
            "that will help them explore the Bible further. Keep them natural and easy to understand."
        )
        related_resp = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": "You are an assistant that generates related questions."},
                {"role": "user", "content": related_prompt}
            ]
        )

        related_questions = [
            q.strip("-• \n") for q in related_resp.output_text.split("\n") if q.strip()
        ]

        return {
            "answer": answer_text,
            "related_questions": related_questions
        }

    except Exception as e:
        return {"error": str(e)}
