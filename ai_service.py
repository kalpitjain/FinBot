import json
import logging
from typing import Dict, Optional
from openai import OpenAI
from config import OPENAI_API_KEY, SYSTEM_PROMPT
from data import get_customer, get_all_transactions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client with error handling
try:
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not configured")
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None


def prepare_context_data() -> Dict:
    """Prepare customer and transaction data as context for the AI"""
    try:
        customer_info = get_customer()
        all_transactions = get_all_transactions()
        
        # Convert to JSON for context
        customer_data = customer_info.model_dump()
        transactions_data = [transaction.model_dump() for transaction in all_transactions]
        
        context = {
            "customer": customer_data,
            "transactions": transactions_data,
            "transaction_count": len(transactions_data),
            "date_range": {
                "start": transactions_data[0]["date"] if transactions_data else None,
                "end": transactions_data[-1]["date"] if transactions_data else None
            }
        }
        
        return context
    except Exception as e:
        logger.error(f"Error preparing context data: {e}")
        return {
            "customer": {},
            "transactions": [],
            "transaction_count": 0,
            "date_range": {"start": None, "end": None}
        }


async def process_query(query: str) -> Dict:
    """
    Process user query using OpenAI GPT with transaction context
    Returns response text and optional chart data
    """
    # Validate input
    if not query or not query.strip():
        return {
            "response": "Please provide a valid query."
        }
    
    # Check if OpenAI client is available
    if client is None:
        return {
            "response": "AI service is not available. Please check the OpenAI API key configuration."
        }
    
    # Prepare context
    context = prepare_context_data()
    
    # Create user message with context
    user_message = f"""User Query: {query}

Customer Details:
{json.dumps(context['customer'], indent=2)}

Transaction Data Summary:
- Total transactions: {context['transaction_count']}
- Date range: {context['date_range']['start']} to {context['date_range']['end']}

Recent Transactions (last 50):
{json.dumps(context['transactions'][-50:], indent=2)}

Please analyze this data and respond to the user's query with clear insights and analysis."""
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1",  
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=2000,
            timeout=30.0
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("Empty response from OpenAI API")
        
        response_text = response.choices[0].message.content
        
        return {
            "response": response_text.strip()
        }
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        error_message = str(e)
        
        # Provide more user-friendly error messages
        if "rate_limit" in error_message.lower():
            user_message = "API rate limit exceeded. Please try again in a moment."
        elif "authentication" in error_message.lower() or "api_key" in error_message.lower():
            user_message = "API authentication failed. Please check the API key configuration."
        elif "timeout" in error_message.lower():
            user_message = "Request timed out. Please try again."
        else:
            user_message = f"I encountered an error processing your request. Please try again."
        
        return {
            "response": user_message
        }
