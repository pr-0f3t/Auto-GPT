from pathlib import Path
from unittest.mock import Mock

import pytest

from autogpt.agents.agent import Agent
from autogpt.commands.decorators import run_in_workspace
from benchmarks import bootstrap_agent


class MockAgent(Agent, Mock):
    pass


@pytest.fixture
def agent(tmp_path):
    task = Mock()
    task.user_input = "Run"
    mock_agent = bootstrap_agent(task)
    mock_agent.config.workspace_path = tmp_path
    return mock_agent


def test_run_in_workspace_change_directory(agent):
    @run_in_workspace
    def dummy_func(agent):
        return Path.cwd()

    # Pass agent as positional parameter
    result_path = dummy_func(agent)
    assert str(result_path) == str(agent.config.workspace_path)

    # Pass agent as named parameter
    result_path = dummy_func(agent=agent)
    assert str(result_path) == str(agent.config.workspace_path)


def test_run_in_workspace_restore_directory(agent):
    original_dir = Path.cwd()

    @run_in_workspace
    def dummy_func(agent):
        pass

    dummy_func(agent)
    assert Path.cwd() == original_dir