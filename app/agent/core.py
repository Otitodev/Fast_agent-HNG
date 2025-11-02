import os
from typing import Optional
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from app.schemas import WebhookMessage
from app.exceptions import LLMServiceError, ValidationError
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# --- Initialize the Mistral Client ---
client: Optional[MistralClient] = None
MODEL_NAME: str = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

def initialize_llm_client() -> None:
    """Initialize the Mistral client with proper error handling"""
    global client
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise LLMServiceError("MISTRAL_API_KEY environment variable is not set")
    
    try:
        client = MistralClient(api_key=api_key)
    except Exception as e:
        raise LLMServiceError(f"Failed to initialize Mistral client: {str(e)}")

# Initialize client on import
try:
    initialize_llm_client()
except LLMServiceError as e:
    print(f"Warning: {e}")
    client = None


def get_ai_response(user_input: str) -> str:
    """
    Invokes the Mistral LLM to get an AI-driven response.
    
    Args:
        user_input: The input text to send to the LLM
        
    Returns:
        str: The generated response from the LLM
        
    Raises:
        LLMServiceError: If there's an issue with the LLM service
        ValidationError: If the input is invalid
    """
    if not user_input or not isinstance(user_input, str):
        raise ValidationError("Input must be a non-empty string")
        
    if not client:
        try:
            initialize_llm_client()
        except LLMServiceError as e:
            raise LLMServiceError("LLM service is currently unavailable") from e

    try:
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
            if not response.choices or not response.choices[0].message.content:
                raise LLMServiceError("Received empty response from LLM service")
                
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise LLMServiceError(
                f"Failed to get response from LLM service: {str(e)}",
                details={"model": MODEL_NAME, "error_type": type(e).__name__}
            )
    except Exception as e:
        # Catch any other unexpected errors
        raise LLMServiceError("An unexpected error occurred while processing your request") from e

def process_telex_message(message: WebhookMessage) -> str:
    """
    Process incoming Telex message and generate an AI response.
    
    Args:
        message: The incoming webhook message from Telex
        
    Returns:
        str: The generated response
        
    Raises:
        ValidationError: If the message is invalid
        LLMServiceError: If there's an issue with the LLM service
    """
    if not message or not message.content:
        raise ValidationError("Empty message received")
        
    print(f"Agent Processing: Message from {message.sender_id} in channel {message.channel_id}")
    
    try:
        # Process the message content with the LLM
        return get_ai_response(message.content)
    except Exception as e:
        # Log the error and provide a user-friendly message
        error_msg = f"Error processing message: {str(e)}"
        print(error_msg)
        raise