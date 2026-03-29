import os
from fastapi import FastAPI, HTTPException  # FastAPI is just like express
from pydantic import BaseModel              # BaseModel = Zod schema / TypeScript Interface
from google import genai                    # The official Google AI SDK
from google.genai import errors             # For catching specific API errors
from dotenv import load_dotenv              # Exact same as JS: require('dotenv').config()

# 1. Load environment variables from .env file into the OS environment
load_dotenv()

# 2. Initialize the Gemini Client
# JS Equivalent: const client = new genai.Client({ apiKey: process.env.GEMINI_API_KEY })
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 3. Create the FastAPI app instance
# JS Equivalent: const app = express()
app = FastAPI()

# 4. Define the Request Body Schema
# JS Equivalent: interface AskRequest { question: string }
# FastAPI automatically validates that the incoming JSON has a 'question' key that is a string.
class AskRequest(BaseModel):
    question: str

# 5. Define the Route
# JS Equivalent: app.post("/ask", async (req, res) => { ... })
# The '@' is a decorator. It links the URL path to the function directly beneath it.
@app.post("/ask")
async def ask_gemini(request: AskRequest):
    print(f"Asking Gemini: {request.question}")
    
    # 6. Error Handling
    try:
        # Generate the response using the model and the question provided
        # JS Equivalent: await client.models.generateContent({ model: "...", contents: "..." })
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=request.question
        )
        
        # 7. Return JSON
        # FastAPI automatically converts Python dictionaries (dicts) into JSON.
        # JS Equivalent: res.json({ question: ..., answer: ... })
        return {
            "question": request.question,
            "answer": response.text,
        }
        
    except errors.ClientError as e:
        # If Gemini rejects our request (like hitting a rate limit / 429)
        print(f"API Error: {e}")
        
        # Throw an HTTP Exception
        # JS Equivalent: res.status(429).json({ detail: "..." })
        raise HTTPException(
            status_code=429, 
            detail="Gemini API Quota Exceeded. Check VPN or wait 1 minute."
        )
