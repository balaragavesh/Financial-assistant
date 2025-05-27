# financial_agent.py

from openai import OpenAI
import requests
import json
from config import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODEL

# --- 🔑 GROQ CLIENT SETUP ---
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_API_BASE,
)

# --- 🔧 TOOL FUNCTIONS ---
def get_stock_price(symbol):
    try:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=07JCQY5TGG9TXGK7'
        response = requests.get(url).json()
        price = response['Global Quote']['05. price']
        return f"The current price of {symbol} is ${price}."
    except:
        return "Sorry, I couldn't retrieve the stock price."

def explain_financial_term(term):
    prompt = f"Explain the financial term '{term}' in simple terms."
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def summarize_news(news):
    prompt = f"Summarize the following financial news and explain its impact:\n{news}"
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- 📦 TOOL DEFINITIONS ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the current price of a stock symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g. AAPL, TSLA)"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "explain_financial_term",
            "description": "Explain a financial term in simple words",
            "parameters": {
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "Financial term like P/E ratio, EBITDA, etc."
                    }
                },
                "required": ["term"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_news",
            "description": "Summarize financial news and explain its impact",
            "parameters": {
                "type": "object",
                "properties": {
                    "news": {
                        "type": "string",
                        "description": "News headline or article to summarize"
                    }
                },
                "required": ["news"]
            }
        }
    }
]

# --- 🧠 AGENT FUNCTION ---
def run_agent(user_input):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        fn_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if fn_name == "get_stock_price":
            return get_stock_price(args["symbol"])
        elif fn_name == "explain_financial_term":
            return explain_financial_term(args["term"])
        elif fn_name == "summarize_news":
            return summarize_news(args["news"])

    return message.content or "I couldn't generate a response."

# --- 🖥️ CLI TEST RUNNER ---
if __name__ == "__main__":
    print("📊 Financial AI Copilot (Groq-Powered)\nType 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("🤖:", run_agent(user_input), "\n")
