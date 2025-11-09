"""Unit tests for LangSmith anonymizers."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.core.anonymizers import create_panos_tracer


class TestCreatePanosTracer:
    """Tests for create_panos_tracer function."""

    @patch("langchain_core.tracers.langchain.LangChainTracer")
    @patch("src.core.anonymizers.Client")
    @patch("src.core.anonymizers.create_anonymizer")
    def test_create_anonymizer_called_with_patterns(
        self, mock_create_anon, mock_client, mock_tracer_class
    ):
        """Test that create_anonymizer is called with correct patterns."""
        # Mock anonymizer
        mock_anonymizer = Mock()
        mock_create_anon.return_value = mock_anonymizer

        # Mock client
        mock_ls_client = Mock()
        mock_client.return_value = mock_ls_client

        # Mock tracer
        mock_tracer = Mock()
        mock_tracer_class.return_value = mock_tracer

        # Call function
        result = create_panos_tracer()

        # Verify create_anonymizer was called
        assert mock_create_anon.called
        call_args = mock_create_anon.call_args[0][0]

        # Should have 4 patterns
        assert len(call_args) == 4

        # Verify pattern types
        assert any("LUFRPT" in str(pattern) for pattern in call_args)  # PAN-OS key
        assert any("sk-ant" in str(pattern) for pattern in call_args)  # Anthropic key
        assert any("password" in str(pattern) for pattern in call_args)  # Password field
        assert any("<password>" in str(pattern) for pattern in call_args)  # XML password

    @patch("src.core.anonymizers.Client")
    @patch("langchain_core.tracers.langchain.LangChainTracer")
    @patch("src.core.anonymizers.create_anonymizer")
    def test_returns_langchain_tracer(self, mock_create_anon, mock_tracer, mock_client):
        """Test that function returns LangChainTracer instance."""
        # Mock components
        mock_anonymizer = Mock()
        mock_create_anon.return_value = mock_anonymizer
        mock_ls_client = Mock()
        mock_client.return_value = mock_ls_client
        mock_tracer_instance = Mock()
        mock_tracer.return_value = mock_tracer_instance

        # Call function
        result = create_panos_tracer()

        # Should return LangChainTracer
        assert result == mock_tracer_instance

    @patch("src.core.anonymizers.Client")
    @patch("langchain_core.tracers.langchain.LangChainTracer")
    @patch("src.core.anonymizers.create_anonymizer")
    def test_client_created_with_anonymizer(
        self, mock_create_anon, mock_tracer, mock_client
    ):
        """Test that LangSmith Client is created with anonymizer."""
        # Mock anonymizer
        mock_anonymizer = Mock()
        mock_create_anon.return_value = mock_anonymizer

        # Call function
        create_panos_tracer()

        # Verify Client was called with anonymizer
        mock_client.assert_called_once_with(anonymizer=mock_anonymizer)


class TestAnonymizerPatterns:
    """Tests for specific anonymization patterns."""

    def test_panos_api_key_pattern(self):
        """Test that PAN-OS API key pattern matches correctly."""
        # Sample PAN-OS API keys (format: LUFRPT followed by base64)
        test_keys = [
            "LUFRPT1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW==",
            "LUFRPT+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk=",
        ]

        import re

        pattern = r"LUFRPT[A-Za-z0-9+/=]{40,}"

        for key in test_keys:
            assert re.search(pattern, key), f"Pattern should match {key}"

        # Should not match invalid keys
        assert not re.search(pattern, "LUFRPT123"), "Should not match short key"
        assert not re.search(pattern, "NOTKEY1234567890"), "Should not match wrong prefix"

    def test_anthropic_api_key_pattern(self):
        """Test that Anthropic API key pattern matches correctly."""
        # Sample Anthropic API keys (need 40+ chars after prefix)
        test_keys = [
            "sk-ant-api03-1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV",
            "sk-ant-1234567890-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        ]

        import re

        pattern = r"sk-ant-[A-Za-z0-9-_]{40,}"

        for key in test_keys:
            assert re.search(pattern, key), f"Pattern should match {key}"

        # Should not match invalid keys
        assert not re.search(pattern, "sk-ant-short"), "Should not match short key"
        assert not re.search(pattern, "sk-test-123"), "Should not match wrong prefix"

    def test_password_field_pattern(self):
        """Test that password field pattern matches various formats."""
        test_strings = [
            'password="secret123"',
            "password: mysecret",
            "passwd=test123",
            "pwd: admin",
            'password="complex!@#$%"',
        ]

        import re

        pattern = r"(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[^\s'\"]+"

        for test_str in test_strings:
            match = re.search(pattern, test_str, re.IGNORECASE)
            assert match, f"Pattern should match {test_str}"

    def test_xml_password_pattern(self):
        """Test that XML password element pattern matches correctly."""
        test_strings = [
            "<password>secret123</password>",
            "<password>admin@123</password>",
            "<password>complex!@#$%</password>",
        ]

        import re

        pattern = r"<password>.*?</password>"

        for test_str in test_strings:
            match = re.search(pattern, test_str)
            assert match, f"Pattern should match {test_str}"
            # Verify replacement works
            redacted = re.sub(pattern, "<password><redacted></password>", test_str)
            assert "<redacted>" in redacted
            assert "secret" not in redacted.lower() or "admin" not in redacted.lower()


class TestAnonymizerIntegration:
    """Integration tests for anonymizer with sample data."""

    @patch("src.core.anonymizers.Client")
    @patch("langchain_core.tracers.langchain.LangChainTracer")
    @patch("src.core.anonymizers.create_anonymizer")
    def test_anonymizer_integration(self, mock_create_anon, mock_tracer, mock_client):
        """Test that anonymizer is properly integrated with tracer."""
        # Setup mocks
        mock_anonymizer = Mock()
        mock_create_anon.return_value = mock_anonymizer

        mock_ls_client = Mock()
        mock_client.return_value = mock_ls_client

        mock_tracer_instance = Mock()
        mock_tracer.return_value = mock_tracer_instance

        # Create anonymizer
        tracer = create_panos_tracer()

        # Verify workflow
        assert mock_create_anon.called, "create_anonymizer should be called"
        assert mock_client.called, "Client should be created"
        assert mock_tracer.called, "LangChainTracer should be created"

        # Verify Client was passed to LangChainTracer
        tracer_call_args = mock_tracer.call_args
        assert tracer_call_args is not None
        assert "client" in tracer_call_args[1]
        assert tracer_call_args[1]["client"] == mock_ls_client
