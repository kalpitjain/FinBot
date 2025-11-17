from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional
from datetime import datetime


class Customer(BaseModel):
    customer_id: str = Field(..., min_length=1, description="Unique customer identifier")
    name: str = Field(..., min_length=1, max_length=100)
    account_number: str = Field(..., min_length=1)
    account_type: Literal["savings", "current", "credit"]
    email: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    joining_date: str
    
    @field_validator('joining_date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v


class Transaction(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    date: str
    description: str = Field(..., min_length=1, max_length=500)
    amount: float
    category: str = Field(..., min_length=1, max_length=100)
    transaction_type: Literal["debit", "credit", "transfer"]
    balance: float = Field(..., ge=0, description="Balance must be non-negative")
    merchant: str = Field(..., min_length=1, max_length=200)
    payment_method: str = Field(..., min_length=1, max_length=50)
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v


class MessageType(BaseModel):
    text: str
    isUser: bool
    url: Optional[str] = None


class BotRequest(BaseModel):
    userAsk: str = Field(..., min_length=1, max_length=1000, description="User query")
    conversationHistory: List[MessageType] = Field(default_factory=list, max_length=100)