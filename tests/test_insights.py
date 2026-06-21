"""Tests for the insight generation logic."""

import pandas as pd
import pytest

from src.insights import (
    EXCLUDED_LABELS,
    NOT_ENOUGH_DATA_MESSAGE,
    NOT_INSIGHT_MESSAGE,
    generate_insight,
)


def test_generate_insight_returns_top_category():
    df = pd.DataFrame(
        {
            "Campsite category": ["Standard", "Standard", "Basic"],
        }
    )
    result = generate_insight(df, "Campsite category")
    assert "Standard" in result
    assert "66.7%" in result  # 2 of 3 rows


def test_generate_insight_includes_correct_count():
    df = pd.DataFrame(
        {
            "Region": ["Otago", "Otago", "Otago", "Canterbury"],
        }
    )
    result = generate_insight(df, "Region")
    assert "Otago" in result
    assert "**3**" in result


@pytest.mark.parametrize(
    "excluded_label",
    EXCLUDED_LABELS,
)
def test_generate_insight_excludes_labels(excluded_label):
    """Placeholder labels (from EXCLUDED_LABELS) should never win
    as the top insight, even when numerically most frequent."""
    df = pd.DataFrame(
        {
            "Primary activity": [
                excluded_label,
                excluded_label,
                excluded_label,
                "Fishing",
                "Fishing",
            ],
        }
    )
    result = generate_insight(df, "Primary activity")
    assert "Fishing" in result
    assert excluded_label not in result


def test_generate_insight_unknown_group_by_returns_empty_string():
    df = pd.DataFrame({"Region": ["Otago"]})
    result = generate_insight(df, "Some column non existent")
    assert result == NOT_INSIGHT_MESSAGE


def test_generate_insight_all_values_excluded_returns_fallback_message():
    """If every value in the column is a placeholder, there is no real
    insight to report — should fall back gracefully instead of crashing
    or reporting a meaningless 'Unknown' insight."""
    df = pd.DataFrame(
        {
            "Primary activity": ["Unknown", "Unknown", "Unknown"],
        }
    )
    result = generate_insight(df, "Primary activity")
    assert result == NOT_ENOUGH_DATA_MESSAGE
