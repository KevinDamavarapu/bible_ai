from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
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

@app.get("/")
def home():
    return {"message": "Bible AI is running!"}

@app.post("/bible")
def bible(query: str = Query(..., description="Enter your Bible question here")):
    try:
        system_prompt = (
            "You are Bible AI, a helpful assistant that answers questions only based on the Bible. "
            "You must provide references from scripture when possible."
        )
        
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        
        return {"answer": response.output_text}
    
    except Exception as e:
        return {"error": str(e)}
