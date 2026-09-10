#!/bin/bash
# API Testing Examples using curl
# Run these commands after starting the API server

echo "Text Summarisation API - curl Examples"
echo "========================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"

# Test 1: Health Check
echo -e "${BLUE}1. Health Check${NC}"
echo "Command: curl $API_URL/health"
echo ""
curl -s "$API_URL/health" | python -m json.tool
echo ""
echo ""

# Test 2: Get Configuration
echo -e "${BLUE}2. Get API Configuration${NC}"
echo "Command: curl $API_URL/config"
echo ""
curl -s "$API_URL/config" | python -m json.tool
echo ""
echo ""

# Test 3: Simple Summarisation
echo -e "${BLUE}3. Simple Text Summarisation${NC}"
echo "Command:"
echo "curl -X POST $API_URL/summarise \\"
echo '  -H "Content-Type: application/json" \'
echo '  -d \'{"text": "...", "max_length": 100}\''
echo ""
curl -s -X POST "$API_URL/summarise" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence has revolutionized multiple industries. From healthcare diagnostics to autonomous vehicles, AI is creating new possibilities. Machine learning algorithms process massive datasets to find patterns humans might miss. Natural language processing enables computers to understand human language. These technologies are improving efficiency and enabling new capabilities across sectors.",
    "max_length": 100
  }' | python -m json.tool
echo ""
echo ""

# Test 4: Long Text Summarisation
echo -e "${BLUE}4. Long Text Summarisation${NC}"
echo "Command: (Multi-sentence technical document)"
echo ""
curl -s -X POST "$API_URL/summarise" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Quantum computing represents a paradigm shift in computational capabilities. Unlike classical computers that use bits (0 or 1), quantum computers use quantum bits or qubits that can exist in superposition, allowing them to be both 0 and 1 simultaneously. This property enables quantum computers to explore multiple solutions in parallel, potentially solving certain problems exponentially faster than classical computers. Quantum algorithms like Shors algorithm for factoring and Grovers algorithm for searching demonstrate the potential of quantum computing. However, quantum computers face significant challenges including qubit stability (decoherence), error rates, and the need for very low operating temperatures. Current quantum computers are still in the NISQ (Noisy Intermediate-Scale Quantum) era, with limited qubits and high error rates. Major technology companies and research institutions are racing to develop practical quantum computers that can solve real-world problems.",
    "max_length": 150
  }' | python -m json.tool
echo ""
echo ""

# Test 5: Minimum Length Summary
echo -e "${BLUE}5. Minimum Length Summary (50 words)${NC}"
echo "Command: (max_length set to minimum allowed value)"
echo ""
curl -s -X POST "$API_URL/summarise" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Blockchain technology enables secure, decentralized transactions through cryptographic techniques. Each block contains a hash of the previous block, creating an immutable chain. This makes blockchain ideal for applications requiring transparency and security.",
    "max_length": 50
  }' | python -m json.tool
echo ""
echo ""

# Test 6: Short Text
echo -e "${BLUE}6. Short Text Summarisation${NC}"
echo "Command: (Minimal text input)"
echo ""
curl -s -X POST "$API_URL/summarise" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Cloud computing provides on-demand access to computing resources over the internet.",
    "max_length": 75
  }' | python -m json.tool
echo ""
echo ""

# Test 7: Error Test - Missing Text Field
echo -e "${BLUE}7. Error Test - Missing Required Field${NC}"
echo "Command: (No 'text' field - should return 422)"
echo ""
curl -s -X POST "$API_URL/summarise" \
  -H "Content-Type: application/json" \
  -d '{"max_length": 100}' | python -m json.tool
echo ""
echo ""

# Test 8: Error Test - Invalid max_length (Too Small)
echo -e "${BLUE}8. Error Test - Invalid max_length (< 50)${NC}"
echo "Command: (max_length = 10 - should return 422)"
echo ""
curl -s -X POST "$API_URL/summarise" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test text", "max_length": 10}' | python -m json.tool
echo ""
echo ""

# Test 9: Error Test - Invalid max_length (Too Large)
echo -e "${BLUE}9. Error Test - Invalid max_length (> 1000)${NC}"
echo "Command: (max_length = 2000 - should return 422)"
echo ""
curl -s -X POST "$API_URL/summarise" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test text", "max_length": 2000}' | python -m json.tool
echo ""
echo ""

# Test 10: Interactive API Documentation
echo -e "${BLUE}10. Interactive API Documentation${NC}"
echo "Open the following URLs in your browser:"
echo "  - Swagger UI: $API_URL/docs"
echo "  - ReDoc: $API_URL/redoc"
echo ""

echo -e "${GREEN}All curl examples completed!${NC}"
echo ""
echo "Tips:"
echo "  - Replace $API_URL if using different host/port"
echo "  - Ensure API is running: python -m uvicorn src.main:app --reload"
echo "  - Use 'python -m json.tool' to format JSON output (requires Python)"
echo "  - For Windows, use 'jq' or online JSON formatter if json.tool not available"
