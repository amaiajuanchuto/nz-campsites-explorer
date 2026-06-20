import pandas as pd
import plotly.express as px
import streamlit as st

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="NZ DOC Campsites Explorer",
    page_icon="🏕️",
    layout="wide",
)


# ── Load data ────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/campsites.csv")
    # Clean column names
    df.columns = df.columns.str.strip()
    # Drop the Free column (entirely null)
    df = df.drop(columns=["Free"], errors="ignore")
    # Fill nulls in key columns
    df["Landscape type"] = df["Landscape type"].fillna("Unknown")
    df["Activities"] = df["Activities"].fillna("Not specified")
    df["Dogs alllowed"] = df["Dogs alllowed"].fillna("Unknown")
    # Convert NZTM2000 coordinates to lat/lon
    from pyproj import Transformer

    transformer = Transformer.from_crs("EPSG:2193", "EPSG:4326", always_xy=True)
    df["lon"], df["lat"] = transformer.transform(df["x2"].values, df["y2"].values)

    # Extract primary activity for colour grouping (first listed activity)
    df["Primary activity"] = df["Activities"].apply(
        lambda x: x.split(",")[0].strip() if x != "Not specified" else "Not specified"
    )

    # Extract primary landscape type for colour grouping (first listed type)
    df["Primary landscape"] = df["Landscape type"].apply(
        lambda x: x.split(",")[0].strip() if x != "Unknown" else "Unknown"
    )

    return df


df = load_data()

CATEGORY_COLORS = {
    "Standard": "#e8a0b4",
    "Basic": "#c9a0c8",
    "Great Walk": "#0F6E56",
    "Backcountry": "#d4a373",
    "Serviced": "#185FA5",
}
INSIGHT_TEMPLATES = {
    "Campsite category": (
        "**{label}** is the most common type, making up **{pct}%** "
        "of all campsites ({count} of {total}). This reflects how "
        "DOC prioritises accessible, low-cost camping over premium serviced sites."
    ),
    "Region": (
        "**{label}** has the most DOC campsites of any region, with "
        "**{count}** sites — {pct}% of the national total. This likely "
        "reflects both land availability and visitor demand in the area."
    ),
    "Primary activity": (
        "**{label}** is the most commonly listed primary activity, "
        "appearing at **{count}** campsites ({pct}% of sites with "
        "listed activities). Note: many sites offer multiple activities — "
        "this shows only the first one listed in the dataset."
    ),
    "Primary landscape": (
        "**{label}** is the most common landscape type, found at "
        "**{count}** campsites ({pct}% of sites with listed landscapes). "
        "Note: many sites span multiple landscape types — this shows only "
        "the first one listed in the dataset."
    ),
}

# ── Header ───────────────────────────────────────────────
st.title("🏕️ NZ DOC Campsites Explorer")
st.markdown(
    "Exploring the **Department of Conservation** campsite network across New Zealand. "
    "312 campsites, 16 regions, one interactive map."
)
st.divider()

# ── KPI metrics ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Campsites", len(df))
col2.metric("Regions", df["Region"].nunique())
col3.metric("Total Unpowered Sites", int(df["Number of unpowered sites"].sum()))
col4.metric("Total Powered Sites", int(df["Number of powered sites"].sum()))

st.divider()

# ── Map ──────────────────────────────────────────────────
st.subheader("🗺️ Campsite Locations Across New Zealand")

# ── Map filter ───────────────────────────────────────
color_by = st.selectbox(
    "Group map by:",
    options=["Campsite category", "Region", "Primary activity", "Primary landscape"],
    index=0,
    width=300,
)


def generate_insight(df, group_by):
    """Generate a short text insight based on the current grouping."""
    if group_by not in INSIGHT_TEMPLATES:
        return ""

    counts = df[group_by].value_counts()
    top_label = counts.index[0]
    top_count = counts.iloc[0]
    pct = round((top_count / len(df)) * 100, 1)

    return INSIGHT_TEMPLATES[group_by].format(
        label=top_label, count=top_count, pct=pct, total=len(df)
    )


map_col, legend_col = st.columns([5, 1])

with map_col:
    fig_map = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        color=color_by,
        hover_name="Name of site",
        hover_data={
            "Region": True,
            "Campsite category": True,
            "Number of unpowered sites": True,
            "Number of powered sites": True,
            "Landscape type": True,
            "lat": False,
            "lon": False,
        },
        zoom=4.5,
        center={"lat": -41.0, "lon": 174.0},
        height=600,
        color_discrete_map=CATEGORY_COLORS if color_by == "Campsite category" else None,
    )

    fig_map.update_layout(
        map_style="open-street-map",
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
        showlegend=False,  # we hide the built-in legend, we'll build our own
    )

    st.plotly_chart(fig_map)

with legend_col:
    st.markdown(f"**{color_by}**")
    counts = df[color_by].value_counts()
    colors_used = (
        px.colors.qualitative.Plotly if color_by != "Campsite category" else None
    )

    for i, (label, count) in enumerate(counts.items()):
        if color_by == "Campsite category" and label in CATEGORY_COLORS:
            color = CATEGORY_COLORS[label]
        elif colors_used:
            color = colors_used[i % len(colors_used)]
        else:
            color = "#999999"

        st.markdown(
            f"<div style='display:flex;align-items:center;margin-bottom:6px;'>"
            f"<div style='width:14px;height:14px;background-color:{color};border-radius:50%;margin-right:8px;'></div>"
            f"<span style='font-size:13px;'>{label} ({count})</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.info(generate_insight(df, color_by), icon="💡")
