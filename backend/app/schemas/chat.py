"""Pydantic schemas for chat API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SendMessageRequest(BaseModel):
    """Request schema for sending a chat message."""

    content: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Message content (max 1000 characters)"
    )
    language: str = Field(
        default="en-US",
        pattern="^(en-US|ur-PK)$",
        description="Input language hint for voice input"
    )


class MessageResponse(BaseModel):
    """Response schema for a single message."""

    id: str = Field(..., description="Unique message identifier")
    role: str = Field(..., description="Message role: user, assistant, system")
    content: str = Field(..., description="Message content")
    agent_name: Optional[str] = Field(None, description="Name of responding agent")
    agent_icon: Optional[str] = Field(None, description="Icon of responding agent (emoji)")
    created_at: datetime = Field(..., description="When message was created")

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """Response schema for chat message with AI response."""

    message: MessageResponse = Field(..., description="The AI response message")
    agent_name: str = Field(..., description="Name of the responding agent")
    agent_icon: str = Field(..., description="Icon of the responding agent (emoji)")
    tool_calls: list[str] = Field(
        default_factory=list,
        description="List of MCP tools invoked during the request"
    )


class ConversationResponse(BaseModel):
    """Response schema for a conversation."""

    id: str = Field(..., description="Unique conversation identifier")
    title: Optional[str] = Field(None, description="AI-generated summary title")
    created_at: datetime = Field(..., description="When conversation was created")
    updated_at: datetime = Field(..., description="Last activity timestamp")

    class Config:
        from_attributes = True


class ConversationWithMessagesResponse(ConversationResponse):
    """Response schema for a conversation with its messages."""

    messages: list[MessageResponse] = Field(
        default_factory=list,
        description="List of messages in the conversation"
    )


class ConversationListResponse(BaseModel):
    """Response schema for listing conversations."""

    conversations: list[ConversationResponse] = Field(
        ..., description="List of conversations"
    )
    total: int = Field(..., description="Total number of conversations")
    limit: int = Field(..., description="Maximum results returned")
    offset: int = Field(..., description="Number of results skipped")


class TitleGenerationResponse(BaseModel):
    """Response schema for title generation."""

    title: str = Field(..., description="Generated conversation title")


class ErrorResponse(BaseModel):
    """Response schema for errors."""

    detail: str = Field(..., description="Error message")


class UnifiedChatRequest(BaseModel):
    """Request schema for unified chat endpoint.

    Creates a new conversation if conversation_id is not provided.
    """

    conversation_id: Optional[str] = Field(
        default=None,
        description="Existing conversation ID (creates new if not provided)"
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's natural language message (max 1000 characters)"
    )


class ToolCallInfo(BaseModel):
    """Information about an MCP tool call."""

    tool_name: str = Field(..., description="Name of the MCP tool invoked")
    success: bool = Field(..., description="Whether the tool call succeeded")


class UnifiedChatResponse(BaseModel):
    """Response schema for unified chat endpoint."""

    conversation_id: str = Field(..., description="The conversation ID")
    response: str = Field(..., description="AI assistant's response")
    tool_calls: list[ToolCallInfo] = Field(
        default_factory=list,
        description="List of MCP tools invoked during processing"
    )
    agent_name: str = Field(default="Aren", description="Name of the responding agent")
    agent_icon: str = Field(default="🤖", description="Icon of the responding agent")
