# 🎂 Baking Studio — Personal Recipe & Technique Agent

A beautiful, interactive baking companion built with Python + Streamlit.

## Features

| Page | What it does |
|------|-------------|
| 🏠 Home | Dashboard with quick tips and category overview |
| 📚 Recipe Library | Browse, search, and filter all saved recipes by category/flavor |
| ✏️ Add Recipe | Manually add recipes with full flavor profiling |
| 🔗 Import from URL | Paste any recipe URL — ingredients & steps auto-extracted |
| 🎨 Flavor Explorer | Dial in sweetness/tartness/richness etc. and find matching recipes |
| 🎬 Techniques & Videos | Curated YouTube technique guides (piping, chocolate, glazes, etc.) |
| 👩‍🍳 Chef Inspirations | Instagram handles + YouTube channels of top pastry chefs |
| 🌍 World Dessert Index | Classics from France, Italy, Japan, Middle East, India, and more |
| 📖 Full Baking Index | Complete clickable index of every cake base, filling, buttercream, ganache, decoration |

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo → set entry point to `app.py`
4. Deploy!

The SQLite database (`baking_studio.db`) will be created automatically on first run.
