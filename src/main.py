"""FastAPI backend for text summarisation using AWS Bedrock."""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config import settings
from src.models import SummariseRequest, SummariseResponse, ErrorResponse
from src.bedrock_summarizer import get_summariser

# Initialize FastAPI app
app = FastAPI(
    title="Text Summarisation API",
    description="A backend API for summarising text using AWS Bedrock",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Check API health status."""
    return {
        "status": "healthy",
        "service": "text-summarisation-api",
        "model": settings.bedrock_model_id,
    }


@app.post(
    "/summarise",
    response_model=SummariseResponse,
    tags=["Summarisation"],
    status_code=status.HTTP_200_OK,
)
async def summarise(request: SummariseRequest) -> SummariseResponse:
    """
    Summarise the provided text using AWS Bedrock.

    Args:
        request: SummariseRequest containing the text to summarise

    Returns:
        SummariseResponse containing the summary and metadata

    Raises:
        HTTPException: If summarisation fails
    """
    try:
        # Get the summariser instance
        summariser = get_summariser()

        # Perform summarisation (model_id override is optional)
        result = summariser.summarise(request.text, request.max_length, request.model_id)

        # Return formatted response
        return SummariseResponse(
            original_text=request.text,
            summary=result["summary"],
            model=result["model"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to summarise text. Check AWS credentials and configuration.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during summarisation.",
        )


@app.get("/config", tags=["Configuration"])
async def get_config() -> dict:
    """Get current API configuration (non-sensitive values only)."""
    return {
        "region": settings.aws_region,
        "model_id": settings.bedrock_model_id,
        "api_host": settings.api_host,
        "api_port": settings.api_port,
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detail": exc.detail,
            "code": f"HTTP_{exc.status_code}",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
    )
