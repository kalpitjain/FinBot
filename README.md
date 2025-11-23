# FinBot - Intelligent Financial Assistant 💰

An AI-powered financial chatbot built with FastAPI, React, and OpenAI GPT-4 that analyzes bank transactions and provides personalized financial insights.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![React](https://img.shields.io/badge/React-18-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178c6)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)

## ✨ Features

- 💬 **Natural Language Chat** - Ask questions in plain English
- � **Dynamic Data Fetching** - GPT intelligently fetches only the data you need (e.g., "last 1 month", "this week", "Jan to March")
- 📊 **Transaction Analysis** - Automatic categorization and insights
- 📈 **Spending Patterns** - Identify trends and unusual expenses
- 🔍 **Category Breakdown** - See where your money goes
- 🎯 **Smart Recommendations** - AI-powered financial advice
- 📱 **Responsive Design** - Works on desktop and mobile
- 🔒 **Privacy First** - All data stays local (sample data used)
- 🛠️ **OpenAI Function Calling** - GPT uses tools to fetch precise data based on your queries

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd FinBot
```

2. **Set up the Backend**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create environment file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

3. **Set up the Frontend**
```bash
cd frontend
npm install
cd ..
```

### Running the Servers

#### Option 1: Two Separate Terminals (Recommended for Development)

**Terminal 1 - Backend Server:**
```bash
# From the project root directory
python main.py
```
The backend will start at `http://localhost:8000`

**Terminal 2 - Frontend Development Server:**
```bash
cd frontend
npm run dev
```
The frontend will start at `http://localhost:5173`

#### Option 2: Using Uvicorn (Alternative Backend Start)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Accessing the Application

Once both servers are running:
- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
FinBot/
├── main.py                # FastAPI application & API endpoints
├── ai_service.py          # OpenAI GPT-4 integration
├── config.py              # Environment variables & system prompt
├── models.py              # Pydantic data models
├── data.py                # Sample transaction data generator
├── requirements.txt       # Python dependencies
├── .env                   # Your API keys (create this)
└── frontend/
    ├── src/
    │   ├── App.tsx                    # Root component
    │   ├── main.tsx                   # Entry point
    │   ├── components/
    │   │   ├── Chatbot.tsx           # Main chat interface
    │   │   ├── ChatArea.tsx          # Chat display area
    │   │   ├── ChatInput.tsx         # Message input
    │   │   ├── Messages.tsx          # Message list
    │   │   ├── MessageBubble.tsx     # Individual message
    │   │   └── ErrorBoundary.tsx     # Error handling
    │   ├── types/
    │   │   └── MessageType.ts        # TypeScript types
    │   └── utils/
    │       └── apiHandler.ts         # API communication
    ├── package.json
    ├── tsconfig.json
    └── vite.config.ts
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI GPT-4** - AI language model
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python-dotenv** - Environment management

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Axios** - HTTP client
- **CSS3** - Styling

## 🔧 Configuration

### Backend Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=sk-your-actual-openai-api-key

# Optional (defaults shown)
# PORT=8000
# HOST=0.0.0.0
```

### Frontend Environment Variables (frontend/.env)
```bash
# Optional - defaults to localhost:8000
VITE_APP_API_URL=http://localhost:8000
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/getBotResponse` | Main chat endpoint - send query, get AI response |
| `GET` | `/health` | Health check - verify server is running |

## 🤖 How It Works - Dynamic Data Fetching

FinBot uses **OpenAI Function Calling** (Tools API) to dynamically fetch transaction data based on user queries. Instead of sending all transaction data in every request, GPT intelligently calls the appropriate function to retrieve only the data it needs.

### Available Functions

The AI has access to these data-fetching functions:

1. **get_customer_info()** - Retrieves customer account details
2. **get_current_week_transactions()** - Gets this week's transactions
3. **get_current_month_transactions()** - Gets this month's transactions
4. **get_current_year_transactions()** - Gets this year's transactions
5. **get_transactions_last_n_days(days)** - Gets transactions from the last N days
6. **get_transactions_last_n_months(months)** - Gets transactions from the last N months
7. **get_transactions_by_date_range(start_date, end_date)** - Gets transactions between specific dates

### Example Queries

| User Query | Function Called | Description |
|------------|----------------|-------------|
| "Show me my spending last month" | `get_transactions_last_n_months(1)` | Fetches only last month's data |
| "What did I spend this week?" | `get_current_week_transactions()` | Fetches current week only |
| "Analyze my transactions from January to March" | `get_transactions_by_date_range("2025-01-01", "2025-03-31")` | Fetches specific date range |
| "Show me expenses from last 7 days" | `get_transactions_last_n_days(7)` | Fetches last 7 days |
| "What's my account info?" | `get_customer_info()` | Fetches customer details |

### Benefits

- ⚡ **Faster responses** - Only relevant data is fetched and processed
- 💰 **Cost efficient** - Reduces token usage by not sending unnecessary data
- 🎯 **More accurate** - GPT analyzes only the data period the user asked about
- 🔄 **Flexible** - Works with any time period or date range


## 🧪 Development

### Backend Development
```bash
# Run with auto-reload
source venv/bin/activate 
uvicorn main:app --reload

# View logs
python main.py  # Shows INFO level logs
```

### Frontend Development
```bash
cd frontend

# Start dev server
npm run dev

# Type checking
npm run build

# Linting
npm run lint
```