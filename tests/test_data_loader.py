"""Tests for the data loading and cleaning logic."""

import pandas as pd

from src.data_loader import (
    add_primary_column,
    clean_columns,
    convert_coordinates,
    extract_primary_value,
    fill_missing_values,
)


def test_clean_columns_strips_whitespace():
    df = pd.DataFrame({" Region ": ["Otago"], "Free": [None]})
    result = clean_columns(df)
    assert "Region" in result.columns
    assert " Region " not in result.columns


def test_clean_columns_drops_free_column():
    df = pd.DataFrame({"Region": ["Otago"], "Free": [None]})
    result = clean_columns(df)
    assert "Free" not in result.columns


def test_clean_columns_handles_missing_free_column():
    """Should not crash if 'Free' column doesn't exist."""
    df = pd.DataFrame({"Region": ["Otago"]})
    result = clean_columns(df)
    assert "Region" in result.columns


def test_fill_missing_values_replaces_nulls():
    df = pd.DataFrame(
        {
            "Landscape type": [None, "Coastal"],
            "Activities": [None, "Fishing"],
            "Dogs alllowed": [None, "Yes"],
        }
    )
    result = fill_missing_values(df)
    assert result["Landscape type"].tolist() == ["Unknown", "Coastal"]
    assert result["Activities"].tolist() == ["Unknown", "Fishing"]
    assert result["Dogs alllowed"].tolist() == ["Unknown", "Yes"]


def test_extract_primary_value_single_value():
    assert extract_primary_value("Fishing", "Unknown") == "Fishing"


def test_extract_primary_value_comma_separated():
    assert extract_primary_value("Fishing, Swimming, Boating", "Unknown") == "Fishing"


def test_extract_primary_value_strips_whitespace():
    assert extract_primary_value("Fishing,  Swimming", "Unknown") == "Fishing"


def test_extract_primary_value_fallback():
    assert extract_primary_value("Unknown", "Unknown") == "Unknown"


def test_add_primary_column():
    df = pd.DataFrame({"Activities": ["Fishing, Swimming", "Unknown"]})
    result = add_primary_column(df, "Activities", "Primary activity")
    assert result["Primary activity"].tolist() == ["Fishing", "Unknown"]


def test_convert_coordinates_returns_valid_lat_lon():
    """NZ should have negative latitude and positive longitude around 165-178."""
    df = pd.DataFrame(
        {
            "x2": [1500000.0],  # roughly central NZ NZTM easting
            "y2": [5400000.0],  # roughly central NZ NZTM northing
        }
    )
    result = convert_coordinates(df)
    assert -48 < result["lat"].iloc[0] < -34  # NZ latitude range
    assert 166 < result["lon"].iloc[0] < 179  # NZ longitude range
