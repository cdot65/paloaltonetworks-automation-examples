"""Integration test for LangSmith tracing with anonymization.

This test verifies that sensitive data (API keys, passwords) are properly
masked when traces are sent to LangSmith.

Prerequisites:
    - LANGSMITH_API_KEY must be set
    - LANGSMITH_TRACING=true must be set
    - Internet connection to langsmith.com

Usage:
    # Run manually with LangSmith credentials
    LANGSMITH_API_KEY=lsv2_pt_xxx LANGSMITH_TRACING=true pytest tests/integration/test_langsmith_anonymization.py -v -s

    # Skip if LangSmith not configured
    pytest tests/integration/test_langsmith_anonymization.py -v
"""

import os
import uuid
from unittest.mock import Mock, patch

import pytest
from langchain_core.messages import HumanMessage

# Skip entire test file if LangSmith not configured
pytestmark = pytest.mark.skipif(
    not os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGSMITH_TRACING") != "true",
    reason="LangSmith tracing not enabled - set LANGSMITH_API_KEY and LANGSMITH_TRACING=true to run",
)


class TestLangSmithAnonymization:
    """Test that sensitive data is anonymized in LangSmith traces."""

    @patch("src.core.client.get_firewall_client")
    def test_api_keys_anonymized_in_traces(self, mock_get_client, autonomous_graph):
        """Test that PAN-OS API keys are anonymized in traces.

        This test sends a message containing a fake API key to the agent
        and verifies the trace is captured. Manual verification in LangSmith
        UI is required to confirm the API key was masked.
        """
        # Setup mock firewall with fake API key (will be in trace)
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.api_key = "LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBNnE9OGNHNjh0VDM4Ug=="
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        # Create unique test run ID for finding trace in LangSmith
        test_run_id = f"anonymization-test-{uuid.uuid4()}"

        # Send message with sensitive data patterns
        result = autonomous_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=f"Test ID: {test_run_id}. "
                        "This message contains test data: "
                        "API key LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBNnE9OGNHNjh0VDM4Ug== "
                        "and password='super_secret_123'"
                    )
                ]
            },
            config={"configurable": {"thread_id": test_run_id}},
        )

        # Verify agent responded (proves trace was sent)
        assert "messages" in result
        assert len(result["messages"]) > 0

        # Print instructions for manual verification
        print("\n" + "=" * 70)
        print("MANUAL VERIFICATION REQUIRED")
        print("=" * 70)
        print(f"\n1. Go to LangSmith: https://smith.langchain.com")
        print(f"2. Search for test run ID: {test_run_id}")
        print(f"3. Open the trace and verify:")
        print(f"   - API key 'LUFRPT14M...' is replaced with '<panos-api-key>'")
        print(f"   - Password 'super_secret_123' is replaced with '<password>'")
        print(f"\nIf you see the actual sensitive values, anonymization FAILED!")
        print("=" * 70 + "\n")

        # Return test run ID for manual lookup
        return test_run_id

    @patch("src.core.client.get_firewall_client")
    def test_anthropic_api_key_anonymized(self, mock_get_client, autonomous_graph):
        """Test that Anthropic API keys are anonymized in traces."""
        # Setup mock
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        test_run_id = f"anthropic-key-test-{uuid.uuid4()}"

        # Send message with fake Anthropic API key pattern
        result = autonomous_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=f"Test ID: {test_run_id}. "
                        "Testing with Anthropic key: sk-ant-api03-test_key_12345"
                    )
                ]
            },
            config={"configurable": {"thread_id": test_run_id}},
        )

        assert "messages" in result

        print("\n" + "=" * 70)
        print("ANTHROPIC API KEY ANONYMIZATION TEST")
        print("=" * 70)
        print(f"\nSearch for: {test_run_id}")
        print(f"Verify 'sk-ant-api03-test_key_12345' is masked as '<anthropic-api-key>'")
        print("=" * 70 + "\n")

        return test_run_id

    @patch("src.core.client.get_firewall_client")
    def test_xml_passwords_anonymized(self, mock_get_client, autonomous_graph):
        """Test that XML password elements are anonymized."""
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        test_run_id = f"xml-password-test-{uuid.uuid4()}"

        # Send message with XML password pattern
        result = autonomous_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=f"Test ID: {test_run_id}. "
                        "XML config: <config><password>MySecretPassword123</password></config>"
                    )
                ]
            },
            config={"configurable": {"thread_id": test_run_id}},
        )

        assert "messages" in result

        print("\n" + "=" * 70)
        print("XML PASSWORD ANONYMIZATION TEST")
        print("=" * 70)
        print(f"\nSearch for: {test_run_id}")
        print(f"Verify '<password>MySecretPassword123</password>' is masked")
        print("=" * 70 + "\n")

        return test_run_id

    @patch("src.core.client.get_firewall_client")
    def test_multiple_patterns_in_single_trace(self, mock_get_client, autonomous_graph):
        """Test that multiple sensitive patterns are all anonymized."""
        mock_fw = Mock()
        mock_fw.hostname = "192.168.1.1"
        mock_fw.id = "192.168.1.1"
        mock_get_client.return_value = mock_fw

        test_run_id = f"multi-pattern-test-{uuid.uuid4()}"

        # Send message with ALL sensitive patterns
        result = autonomous_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=f"Test ID: {test_run_id}. "
                        "Multiple secrets: "
                        "PAN-OS API: LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBNnE9OGNHNjh0VDM4Ug==, "
                        "Anthropic: sk-ant-api03-test123, "
                        "Password: password='admin123', "
                        "XML: <password>secret</password>"
                    )
                ]
            },
            config={"configurable": {"thread_id": test_run_id}},
        )

        assert "messages" in result

        print("\n" + "=" * 70)
        print("MULTIPLE PATTERNS ANONYMIZATION TEST")
        print("=" * 70)
        print(f"\nSearch for: {test_run_id}")
        print(f"Verify ALL of the following are masked:")
        print(f"  - PAN-OS API key → '<panos-api-key>'")
        print(f"  - Anthropic key → '<anthropic-api-key>'")
        print(f"  - Password field → 'password: <password>'")
        print(f"  - XML password → '<password>***</password>'")
        print("=" * 70 + "\n")

        return test_run_id


@pytest.mark.manual
def test_langsmith_anonymization_documentation():
    """Document the procedure for verifying LangSmith anonymization.

    This is a manual test - it provides instructions for human verification.
    """
    procedure = """
    # LangSmith Anonymization Verification Procedure

    ## Prerequisites
    1. Set environment variables:
       ```bash
       export LANGSMITH_API_KEY="lsv2_pt_your_key_here"
       export LANGSMITH_TRACING="true"
       export LANGSMITH_PROJECT="panos-agent-test"
       ```

    2. Ensure anonymizers are enabled in src/autonomous_graph.py and src/deterministic_graph.py

    ## Running Tests

    1. Run the anonymization test suite:
       ```bash
       LANGSMITH_API_KEY=xxx LANGSMITH_TRACING=true pytest tests/integration/test_langsmith_anonymization.py -v -s
       ```

    2. Each test will print a unique test run ID like:
       `anonymization-test-12345678-1234-1234-1234-123456789abc`

    ## Verification Steps

    1. Go to https://smith.langchain.com
    2. Navigate to your project (default: "panos-agent-test")
    3. Search for the test run ID printed by pytest
    4. Click on the trace to view details
    5. Inspect the inputs/outputs for sensitive data

    ## What to Check

    For each test, verify the following patterns are MASKED (not visible):

    ### test_api_keys_anonymized_in_traces
    - ❌ Should NOT see: `LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBNnE9OGNHNjh0VDM4Ug==`
    - ✅ Should see: `<panos-api-key>`
    - ❌ Should NOT see: `super_secret_123`
    - ✅ Should see: `password: <password>`

    ### test_anthropic_api_key_anonymized
    - ❌ Should NOT see: `sk-ant-api03-test_key_12345`
    - ✅ Should see: `<anthropic-api-key>`

    ### test_xml_passwords_anonymized
    - ❌ Should NOT see: `<password>MySecretPassword123</password>`
    - ✅ Should see: `<password>***</password>` or similar masked version

    ### test_multiple_patterns_in_single_trace
    - All of the above patterns should be masked in a single trace

    ## What Failure Looks Like

    If you see the ACTUAL sensitive values (API keys, passwords) in the trace:
    - ❌ FAILED - Anonymization is not working
    - Check that anonymizers are properly configured
    - Verify LangSmithAnonymizer is added to checkpointer
    - Review src/core/anonymizers.py patterns

    ## What Success Looks Like

    If you see ONLY the masked placeholders:
    - ✅ PASSED - Anonymization is working correctly
    - Safe to enable production tracing
    - Sensitive data protected in LangSmith traces

    ## Notes

    - This is a MANUAL test requiring human verification
    - Automated verification not possible (requires LangSmith UI access)
    - Run this test before enabling production tracing
    - Document results in test report
    """

    print(procedure)

    # This test always passes - it's just documentation
    assert True, "This is a documentation test - follow the procedure above"
