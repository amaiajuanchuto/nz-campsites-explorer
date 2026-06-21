"""Load and clean the DOC campsites dataset."""

import pandas as pd
from pyproj import Transformer


def clean_columns(df):
    """Strip whitespace from column names and drop unused columns."""
    df.columns = df.columns.str.strip()
    return df.drop(columns=["Free"], errors="ignore")


def fill_missing_values(df):
    """Replace nulls in key categorical columns with explicit labels."""
    df["Landscape type"] = df["Landscape type"].fillna("Unknown")
    df["Activities"] = df["Activities"].fillna("Unknown")
    df["Dogs alllowed"] = df["Dogs alllowed"].fillna("Unknown")
    return df


def extract_primary_value(value, fallback_label):
    """Return the first comma-separated value, or a fallback if missing."""
    if value == fallback_label:
        return fallback_label
    return value.split(",")[0].strip()


def add_primary_column(df, source_col, primary_col, fallback_label="Unknown"):
    """Add single value columns derived from multi values field."""
    df[primary_col] = df[source_col].apply(
        lambda x: extract_primary_value(x, fallback_label)
    )
    return df


def convert_coordinates(df):
    """Convert NZTM2000 (EPSG:2193) coordinates to WGS84 lat/lon (EPSG:4326)."""
    transformer = Transformer.from_crs("EPSG:2193", "EPSG:4326", always_xy=True)
    df["lon"], df["lat"] = transformer.transform(df["x2"].values, df["y2"].values)
    return df


def load_and_clean_campsites(filepath="data/campsites.csv"):
    """Full pipeline: load, clean, enrich and convert the campsites dataset."""
    df = pd.read_csv(filepath)
    df = clean_columns(df)
    df = fill_missing_values(df)
    df = add_primary_column(df, source_col="Activities", primary_col="Primary activity")
    df = add_primary_column(
        df, source_col="Landscape type", primary_col="Primary landscape"
    )
    df = convert_coordinates(df)
    return df
