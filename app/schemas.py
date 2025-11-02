from pydantic import BaseModel, Field
from typing import Literal

# --- Incoming Webhook Message Model (Assumed Telex.im Payload) ---
class WebhookMessage(BaseModel):
    """Schema for the incoming message from Telex.im webhook."""
    
    # These fields are crucial for sending a response back
    channel_id: str = Field(..., description="The ID of the conversation channel.")
    sender_id: str = Field(..., description="The ID of the user who sent the message.")
    
    # The actual message content
    content: str = Field(..., description="The text content of the user's message (e.g., code snippet).")
    
    # A few other typical fields you might receive
    timestamp: str = None
    event_type: str = "message_received"


# --- Outgoing A2A Response Model (Response to Telex) ---
# NOTE: This is an *assumed* structure based on typical webhook responses. 
# Consult the Telex.im A2A documentation to verify the exact required keys.
class TelexResponse(BaseModel):
    """Schema for the JSON response the FastAPI app sends back to Telex.im."""

    channel_id: str
    recipient_id: str
    response_type: Literal["message"] = "message" # Indicates a text response
    content: str
    # You might need to add: flow_id, agent_name, execution_status, etc.