# 🏕️ NZ DOC Campsites Explorer

An interactive data analysis and visualisation app built with Python, Pandas, Plotly and Streamlit, exploring the Department of Conservation (DOC) campsite network across New Zealand.

## 🎯 Purpose

I am a software engineer originally from Chile, currently based in Brisbane and planning to relocate to New Zealand. As someone who loves the outdoors and is genuinely excited about Kiwi culture, I thought: what better way to get to know my future home than by diving into the data?

This project started as a curiosity: where are all the DOC campsites? Which regions have the most? What kind of landscapes can you camp in? One dataset later and I had all my answers.

It is part data analysis, part love to a country I have not moved to yet, but very much plan to. 🥝

## 🗺️ Live Demo

[Link coming soon — will be deployed on Streamlit Cloud]

## 📊 Features

- Interactive map of all 312 DOC campsites across NZ, coloured by category
- Campsite distribution by region
- Category breakdown (Standard, Basic, Great Walk, Backcountry, Serviced)
- Landscape type analysis (Coastal, Forest, Alpine, Rivers and lakes)
- Regional capacity comparison (powered vs unpowered sites)

## 🛠️ Tech Stack

- Python 3.12
- Pandas — data cleaning and analysis
- Plotly — interactive charts and map
- Streamlit — web app framework

## 🚀 How to Run Locally

**Prerequisites:** Python 3.12+, Poetry

```bash
# Clone the repository
git clone https://github.com/amaiajuanchuto/nz-campsites-explorer
cd nz-campsites-explorer

# Install dependencies
poetry install

# Run the app
poetry run streamlit run app.py
```

Then open your browser at `http://localhost:8501`

## 📁 Project Structure
nz-campsites-explorer/
├── app.py                  # Main Streamlit application
├── data/
│   └── campsites.csv       # DOC campsites dataset (source: data.govt.nz)
├── pyproject.toml          # Dependencies
└── README.md

## 📂 Data Source

Department of Conservation (DOC) — New Zealand Government
Source: [data.govt.nz](https://data.govt.nz)
Dataset: NZ DOC Campsites

## 🔍 Key Insights

1. **Marlborough leads** with 48 campsites — the most of any NZ region
2. **Standard and Basic campsites dominate** (65% of all sites) reflecting NZ's back-to-nature outdoor culture
3. **Coastal and riverside landscapes** account for over 55% of campsites, mapping directly to NZ's most visited natural areas

## 👩‍💻 Author

Amaia Juanchuto — Full-stack Software Engineer
[LinkedIn](https://linkedin.com/in/amaiajuanchuto) | [GitHub](https://github.com/amaiajuanchuto)
