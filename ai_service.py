import json
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from openai import OpenAI
from config import OPENAI_API_KEY, SYSTEM_PROMPT
from data import (
    get_customer, 
    get_all_transactions,
    get_transactions_by_date_range,
    get_current_month_transactions,
    get_current_week_transactions,
    get_current_year_transactions
)
from models import MessageType

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

# Define tools/functions for GPT to call
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_transactions_by_date_range",
            "description": "Get transactions within a specific date range. Use this when the user asks for transactions between specific dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    }
                },
                "required": ["start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_transactions_last_n_days",
            "description": "Get transactions for the last N days. Use this when the user asks for transactions from 'last N days' or 'past N days'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of days to look back"
                    }
                },
                "required": ["days"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_transactions_last_n_months",
            "description": "Get transactions for the last N months. Use this when the user asks for transactions from 'last N months' or 'past N months' or 'last 1 month'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "months": {
                        "type": "integer",
                        "description": "Number of months to look back"
                    }
                },
                "required": ["months"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_month_transactions",
            "description": "Get all transactions for the current month. Use this when the user asks for 'this month' or 'current month' transactions.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_week_transactions",
            "description": "Get all transactions for the current week. Use this when the user asks for 'this week' or 'current week' transactions.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_year_transactions",
            "description": "Get all transactions for the current year. Use this when the user asks for 'this year' or 'current year' or 'year to date' transactions.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_info",
            "description": "Get customer account details and information. Use this when the user asks about their account, profile, or personal details.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def execute_function(function_name: str, arguments: Dict) -> str:
    """Execute a function call from GPT and return the result as JSON string"""
    try:
        logger.info(f"Executing function: {function_name} with args: {arguments}")
        
        if function_name == "get_customer_info":
            customer = get_customer()
            return json.dumps(customer.model_dump(), indent=2)
        
        elif function_name == "get_current_month_transactions":
            transactions = get_current_month_transactions()
            return json.dumps([t.model_dump() for t in transactions], indent=2)
        
        elif function_name == "get_current_week_transactions":
            transactions = get_current_week_transactions()
            return json.dumps([t.model_dump() for t in transactions], indent=2)
        
        elif function_name == "get_current_year_transactions":
            transactions = get_current_year_transactions()
            return json.dumps([t.model_dump() for t in transactions], indent=2)
        
        elif function_name == "get_transactions_by_date_range":
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            transactions = get_transactions_by_date_range(start_date, end_date)
            return json.dumps([t.model_dump() for t in transactions], indent=2)
        
        elif function_name == "get_transactions_last_n_days":
            days = arguments.get("days")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            transactions = get_transactions_by_date_range(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            return json.dumps([t.model_dump() for t in transactions], indent=2)
        
        elif function_name == "get_transactions_last_n_months":
            months = arguments.get("months")
            end_date = datetime.now()
            # Calculate approximate start date (months * 30 days)
            start_date = end_date - timedelta(days=months * 30)
            transactions = get_transactions_by_date_range(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            return json.dumps([t.model_dump() for t in transactions], indent=2)
        
        else:
            return json.dumps({"error": f"Unknown function: {function_name}"})
    
    except Exception as e:
        logger.error(f"Error executing function {function_name}: {e}")
        return json.dumps({"error": str(e)})


async def process_query(query: str, conversation_history: List[MessageType] = None) -> Dict:
    """
    Process user query using OpenAI GPT with function calling for dynamic data fetching
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

    try:
        # Build messages array with conversation history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history:
                role = "user" if msg.isUser else "assistant"
                messages.append({"role": role, "content": msg.text})
        
        # Add current user message
        messages.append({"role": "user", "content": query})
        
        # Initialize conversation loop for function calling
        max_iterations = 5  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call OpenAI API with tools
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=2000,
                timeout=30.0
            )

            if not response.choices:
                raise ValueError("Empty response from OpenAI API")

            message = response.choices[0].message
            
            # Check if GPT wants to call a function
            if message.tool_calls:
                # Add assistant's message to conversation
                messages.append(message)
                
                # Process each tool call
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"GPT calling function: {function_name}")
                    
                    # Execute the function
                    function_result = execute_function(function_name, function_args)
                    
                    # Add function result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": function_result
                    })
                
                # Continue the loop to get GPT's response after function calls
                continue
            
            # No more function calls, we have the final response
            if message.content:
                return {
                    "response": message.content.strip()
                }
            else:
                raise ValueError("No content in final response")
        
        # Max iterations reached
        logger.warning(f"Max iterations ({max_iterations}) reached in function calling loop")
        return {
            "response": "I apologize, but I'm having trouble processing your request. Please try rephrasing your question."
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
