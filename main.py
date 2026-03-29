import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
app = FastAPI()

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_gemini(request: AskRequest):
    print(f"Asking Gemini: {request.question}")
    
    # Python's version of try/catch
    try:
        # Switching to 1.5-flash to bypass the limit: 0 issue
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=request.question
        )
        return {
            "question": request.question,
            "answer": response.text,
        }
    except errors.ClientError as e:
        # If Gemini rejects our request, we return a nice HTTP error instead of crashing
        # Like: res.status(429).json({ error: "..." })
        print(f"API Error: {e}")
        raise HTTPException(status_code=429, detail="Gemini API Quota Exceeded. Check VPN or wait 1 minute.")
