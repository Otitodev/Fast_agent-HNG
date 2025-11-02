import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from app.schemas import WebhookMessage
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# --- Initialize the Mistral Client ---
# Assumes MISTRAL_API_KEY is set in your environment
try:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    # Use a faster, powerful model optimized for function calling and chat
    MODEL_NAME = "mistral-large-latest" 
    # Alternative: "mistral-small-latest" for lower latency/cost
except Exception as e:
    print(f"Error initializing Mistral client: {e}")
    client = None
    MODEL_NAME = "fallback"


def get_ai_response(user_input: str) -> str:
    """Invokes the Mistral LLM to get an AI-driven response."""
    
    if not client:
        return "ERROR: Mistral client not initialized. Check MISTRAL_API_KEY."

    # Define the agent's persona and instructions
    system_prompt = (
        "You are an **AI Code Reviewer and Helper Agent** for a developer platform. "
        "Your task is to analyze the user's input, which is often a code snippet. "
        "Based on the input, you should either: "
        "1. Provide a concise, constructive review, suggesting improvements for best practices, or "
        "2. Explain the code's purpose, or "
        "3. Answer a question related to the provided code. "
        "Keep your response professional, helpful, and format code using markdown blocks."
    )
    
    # Prepare the message payload for Mistral
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_input)
    ]
    
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=messages
        )
        # Extract the content from the response object
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Handle API errors gracefully
        return f"🚨 Sorry, the Mistral AI service encountered an error using {MODEL_NAME}. Details: {e}"

def process_telex_message(message: WebhookMessage) -> str:
    """
    Main function to process the incoming Telex message and get the agent's response.
    """
    print(f"Agent Processing: Message from {message.sender_id} in channel {message.channel_id}")
    
    # Get response from the core AI engine
    ai_response_text = get_ai_response(message.content)
    
    return ai_response_text