from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.schemas import WebhookMessage, TelexResponse
from app.agent.core import process_telex_message, get_ai_response
import os

# Initialize FastAPI app
app = FastAPI(
    title="Telex.im AI Code Helper Agent",
    description="Backend for the AI agent to provide code reviews and explanations via Telex.im webhooks.",
    version="1.0.0"
)

# Root Endpoint for Health Check
@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """Simple endpoint to verify the server is running."""
    return {"status": "Agent is running successfully!", "service": "AI Code Reviewer"}

# Main Webhook Endpoint
@app.post("/webhook", response_model=TelexResponse, status_code=status.HTTP_200_OK)
async def telex_webhook_handler(message: WebhookMessage):
    """
    Receives the message payload from Telex.im and sends an AI-generated response back.
    """
    
    # 1. Process the incoming message with the AI logic
    ai_response_content = process_telex_message(message)
    
    # 2. Construct the outgoing response payload (A2A Protocol)
    # The platform expects a JSON response to send the message back to the user/channel.
    response_payload = TelexResponse(
        channel_id=message.channel_id,
        recipient_id=message.sender_id, # Target the original sender
        content=ai_response_content
    )
    
    # 3. Return the payload. FastAPI automatically converts the Pydantic model to JSON.
    return response_payload

@app.get("/test-llm", status_code=status.HTTP_200_OK)
async def test_llm_connection():
    """
    Test endpoint to verify LLM connection and basic functionality.
    Returns a simple response from the LLM to confirm it's working.
    """
    try:
        # Test with a simple prompt
        test_prompt = "Hello! Are you working? Please respond with a short confirmation that you're operational."
        response = get_ai_response(test_prompt)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "llm_response": response,
                "message": "LLM connection is working correctly!"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM service error: {str(e)}"
        )

# Uvicorn command to run: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1