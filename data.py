from datetime import datetime, timedelta
import random
from typing import List
from models import Customer, Transaction

# Sample customer data
SAMPLE_SAMPLE_CUSTOMER = Customer(
    customer_id="CUST001",
    name="Kalpit Jain",
    account_number="****1234",
    account_type="savings",
    email="kalpit.jain@email.com",
    phone="+91934567890",
    joining_date="2020-01-15"
)

# Transaction categories with typical amounts and frequencies
TRANSACTION_CATEGORIES = {
    "Groceries": {
        "merchants": ["Big Bazaar", "Reliance Fresh", "DMart", "Spencer's", "Local Kirana"],
        "amount_range": (300, 3000),
        "frequency": "high",  # Multiple times per week
        "type": "debit"
    },
    "Utilities": {
        "merchants": ["Tata Power", "Adani Electricity", "BSNL", "MTNL", "Municipal Water"],
        "amount_range": (500, 3000),
        "frequency": "monthly",
        "type": "debit"
    },
    "Entertainment": {
        "merchants": ["PVR Cinemas", "BookMyShow", "Hotstar", "Netflix India", "JioSaavn"],
        "amount_range": (100, 1500),
        "frequency": "medium",
        "type": "debit"
    },
    "Transport": {
        "merchants": ["Ola", "Uber", "Indian Railways", "Delhi Metro", "Petrol Pump"],
        "amount_range": (50, 1000),
        "frequency": "high",
        "type": "debit"
    },
    "Dining": {
        "merchants": ["Swiggy", "Zomato", "Barbeque Nation", "Cafe Coffee Day", "Local Dhaba"],
        "amount_range": (150, 2500),
        "frequency": "high",
        "type": "debit"
    },
    "Shopping": {
        "merchants": ["Amazon India", "Flipkart", "Myntra", "Reliance Trends", "Croma", "Tanishq"],
        "amount_range": (500, 10000),
        "frequency": "medium",
        "type": "debit"
    },
    "Healthcare": {
        "merchants": ["Apollo Pharmacy", "Practo", "Fortis Hospital", "Max Healthcare", "Local Clinic"],
        "amount_range": (200, 5000),
        "frequency": "low",
        "type": "debit"
    },
    "Subscriptions": {
        "merchants": ["Hotstar Premium", "Amazon Prime India", "JioFiber", "Airtel Xstream", "Gym Membership"],
        "amount_range": (100, 1000),
        "frequency": "monthly",
        "type": "debit"
    },
    "Salary": {
        "merchants": ["Employer Direct Deposit"],
        "amount_range": (30000, 150000),
        "frequency": "monthly",
        "type": "credit"
    },
    "Rent": {
        "merchants": ["Landlord", "Property Management"],
        "amount_range": (8000, 35000),
        "frequency": "monthly",
        "type": "debit"
    }
}

PAYMENT_METHODS = ["card", "UPI", "NEFT", "cash", "direct_debit"]


def generate_sample_transactions():
    """Generate sample transactions for the current year, month, and week"""
    transactions = []
    current_date = datetime.now()
    start_date = datetime(current_date.year, 1, 1)
    
    next_transaction_id = 1
    account_balance = 10000.0
    
    # Generate transactions from January 1st to current date
    current_day = start_date
    
    while current_day <= current_date:
        # Determine how many transactions for this day
        daily_transaction_count = 0
        
        # Check for monthly recurring expenses (rent, utilities, subscriptions)
        if current_day.day == 1:  # First of month
            # Salary
            transactions.append(create_transaction(
                next_transaction_id, current_day, "Salary", account_balance
            ))
            account_balance += transactions[-1].amount
            next_transaction_id += 1
            
        if current_day.day == 5:  # Rent due
            transactions.append(create_transaction(
                next_transaction_id, current_day, "Rent", account_balance
            ))
            account_balance += transactions[-1].amount
            next_transaction_id += 1
            
        if current_day.day == 10:  # Utilities
            for utility in ["Utilities", "Subscriptions"]:
                if random.random() > 0.3:  # 70% chance
                    transactions.append(create_transaction(
                        next_transaction_id, current_day, utility, account_balance
                    ))
                    account_balance += transactions[-1].amount
                    next_transaction_id += 1
        
        # Daily random transactions
        # Weekdays: more transactions
        if current_day.weekday() < 5:  # Monday-Friday
            daily_transaction_count = random.randint(2, 5)
        else:  # Weekend
            daily_transaction_count = random.randint(1, 3)
        
        for _ in range(daily_transaction_count):
            # Random category weighted by frequency
            category = random.choices(
                list(TRANSACTION_CATEGORIES.keys()),
                weights=[
                    3 if t["frequency"] == "high" else 
                    2 if t["frequency"] == "medium" else 
                    0.5 if t["frequency"] == "low" else 0.3
                    for t in TRANSACTION_CATEGORIES.values()
                ],
                k=1
            )[0]
            
            # Skip monthly items here (already added above)
            if category in ["Salary", "Rent", "Utilities", "Subscriptions"]:
                if current_day.day not in [1, 5, 10]:
                    continue
            
            transactions.append(create_transaction(
                next_transaction_id, current_day, category, account_balance
            ))
            account_balance += transactions[-1].amount
            next_transaction_id += 1
        
        current_day += timedelta(days=1)
    
    # Sort by date
    transactions.sort(key=lambda x: x.date)
    
    return transactions


def create_transaction(transaction_id: int, date: datetime, category: str, current_balance: float) -> Transaction:
    """Create a single transaction"""
    if category not in TRANSACTION_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    
    template = TRANSACTION_CATEGORIES[category]
    merchant = random.choice(template["merchants"])
    amount_range = template["amount_range"]
    amount = round(random.uniform(amount_range[0], amount_range[1]), 2)
    
    # Debit transactions are negative
    if template["type"] == "debit":
        amount = -amount
    
    new_balance = round(current_balance + amount, 2)
    
    # Prevent negative balances (optional safety check)
    if new_balance < 0:
        new_balance = 0
    
    payment_method = random.choice(PAYMENT_METHODS) if template["type"] != "credit" else "direct_deposit"
    
    return Transaction(
        transaction_id=f"TXN{transaction_id:06d}",
        date=date.strftime("%Y-%m-%d"),
        description=f"{merchant} - {category}",
        amount=amount,
        category=category,
        transaction_type=template["type"],
        balance=new_balance,
        merchant=merchant,
        payment_method=payment_method
    )


# Generate all transactions
SAMPLE_TRANSACTIONS = generate_sample_transactions()


def get_customer() -> Customer:
    """Get customer details"""
    return SAMPLE_CUSTOMER


def get_all_transactions() -> List[Transaction]:
    """Get all transactions"""
    return SAMPLE_TRANSACTIONS


def get_transactions_by_date_range(start_date: str, end_date: str) -> List[Transaction]:
    """Get transactions within a date range"""
    try:
        # Validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    if start_date > end_date:
        raise ValueError("start_date must be before or equal to end_date")
    
    return [
        transaction for transaction in SAMPLE_TRANSACTIONS 
        if start_date <= transaction.date <= end_date
    ]


def get_current_month_transactions() -> List[Transaction]:
    """Get transactions for current month"""
    current_date = datetime.now()
    start_date = datetime(current_date.year, current_date.month, 1).strftime("%Y-%m-%d")
    end_date = current_date.strftime("%Y-%m-%d")
    return get_transactions_by_date_range(start_date, end_date)


def get_current_week_transactions() -> List[Transaction]:
    """Get transactions for current week"""
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    start_date = start_of_week.strftime("%Y-%m-%d")
    end_date = current_date.strftime("%Y-%m-%d")
    return get_transactions_by_date_range(start_date, end_date)


def get_current_year_transactions() -> List[Transaction]:
    """Get transactions for current year"""
    current_date = datetime.now()
    start_date = datetime(current_date.year, 1, 1).strftime("%Y-%m-%d")
    end_date = current_date.strftime("%Y-%m-%d")
    return get_transactions_by_date_range(start_date, end_date)
