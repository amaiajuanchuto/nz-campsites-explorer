"""Generate contextual text insights based on campsite data groupings."""

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

EXCLUDED_LABELS = {"Not specified", "Unknown"}


def generate_insight(df, group_by):
    """Generate a short text insight based on the current grouping."""
    if group_by not in INSIGHT_TEMPLATES:
        return ""

    counts = df[group_by].value_counts()
    # Exclude placeholder labels so the insight reflects real data, not gaps
    counts = counts[~counts.index.isin(EXCLUDED_LABELS)]

    if counts.empty:
        return "Not enough labelled data available for this grouping yet..."

    top_label = counts.index[0]
    top_count = counts.iloc[0]
    pct = round((top_count / len(df)) * 100, 1)

    return INSIGHT_TEMPLATES[group_by].format(
        label=top_label, count=top_count, pct=pct, total=len(df)
    )
