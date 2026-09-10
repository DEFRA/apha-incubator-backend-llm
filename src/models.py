"""Data models for the summarisation API."""
from pydantic import BaseModel, Field


class SummariseRequest(BaseModel):
    """Request model for text summarisation."""

    text: str = Field(..., min_length=1, description="The text to summarise")
    max_length: int = Field(
        default=100, ge=50, le=1000, description="Maximum length of summary in words"
    )
    model_id: str | None = Field(
        default=None,
        description="Optional Bedrock model ID to use instead of the server default",
    )


class SummariseResponse(BaseModel):
    """Response model for text summarisation."""

    original_text: str = Field(..., description="The original input text")
    summary: str = Field(..., description="The generated summary")
    model: str = Field(..., description="The model used for summarisation")
    input_tokens: int = Field(default=0, description="Number of input tokens")
    output_tokens: int = Field(default=0, description="Number of output tokens")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: str = Field(default="", description="Additional error details")
    code: str = Field(default="INTERNAL_ERROR", description="Error code")
