#!/usr/bin/env python3
"""
Test script to verify Hugging Face API connectivity and embedding generation.
Run from backend directory: python test_huggingface_api.py
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
EMBEDDING_URL = f"https://router.huggingface.co/hf-inference/models/{EMBEDDING_MODEL}"

async def test_huggingface_api():
    """Test Hugging Face API for embedding generation"""

    print("=" * 60)
    print("Hugging Face API Test")
    print("=" * 60)

    # Check if API key is set
    print(f"\n1. Checking API Key...")
    if not HUGGINGFACE_API_KEY:
        print("❌ ERROR: HUGGINGFACE_API_KEY environment variable not set!")
        print("   Set it in your .env file: HUGGINGFACE_API_KEY=your_key_here")
        return False

    print(f"✓ API Key found: {HUGGINGFACE_API_KEY[:8]}...{HUGGINGFACE_API_KEY[-4:]}")

    # Test API endpoint
    print(f"\n2. Testing API Endpoint...")
    print(f"   URL: {EMBEDDING_URL}")

    test_text = "This is a test document for embedding generation."

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"\n3. Sending request...")
            response = await client.post(
                EMBEDDING_URL,
                headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
                json={"inputs": test_text, "options": {"wait_for_model": True}}
            )

            print(f"   Status Code: {response.status_code}")

            if response.status_code != 200:
                print(f"\n❌ ERROR: Request failed!")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

            result = response.json()
            print(f"\n✓ Request successful!")
            print(f"   Response type: {type(result)}")

            # Parse embedding
            embedding = None
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    embedding = result[0]  # Nested: [[0.1, 0.2, ...]]
                    print(f"   Format: Nested list")
                else:
                    embedding = result  # Flat: [0.1, 0.2, ...]
                    print(f"   Format: Flat list")

            if embedding:
                print(f"   Embedding dimensions: {len(embedding)}")
                print(f"   First 5 values: {embedding[:5]}")
                print(f"\n✅ SUCCESS! Hugging Face API is working correctly!")
                return True
            else:
                print(f"\n❌ ERROR: Unexpected response format!")
                print(f"   Response: {result}")
                return False

    except httpx.TimeoutException:
        print(f"\n❌ ERROR: Request timed out!")
        print(f"   The API might be slow or unavailable.")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_huggingface_api())
    exit(0 if success else 1)
