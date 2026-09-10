"""Configuration management for the Summarisation API."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # AWS Configuration
    aws_bearer_token_bedrock: str = os.getenv("AWS_BEARER_TOKEN_BEDROCK", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    bedrock_model_id: str = os.getenv(
        "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
    )

    # API Configuration
    api_port: int = int(os.getenv("API_PORT", 8000))
    api_host: str = os.getenv("API_HOST", "0.0.0.0")

    def __init__(self):
        """Validate that required settings are present."""
        if not self.aws_bearer_token_bedrock:
            raise ValueError("AWS_BEARER_TOKEN_BEDROCK environment variable is required")

    @property
    def is_valid(self) -> bool:
        """Check if all required settings are configured."""
        return bool(self.aws_bearer_token_bedrock and self.aws_region)


# Global settings instance
settings = Settings()
