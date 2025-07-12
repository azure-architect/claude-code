"""Pytest configuration and shared fixtures."""

from typing import Any, Dict

import pytest


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Sample data fixture for testing."""
    return {"test": "data"}
