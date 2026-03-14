#!/bin/bash
# Script to test LangSmith anonymization
# Usage: ./scripts/test_anonymization.sh

set -e

echo "=========================================="
echo "LangSmith Anonymization Test"
echo "=========================================="
echo

# Check for required environment variables
if [ -z "$LANGSMITH_API_KEY" ]; then
    echo "❌ Error: LANGSMITH_API_KEY not set"
    echo
    echo "Set it with:"
    echo "  export LANGSMITH_API_KEY='lsv2_pt_your_key_here'"
    exit 1
fi

# Set tracing environment variables
export LANGSMITH_TRACING="true"
export LANGSMITH_PROJECT="${LANGSMITH_PROJECT:-panos-agent-anonymization-test}"

echo "✅ LangSmith tracing enabled"
echo "   Project: $LANGSMITH_PROJECT"
echo

# Run the anonymization tests
echo "Running anonymization tests..."
echo "Each test will print a unique ID for manual verification"
echo

uv run pytest tests/integration/test_langsmith_anonymization.py -v -s

echo
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo
echo "1. Go to https://smith.langchain.com"
echo "2. Navigate to project: $LANGSMITH_PROJECT"
echo "3. Search for the test run IDs printed above"
echo "4. Verify sensitive data is masked (see test output)"
echo
echo "If you see actual API keys/passwords: ❌ FAILED"
echo "If you see only masked placeholders: ✅ PASSED"
echo
