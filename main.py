from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from models import BotRequest
from ai_service import process_query
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FinBot - Intelligent Financial Assistant",
    description="AI-powered financial chatbot for transaction analysis and insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/getBotResponse")
async def handle_chat_request(request: BotRequest):
    # Processes user queries and returns AI-generated responses
    try:
        # Validate input
        user_query = request.userAsk.strip()
        if not user_query:
            logger.warning("Received whitespace-only query")
            return {"success": False, "error": "Query cannot be empty"}
        
        # Limit query length
        if len(user_query) > 1000:
            logger.warning(f"Query too long: {len(user_query)} characters")
            return {"success": False, "error": "Query is too long. Please limit to 1000 characters."}
        
        logger.info(f"Processing query: {user_query[:50]}...")
        
        # Process the query using AI service
        result = await process_query(user_query)
        
        if not result or "response" not in result:
            logger.error("Invalid result from process_query")
            return {"success": False, "error": "Failed to process query"}
        
        return {
            "success": True,
            "response": result["response"]
        }
        
    except Exception as e:
        logger.error(f"Error in handle_chat_request: {e}", exc_info=True)
        return {"success": False, "error": f"Error processing request: {str(e)}"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "FinBot"}


@app.on_event("startup")
async def startup_event():
    # Run validation checks on startup
    logger.info("Starting FinBot API")
    from config import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        logger.warning("WARNING: OPENAI_API_KEY not configured. AI features will not work.")
    else:
        logger.info("OpenAI API key configured")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
