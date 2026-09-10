"""AWS Bedrock integration for text summarisation."""
import json
import logging
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from src.config import settings

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BedrockSummariser:
    """Handle text summarisation using AWS Bedrock."""

    def __init__(self):
        """Initialize Bedrock client with authentication."""
        self.region = settings.aws_region
        self.model_id = settings.bedrock_model_id
        self._bearer_token = settings.aws_bearer_token_bedrock
        
        logger.info(f"Initializing Bedrock Summariser for region: {self.region}")
        logger.info(f"Model ID: {self.model_id}")
        
        try:
            # Create Bedrock runtime client
            # The bearer token/credentials are typically from environment variables
            self.client = boto3.client(
                "bedrock-runtime",
                region_name=self.region,
            )
            logger.info("Bedrock client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            raise RuntimeError(f"Failed to initialize Bedrock client: {str(e)}")

    def summarise(self, text: str, max_length: int = 100, model_id: str | None = None) -> dict:
        """
        Summarise text using AWS Bedrock.

        Args:
            text: The text to summarise
            max_length: Maximum length of summary in words
            model_id: Optional model ID to use instead of the configured default

        Returns:
            Dictionary containing summary and token usage information
        """
        try:
            logger.debug(f"Starting summarisation for {len(text)} characters")

            # Allow callers to override the configured model per request
            invoke_model_id = model_id or self.model_id

            # Prepare the prompt for Claude
            prompt = self._prepare_prompt(text, max_length)
            logger.debug(f"Prompt prepared: {len(prompt)} characters")

            # Prepare the request body for Bedrock
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_length + 50,  # Add buffer for token count
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            }

            logger.debug(f"Invoking model: {invoke_model_id}")

            # Invoke the model using boto3
            response = self.client.invoke_model(
                modelId=invoke_model_id,
                body=json.dumps(request_body),
            )

            logger.debug(f"Model invoked successfully")

            # Parse the response
            response_body = json.loads(response["body"].read())
            logger.debug(f"Response parsed: {response_body.get('usage', {})}")

            # Extract summary and token usage
            summary = response_body["content"][0]["text"]
            input_tokens = response_body.get("usage", {}).get("input_tokens", 0)
            output_tokens = response_body.get("usage", {}).get("output_tokens", 0)

            logger.debug(f"Summarisation complete. Tokens: {input_tokens} in, {output_tokens} out")

            return {
                "summary": summary,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "model": invoke_model_id,
            }

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"Bedrock ClientError ({error_code}): {error_message}")
            
            if error_code == "ValidationException":
                raise RuntimeError(f"Invalid request parameters: {error_message}")
            elif error_code == "ThrottlingException":
                raise RuntimeError("Bedrock API is throttled, please try again later")
            elif error_code == "ResourceNotFoundException":
                raise RuntimeError(f"Model not found: {invoke_model_id}")
            elif error_code == "AccessDeniedException":
                raise RuntimeError("Access denied to Bedrock API. Check your AWS credentials and permissions.")
            else:
                raise RuntimeError(f"Bedrock API error: {error_message}")
                
        except BotoCoreError as e:
            logger.error(f"BotoCore error: {str(e)}")
            raise RuntimeError(f"AWS communication error: {str(e)}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Bedrock response: {str(e)}")
            raise RuntimeError(f"Failed to parse model response: {str(e)}")
            
        except KeyError as e:
            logger.error(f"Missing expected field in response: {str(e)}")
            raise RuntimeError(f"Unexpected response format from Bedrock: {str(e)}")
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise RuntimeError(f"Error invoking Bedrock model: {str(e)}")

    @staticmethod
    def _prepare_prompt(text: str, max_length: int) -> str:
        """
        Prepare the prompt for Claude.

        Args:
            text: The text to summarise
            max_length: Maximum length of summary in words

        Returns:
            The formatted prompt string
        """
        return f"""Please summarise the following text in approximately {max_length} words. 
Provide a clear, concise summary that captures the main points.

Text to summarise:
<text>
{text}
</text>

Summary:"""


# Singleton instance
_summariser_instance = None


def get_summariser() -> BedrockSummariser:
    """Get or create the BedrockSummariser instance."""
    global _summariser_instance
    if _summariser_instance is None:
        _summariser_instance = BedrockSummariser()
    return _summariser_instance
