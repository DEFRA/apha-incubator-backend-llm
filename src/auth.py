#!/usr/bin/env python
"""
Bearer Token Authentication Middleware for AWS Bedrock.
This module handles short-term API key authentication using bearer tokens.
"""
import os
from typing import Optional
from fastapi import Request, HTTPException, status
from functools import wraps


class BearerTokenAuth:
    """Handle bearer token authentication for AWS Bedrock."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize bearer token authentication.

        Args:
            token: The bearer token for authentication (from environment if None)
        """
        self.token = token or os.getenv("AWS_BEARER_TOKEN_BEDROCK")
        if not self.token:
            raise ValueError("AWS_BEARER_TOKEN_BEDROCK is not configured")

    def verify_token(self, token: str) -> bool:
        """
        Verify the provided token matches the configured token.

        Args:
            token: The token to verify

        Returns:
            True if token is valid, False otherwise
        """
        return token == self.token

    async def verify_request(self, request: Request) -> bool:
        """
        Verify the authorization header in a request.

        Args:
            request: The HTTP request object

        Returns:
            True if authorization is valid

        Raises:
            HTTPException: If authorization fails
        """
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header. Use: Authorization: Bearer <token>",
            )

        token = auth_header[7:]  # Remove "Bearer " prefix

        if not self.verify_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid bearer token",
            )

        return True


def require_bearer_token(func):
    """
    Decorator to require bearer token authentication for FastAPI routes.

    Usage:
        @app.post("/protected")
        @require_bearer_token
        async def protected_route(request: Request):
            return {"message": "Authorized"}
    """

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth = BearerTokenAuth()
        await auth.verify_request(request)
        return await func(request, *args, **kwargs)

    return wrapper


# Example usage (not used in main API, but available for reference)
if __name__ == "__main__":
    # Test bearer token authentication
    auth = BearerTokenAuth("test-token-12345")

    # Valid token
    if auth.verify_token("test-token-12345"):
        print("✓ Valid token accepted")

    # Invalid token
    if not auth.verify_token("wrong-token"):
        print("✓ Invalid token rejected")
