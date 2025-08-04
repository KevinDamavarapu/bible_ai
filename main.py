import os
import logging
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Enable CORS for testing on phone/browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    logger.info(f"✅ OPENAI_API_KEY loaded (ending with ...{api_key[-4:]})")
else:
    logger.error("❌ OPENAI_API_KEY not found in environment!")

client = OpenAI(api_key=api_key)


@app.get("/")
def home():
    """Health check endpoint"""
    return {"message": "Bible AI is running!"}


@app.post("/bible")
def bible(query: str = Query(..., description="Enter your Bible question here")):
    """
    Ask Bible AI a question. Returns an AI-generated response based on the Bible.
    """
    try:
        logger.info(f"📖 Bible query received: {query}")

        # Call OpenAI
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Answer this based on the Bible: {query}",
        )

        answer = response.output_text
        logger.info(f"✅ Bible AI answered successfully.")
        return {"mode": "real", "answer": answer}

    except Exception as e:
        logger.error(f"❌ Error in /bible endpoint: {e}")
        return {"mode": "error", "error": str(e)}






