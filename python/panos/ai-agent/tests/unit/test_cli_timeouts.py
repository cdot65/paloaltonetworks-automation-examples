"""Unit tests for CLI timeout handling."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typer.testing import CliRunner

from src.cli.commands import app
from src.core.config import TIMEOUT_AUTONOMOUS, TIMEOUT_DETERMINISTIC


runner = CliRunner()


class TestTimeoutConfiguration:
    """Tests for timeout constants and configuration."""

    def test_timeout_constants_defined(self):
        """Test that timeout constants are properly defined."""
        assert TIMEOUT_AUTONOMOUS == 300.0
        assert TIMEOUT_DETERMINISTIC == 600.0

    def test_timeout_constants_have_docstrings(self):
        """Test that timeout constants have documentation."""
        from src.core import config

        # Check that docstrings exist
        assert config.TIMEOUT_AUTONOMOUS.__doc__ is not None
        assert config.TIMEOUT_DETERMINISTIC.__doc__ is not None
        assert config.TIMEOUT_COMMIT.__doc__ is not None


class TestAutonomousModeTimeout:
    """Tests for autonomous mode timeout handling."""

    @patch("src.autonomous_graph.create_autonomous_graph")
    @patch("src.core.config.get_settings")
    def test_autonomous_timeout_passed_to_graph(self, mock_get_settings, mock_create_graph):
        """Test that timeout is passed to autonomous graph invocation."""
        # Setup mocks
        mock_settings = Mock()
        mock_settings.panos_hostname = "192.168.1.1"
        mock_get_settings.return_value = mock_settings

        mock_graph = Mock()
        mock_response = Mock()
        mock_response.content = "Response"
        mock_graph.invoke.return_value = {"messages": [mock_response]}
        mock_create_graph.return_value = mock_graph

        # Run command
        result = runner.invoke(app, ["run", "-p", "test", "-m", "autonomous"])

        # Verify timeout was passed to graph.invoke
        assert mock_graph.invoke.called
        call_kwargs = mock_graph.invoke.call_args[1]
        assert "config" in call_kwargs
        assert "timeout" in call_kwargs["config"]
        assert call_kwargs["config"]["timeout"] == TIMEOUT_AUTONOMOUS

    @patch("src.autonomous_graph.create_autonomous_graph")
    @patch("src.core.config.get_settings")
    def test_autonomous_timeout_error_caught(self, mock_get_settings, mock_create_graph):
        """Test that TimeoutError is caught in autonomous mode."""
        # Setup mocks
        mock_settings = Mock()
        mock_settings.panos_hostname = "192.168.1.1"
        mock_get_settings.return_value = mock_settings

        mock_graph = Mock()
        mock_graph.invoke.side_effect = TimeoutError("Graph execution timed out")
        mock_create_graph.return_value = mock_graph

        # Run command
        result = runner.invoke(app, ["run", "-p", "test query", "-m", "autonomous"])

        # Verify timeout error handling
        assert result.exit_code == 1
        assert "Timeout Error" in result.stdout or "timeout" in result.stdout.lower()
        assert "300.0s" in result.stdout or "300" in result.stdout

    @patch("src.autonomous_graph.create_autonomous_graph")
    @patch("src.core.config.get_settings")
    def test_autonomous_timeout_error_includes_context(self, mock_get_settings, mock_create_graph):
        """Test that timeout error includes mode and prompt context."""
        # Setup mocks
        mock_settings = Mock()
        mock_settings.panos_hostname = "192.168.1.1"
        mock_get_settings.return_value = mock_settings

        mock_graph = Mock()
        mock_graph.invoke.side_effect = TimeoutError()
        mock_create_graph.return_value = mock_graph

        # Run command with specific prompt
        result = runner.invoke(app, [
            "run",
            "-p", "Create 100 address objects",
            "-m", "autonomous"
        ])

        # Verify context in output
        assert result.exit_code == 1
        output = result.stdout.lower()
        assert "autonomous" in output or "mode" in output


class TestDeterministicModeTimeout:
    """Tests for deterministic mode timeout handling."""

    @patch("src.deterministic_graph.create_deterministic_graph")
    def test_deterministic_timeout_passed_to_graph(self, mock_create_graph):
        """Test that timeout is passed to deterministic graph invocation."""
        # Setup mock
        mock_graph = Mock()
        mock_response = Mock()
        mock_response.content = "Workflow complete"
        mock_graph.invoke.return_value = {"messages": [mock_response]}
        mock_create_graph.return_value = mock_graph

        # Run command
        result = runner.invoke(app, ["run", "-p", "simple_address", "-m", "deterministic"])

        # Verify timeout was passed
        assert mock_graph.invoke.called
        call_kwargs = mock_graph.invoke.call_args[1]
        assert "config" in call_kwargs
        assert "timeout" in call_kwargs["config"]
        assert call_kwargs["config"]["timeout"] == TIMEOUT_DETERMINISTIC

    @patch("src.deterministic_graph.create_deterministic_graph")
    def test_deterministic_timeout_error_caught(self, mock_create_graph):
        """Test that TimeoutError is caught in deterministic mode."""
        # Setup mock that raises TimeoutError
        mock_graph = Mock()
        mock_graph.invoke.side_effect = TimeoutError("Workflow timed out")
        mock_create_graph.return_value = mock_graph

        # Run command
        result = runner.invoke(app, ["run", "-p", "long_workflow", "-m", "deterministic"])

        # Verify timeout error handling
        assert result.exit_code == 1
        assert "Timeout Error" in result.stdout or "timeout" in result.stdout.lower()
        assert "600.0s" in result.stdout or "600" in result.stdout

    @patch("src.deterministic_graph.create_deterministic_graph")
    def test_deterministic_timeout_error_includes_workflow_context(self, mock_create_graph):
        """Test that timeout error includes workflow context."""
        # Setup mock
        mock_graph = Mock()
        mock_graph.invoke.side_effect = TimeoutError()
        mock_create_graph.return_value = mock_graph

        # Run command with workflow name
        workflow_name = "complex_security_workflow"
        result = runner.invoke(app, [
            "run",
            "-p", workflow_name,
            "-m", "deterministic"
        ])

        # Verify context in output
        assert result.exit_code == 1
        output = result.stdout.lower()
        assert "deterministic" in output or "mode" in output


class TestTimeoutErrorLogging:
    """Tests for timeout error logging behavior."""

    @patch("src.cli.commands.logging")
    @patch("src.autonomous_graph.create_autonomous_graph")
    @patch("src.core.config.get_settings")
    def test_timeout_logged_with_context(self, mock_get_settings, mock_create_graph, mock_logging):
        """Test that timeout errors are logged with proper context."""
        # Setup mocks
        mock_settings = Mock()
        mock_settings.panos_hostname = "192.168.1.1"
        mock_get_settings.return_value = mock_settings

        mock_graph = Mock()
        mock_graph.invoke.side_effect = TimeoutError()
        mock_create_graph.return_value = mock_graph

        # Run command
        test_prompt = "List all address objects"
        result = runner.invoke(app, [
            "run",
            "-p", test_prompt,
            "-m", "autonomous"
        ])

        # Verify logging was called
        assert mock_logging.error.called
        log_call_args = str(mock_logging.error.call_args)

        # Verify log includes key context
        assert "timeout" in log_call_args.lower() or "Graph timeout" in log_call_args


class TestTimeoutBehaviorDifferences:
    """Tests for different timeout values between modes."""

    @patch("src.autonomous_graph.create_autonomous_graph")
    @patch("src.deterministic_graph.create_deterministic_graph")
    @patch("src.core.config.get_settings")
    def test_autonomous_uses_shorter_timeout(
        self, mock_get_settings, mock_det_graph, mock_auto_graph
    ):
        """Test that autonomous mode uses shorter timeout than deterministic."""
        # Setup mocks
        mock_settings = Mock()
        mock_settings.panos_hostname = "192.168.1.1"
        mock_get_settings.return_value = mock_settings

        mock_auto = Mock()
        mock_auto.invoke.return_value = {"messages": [Mock(content="Done")]}
        mock_auto_graph.return_value = mock_auto

        mock_det = Mock()
        mock_det.invoke.return_value = {"messages": [Mock(content="Done")]}
        mock_det_graph.return_value = mock_det

        # Run both modes
        runner.invoke(app, ["run", "-p", "test", "-m", "autonomous"])
        runner.invoke(app, ["run", "-p", "test", "-m", "deterministic"])

        # Get timeout values from calls
        auto_timeout = mock_auto.invoke.call_args[1]["config"]["timeout"]
        det_timeout = mock_det.invoke.call_args[1]["config"]["timeout"]

        # Verify autonomous timeout is shorter
        assert auto_timeout < det_timeout
        assert auto_timeout == TIMEOUT_AUTONOMOUS
        assert det_timeout == TIMEOUT_DETERMINISTIC


class TestTimeoutErrorMessages:
    """Tests for timeout error message formatting."""

    @patch("src.autonomous_graph.create_autonomous_graph")
    @patch("src.core.config.get_settings")
    def test_timeout_error_message_format(self, mock_get_settings, mock_create_graph):
        """Test that timeout error message is user-friendly and informative."""
        # Setup mocks
        mock_settings = Mock()
        mock_settings.panos_hostname = "192.168.1.1"
        mock_get_settings.return_value = mock_settings

        mock_graph = Mock()
        mock_graph.invoke.side_effect = TimeoutError()
        mock_create_graph.return_value = mock_graph

        # Run command
        result = runner.invoke(app, ["run", "-p", "test query", "-m", "autonomous"])

        # Verify error message structure
        assert result.exit_code == 1
        output = result.stdout

        # Should mention timeout
        assert "timeout" in output.lower() or "Timeout" in output

        # Should include duration
        assert "300" in output or "5 min" in output.lower()

    @patch("src.deterministic_graph.create_deterministic_graph")
    def test_long_prompt_truncated_in_error(self, mock_create_graph):
        """Test that long prompts are truncated in timeout error messages."""
        # Setup mock
        mock_graph = Mock()
        mock_graph.invoke.side_effect = TimeoutError()
        mock_create_graph.return_value = mock_graph

        # Create very long prompt
        long_prompt = "a" * 200

        # Run command
        result = runner.invoke(app, [
            "run",
            "-p", long_prompt,
            "-m", "deterministic"
        ])

        # Verify prompt is truncated (should show preview, not full prompt)
        assert result.exit_code == 1
        # Error output should be reasonably sized, not include full 200 char prompt
        assert len(result.stdout) < 1000
