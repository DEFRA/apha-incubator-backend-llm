#!/usr/bin/env python
"""
Example usage of the Text Summarisation API with different scenarios.
This script demonstrates various use cases and integration patterns.
"""
import requests
import json
from typing import Optional


class SummarisationAPIClient:
    """Client for interacting with the Text Summarisation API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the API client."""
        self.base_url = base_url

    def health_check(self) -> dict:
        """Check if the API is healthy."""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def summarise(self, text: str, max_length: int = 100) -> dict:
        """
        Summarise text using the API.

        Args:
            text: The text to summarise
            max_length: Maximum length of summary in words (50-1000)

        Returns:
            Dictionary containing the summary and metadata
        """
        payload = {
            "text": text,
            "max_length": max_length
        }
        response = requests.post(f"{self.base_url}/summarise", json=payload)
        response.raise_for_status()
        return response.json()

    def get_config(self) -> dict:
        """Get API configuration."""
        response = requests.get(f"{self.base_url}/config")
        response.raise_for_status()
        return response.json()


def example_simple_summarisation():
    """Example 1: Simple text summarisation."""
    print("\n" + "=" * 60)
    print("Example 1: Simple Text Summarisation")
    print("=" * 60)

    client = SummarisationAPIClient()

    text = """
    The Amazon rainforest, often referred to as the "lungs of the Earth," 
    plays a critical role in global climate regulation. Spanning over 5.5 million 
    square kilometers across nine countries, with Brazil containing about 60% of it, 
    the rainforest is home to approximately 10% of all species on Earth. 
    Recent studies have shown that deforestation threatens not only the biodiversity 
    of the region but also its ability to absorb carbon dioxide from the atmosphere.
    """

    result = client.summarise(text, max_length=50)
    
    print(f"\nOriginal text length: {len(text)} characters")
    print(f"Summary length: {len(result['summary'])} characters")
    print(f"\nSummary: {result['summary']}")
    print(f"\nTokens used - Input: {result['input_tokens']}, Output: {result['output_tokens']}")


def example_batch_processing():
    """Example 2: Processing multiple documents."""
    print("\n" + "=" * 60)
    print("Example 2: Batch Processing Multiple Documents")
    print("=" * 60)

    client = SummarisationAPIClient()

    documents = [
        "Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models.",
        "Quantum computing represents a fundamental shift in computational capabilities using quantum bits or qubits.",
        "Blockchain technology enables secure, decentralized transactions without intermediaries through cryptographic techniques."
    ]

    for i, doc in enumerate(documents, 1):
        print(f"\n--- Document {i} ---")
        result = client.summarise(doc, max_length=30)
        print(f"Summary: {result['summary']}")


def example_variable_summary_lengths():
    """Example 3: Generating summaries of different lengths."""
    print("\n" + "=" * 60)
    print("Example 3: Variable Summary Lengths")
    print("=" * 60)

    client = SummarisationAPIClient()

    text = """
    Artificial intelligence has transformed healthcare in unprecedented ways. 
    From diagnostic imaging using deep learning to drug discovery accelerated by machine learning, 
    AI applications are improving patient outcomes and reducing healthcare costs. 
    Natural language processing enables analysis of medical literature and patient records at scale. 
    Robotic surgery systems, guided by AI, perform complex procedures with precision. 
    Predictive analytics help identify high-risk patients for early intervention. 
    Despite these advances, ethical considerations around data privacy and algorithmic bias remain important challenges.
    """

    lengths = [30, 75, 150]

    for length in lengths:
        print(f"\n--- Summary with max {length} words ---")
        result = client.summarise(text, max_length=length)
        print(f"Generated: {result['summary']}")


def example_error_handling():
    """Example 4: Error handling and validation."""
    print("\n" + "=" * 60)
    print("Example 4: Error Handling & Validation")
    print("=" * 60)

    client = SummarisationAPIClient()

    # Test 1: Empty text
    print("\nTest 1: Empty text (should fail)")
    try:
        result = client.summarise("")
    except requests.exceptions.HTTPError as e:
        print(f"✓ Correctly rejected: {e.response.status_code}")

    # Test 2: Invalid max_length (too small)
    print("\nTest 2: Invalid max_length < 50 (should fail)")
    try:
        result = client.summarise("Test text", max_length=10)
    except requests.exceptions.HTTPError as e:
        print(f"✓ Correctly rejected: {e.response.status_code}")

    # Test 3: Invalid max_length (too large)
    print("\nTest 3: Invalid max_length > 1000 (should fail)")
    try:
        result = client.summarise("Test text", max_length=2000)
    except requests.exceptions.HTTPError as e:
        print(f"✓ Correctly rejected: {e.response.status_code}")

    # Test 4: Valid request
    print("\nTest 4: Valid request (should succeed)")
    result = client.summarise("This is a test document about machine learning and AI.", max_length=50)
    print(f"✓ Success: {result['summary']}")


def example_token_tracking():
    """Example 5: Track token usage for cost estimation."""
    print("\n" + "=" * 60)
    print("Example 5: Token Usage Tracking")
    print("=" * 60)

    client = SummarisationAPIClient()

    texts = [
        ("Short", "AI is transforming industries."),
        ("Medium", "Artificial intelligence has become increasingly important in modern society. AI systems can process vast amounts of data to identify patterns and make predictions."),
        ("Long", "Artificial intelligence has become increasingly important in modern society. AI systems can process vast amounts of data to identify patterns and make predictions. Machine learning, a subset of AI, enables computers to learn from data without being explicitly programmed. Deep learning uses neural networks to process complex patterns. Natural language processing allows computers to understand and generate human language. Computer vision enables machines to interpret visual information. These technologies are revolutionizing healthcare, finance, education, transportation, and many other fields.")
    ]

    total_input = 0
    total_output = 0

    for label, text in texts:
        result = client.summarise(text, max_length=50)
        total_input += result['input_tokens']
        total_output += result['output_tokens']
        print(f"\n{label}:")
        print(f"  Input tokens: {result['input_tokens']}")
        print(f"  Output tokens: {result['output_tokens']}")
        print(f"  Summary: {result['summary']}")

    print(f"\n--- Total Token Usage ---")
    print(f"Total input tokens: {total_input}")
    print(f"Total output tokens: {total_output}")
    print(f"Total tokens: {total_input + total_output}")


def example_production_scenario():
    """Example 6: Production-like scenario - CDP data processing."""
    print("\n" + "=" * 60)
    print("Example 6: Production Scenario - CDP Data Processing")
    print("=" * 60)

    client = SummarisationAPIClient()

    # Check API health first
    try:
        health = client.health_check()
        print(f"\n✓ API Status: {health['status']}")
        print(f"  Model: {health['model']}")
    except Exception as e:
        print(f"✗ API Health Check Failed: {e}")
        return

    # Process customer feedback data
    customer_feedbacks = [
        "The product quality has improved significantly. However, the shipping time is too long. Customer support was helpful but slow to respond.",
        "Great experience with the purchase. Packaging was excellent. The item arrived faster than expected. Would recommend to others.",
        "Disappointed with the product durability. It broke after two weeks of normal use. Return process was complicated."
    ]

    print("\n--- Processing Customer Feedback (CDP Use Case) ---")

    for i, feedback in enumerate(customer_feedbacks, 1):
        try:
            result = client.summarise(feedback, max_length=40)
            print(f"\nFeedback {i}:")
            print(f"  Original: {feedback}")
            print(f"  Summary: {result['summary']}")
            print(f"  Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
        except Exception as e:
            print(f"✗ Error processing feedback {i}: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Text Summarisation API - Usage Examples")
    print("=" * 60)
    print("\nMake sure the API is running before executing examples:")
    print("python -m uvicorn src.main:app --reload")

    try:
        # Run examples
        example_simple_summarisation()
        example_batch_processing()
        example_variable_summary_lengths()
        example_error_handling()
        example_token_tracking()
        example_production_scenario()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60 + "\n")

    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the API")
        print("  Make sure the API is running: python -m uvicorn src.main:app --reload")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
