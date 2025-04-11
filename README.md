# 📍 Nearby Points of Interest Explorer

This is a mobile-friendly, location-aware web application built with Python and Streamlit. It helps users discover nearby landmarks, historical sites, restaurants, natural features, and more — based on their location and interests. It uses open data APIs and optionally summarizes facts using a free, open-source language model.

---

## ✨ Features

- 📍 Detects or manually inputs user location
- 📏 User-defined search radius (in meters)
- 🎯 Interest filters: History, Food, Architecture, Nature
- 🌐 Uses free APIs:
  - OpenStreetMap + Overpass
  - OpenTripMap
  - Wikipedia
- 🤖 Uses open-source LLM (e.g. BART) to summarize long descriptions
- 🗺️ Interactive map and fact list (optimized for mobile)
- ✅ Works fully on free-tier deployments (Streamlit Cloud, Render, Railway)

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/quinten1997/The-more-you-know.git

```

### 2. Install dependencies
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Set your API keys (optional but recommended)
Create a `.env` file or set environment variables:
```
OPENTRIPMAP_API_KEY=your_key
GEONAMES_USERNAME=your_geonames_username
YELP_API_KEY=your_yelp_key  # optional
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🔑 API Keys

| API          | How to Get It                                      |
|--------------|----------------------------------------------------|
| OpenTripMap  | https://opentripmap.io/                            |
| GeoNames     | http://www.geonames.org/login                      |
| Yelp Fusion* | https://www.yelp.com/developers/documentation/v3  |

\*Yelp is optional; you can rely solely on OpenStreetMap.

---

## 📁 Folder Structure

```
location_fact_app/
├── app.py               # Streamlit entrypoint
├── backend.py           # Core logic
├── requirements.txt     # Python dependencies
├── fetchers/            # API fetch logic
│   ├── opentripmap.py
│   ├── wikipedia.py
│   └── overpass.py
├── utils/               # Summarizer and geo utilities
│   ├── summarizer.py
│   └── geo.py
├── ui/                  # Map display logic
│   └── map_display.py
└── README.md
```

---

## 🛰️ Deployment

Recommended platforms:
- [Streamlit Cloud](https://streamlit.io/cloud) — easiest for quick deployment
- [Render](https://render.com/)
- [Railway](https://railway.app/)

All support free hosting with minor limitations (RAM, sleep on idle, etc).

---

## 🧠 LLM Summarization (Optional)

This app uses `facebook/bart-large-cnn` via Hugging Face Transformers for summarization. If the model can't be loaded (e.g., on a small server), it will gracefully fall back to simple truncation.

---

## ❤️ Credits

Built using:
- OpenStreetMap, Wikipedia, OpenTripMap
- Streamlit, Hugging Face Transformers, Folium
- Designed for travel lovers, explorers, and local adventurers

---

Feel free to fork and customize for your city, region, or interests!