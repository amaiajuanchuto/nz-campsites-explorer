import plotly.express as px
import streamlit as st

from src.data_loader import load_and_clean_campsites
from src.insights import generate_insight

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="NZ DOC Campsites Explorer",
    page_icon="🏕️",
    layout="wide",
)


# ── Load data ────────────────────────────────────────────
@st.cache_data
def load_data():
    return load_and_clean_campsites()


df = load_data()

CATEGORY_COLORS = {
    "Standard": "#e8a0b4",
    "Basic": "#c9a0c8",
    "Great Walk": "#0F6E56",
    "Backcountry": "#d4a373",
    "Serviced": "#185FA5",
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
            (
                f"<div style='display:flex;align-items:center;margin-bottom:6px;'>"
                f"<div style='width:14px;height:14px;background-color:{color};"
                f"border-radius:50%;margin-right:8px;'></div>"
                f"<span style='font-size:13px;'>{label} ({count})</span>"
                f"</div>"
            ),
            unsafe_allow_html=True,
        )

st.info(generate_insight(df, color_by), icon="💡")
