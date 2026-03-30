import streamlit as st
import sqlite3
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import urllib.parse

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎂 Baking Studio",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #FDF6EC !important;
    font-family: 'DM Sans', sans-serif;
    color: #2C1A0E !important;
}

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #6B3F2A !important; }

p, li, span, div, label { color: #2C1A0E; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #2C1A0E 0%, #6B3F2A 100%) !important;
    border-right: 2px solid #C87941;
}
[data-testid="stSidebar"] * { color: #FDF6EC !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 15px; padding: 6px 0; }

/* Cards */
.recipe-card {
    background: #FFFDF8;
    border: 1px solid #E8D5C0;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 2px 12px rgba(107,63,42,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    color: #2C1A0E !important;
}
.recipe-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(107,63,42,0.15);
}
.recipe-card b, .recipe-card strong { color: #2C1A0E !important; }
.recipe-card small { color: #666 !important; }
.recipe-card a { color: #C87941 !important; }

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 2em;
    color: #6B3F2A !important;
    border-bottom: 3px solid #C87941;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

/* Tag pill */
.tag-pill {
    display: inline-block;
    background: #F2C4B0;
    color: #6B3F2A !important;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 12px;
    margin: 2px;
}

.stButton > button {
    background: linear-gradient(135deg, #C87941, #6B3F2A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}

.stTextInput > div > div > input {
    border: 2px solid #E8D5C0 !important;
    border-radius: 10px !important;
    background: white !important;
    color: #2C1A0E !important;
}

.stTextArea > div > div > textarea {
    border: 2px solid #E8D5C0 !important;
    border-radius: 10px !important;
    background-color: #FFFFFF !important;
    color: #2C1A0E !important;
}

/* ── ALL DROPDOWNS & SELECTS ── */
/* Outer container */
.stSelectbox > div > div { background-color: #FFFFFF !important; }

/* The visible selected value box */
[data-baseweb="select"] > div:first-child,
[data-baseweb="select"] > div:first-child > div,
[data-baseweb="select"] > div:first-child span,
[data-baseweb="select"] > div:first-child input {
    background-color: #FFFFFF !important;
    color: #2C1A0E !important;
}

/* Dropdown arrow icon area */
[data-baseweb="select"] > div:first-child > div:last-child {
    background-color: #FFFFFF !important;
}

/* The popup menu list */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
[data-baseweb="menu"] > ul,
[data-baseweb="menu"] ul li,
[role="listbox"],
[role="option"] {
    background-color: #FFFFFF !important;
    color: #2C1A0E !important;
}

/* Each option item */
[role="option"]:hover,
[data-baseweb="menu"] ul li:hover {
    background-color: #F2C4B0 !important;
    color: #2C1A0E !important;
}

/* ── ALL TEXT INPUTS ── */
[data-baseweb="input"],
[data-baseweb="input"] > div,
[data-baseweb="input"] input,
[data-baseweb="textarea"],
[data-baseweb="textarea"] > div,
[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #2C1A0E !important;
}

/* ── ALL LABELS ── */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stSlider label,
.stRadio label,
.stCheckbox label,
.stNumberInput label,
[data-testid="stWidgetLabel"] {
    color: #2C1A0E !important;
    font-weight: 500 !important;
}

/* ── SLIDERS ── */
[data-testid="stSlider"] > div > div > div > div {
    background-color: #C87941 !important;
}

/* ── METRIC WIDGETS ── */
[data-testid="stMetricValue"] { color: #6B3F2A !important; }
[data-testid="stMetricLabel"] { color: #2C1A0E !important; }

/* ── ALERTS / INFO BOXES ── */
.stAlert, .stAlert p, .stAlert div { color: #2C1A0E !important; }

/* ── EXPANDERS ── */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #2C1A0E !important;
    font-weight: 600;
}

/* ── FORM SUBMIT AREA ── */
[data-testid="stForm"] {
    background-color: #FFFDF8 !important;
    border: 1px solid #E8D5C0 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* ── GENERAL PARAGRAPH / TEXT ── */
p, li, span, div, td, th { color: #2C1A0E; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #2C1A0E 0%, #6B3F2A 60%, #C87941 100%);
    border-radius: 20px;
    padding: 40px;
    color: white !important;
    margin-bottom: 30px;
    text-align: center;
}
.hero-banner h1 { color: #FDF6EC !important; font-size: 2.8em !important; }
.hero-banner p { color: #F2C4B0 !important; font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

# ─── Database Setup ─────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("baking_studio.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        subcategory TEXT,
        description TEXT,
        ingredients TEXT,
        steps TEXT,
        flavor_sweetness INTEGER DEFAULT 5,
        flavor_tartness INTEGER DEFAULT 3,
        flavor_richness INTEGER DEFAULT 5,
        flavor_bitterness INTEGER DEFAULT 2,
        flavor_nuttiness INTEGER DEFAULT 2,
        flavor_floral INTEGER DEFAULT 1,
        source_url TEXT,
        video_url TEXT,
        instagram_url TEXT,
        region TEXT,
        difficulty TEXT DEFAULT 'Medium',
        tags TEXT,
        notes TEXT,
        thumbnail_url TEXT,
        created_at TEXT
    )""")
    # Migrate existing DBs — add thumbnail_url if missing
    try:
        c.execute("ALTER TABLE recipes ADD COLUMN thumbnail_url TEXT")
        conn.commit()
    except Exception:
        pass  # column already exists
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("baking_studio.db")
    conn.row_factory = sqlite3.Row  # allows dict-style access by column name
    return conn

def save_recipe(data):
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO recipes 
        (name, category, subcategory, description, ingredients, steps,
         flavor_sweetness, flavor_tartness, flavor_richness, flavor_bitterness,
         flavor_nuttiness, flavor_floral, source_url, video_url, instagram_url,
         region, difficulty, tags, notes, thumbnail_url, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (data['name'], data['category'], data['subcategory'], data['description'],
         data['ingredients'], data['steps'],
         data['sweetness'], data['tartness'], data['richness'], data['bitterness'],
         data['nuttiness'], data['floral'],
         data['source_url'], data['video_url'], data['instagram_url'],
         data['region'], data['difficulty'], data['tags'], data['notes'],
         data.get('thumbnail_url', ''),
         datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM recipes ORDER BY category, subcategory, name")
    rows = c.fetchall()
    conn.close()
    return rows

def get_recipes_by_category(category):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM recipes WHERE category=? ORDER BY subcategory, name", (category,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_recipe(recipe_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
    conn.commit()
    conn.close()

def update_recipe(recipe_id, data):
    conn = get_db()
    c = conn.cursor()
    c.execute("""UPDATE recipes SET name=?, category=?, subcategory=?, description=?,
        ingredients=?, steps=?, flavor_sweetness=?, flavor_tartness=?, flavor_richness=?,
        flavor_bitterness=?, flavor_nuttiness=?, flavor_floral=?, source_url=?, video_url=?,
        instagram_url=?, region=?, difficulty=?, tags=?, notes=?
        WHERE id=?""",
        (data['name'], data['category'], data['subcategory'], data['description'],
         data['ingredients'], data['steps'],
         data['sweetness'], data['tartness'], data['richness'], data['bitterness'],
         data['nuttiness'], data['floral'],
         data['source_url'], data['video_url'], data['instagram_url'],
         data['region'], data['difficulty'], data['tags'], data['notes'], recipe_id))
    conn.commit()
    conn.close()

# ─── URL Scraper ────────────────────────────────────────────────────────────────
def scrape_recipe_from_url(url):
    """Extract recipe data using JSON-LD schema first, then heuristic fallback."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Priority 1: JSON-LD structured data (works on most food blogs)
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                raw = script.string
                if not raw:
                    continue
                data = json.loads(raw)
                # Handle @graph arrays (WordPress/Yoast SEO pattern)
                if isinstance(data, dict) and "@graph" in data:
                    items = data["@graph"]
                elif isinstance(data, list):
                    items = data
                else:
                    items = [data]

                for item in items:
                    rtype = item.get("@type", "")
                    if isinstance(rtype, list):
                        rtype = " ".join(rtype)
                    if "Recipe" not in rtype:
                        continue

                    name = item.get("name", "")
                    desc = item.get("description", "")

                    # Clean ingredients
                    raw_ingr = item.get("recipeIngredient", [])
                    clean_ingr = []
                    for i in raw_ingr:
                        if isinstance(i, str) and i.strip():
                            clean_ingr.append(re.sub(r'\s+', ' ', i).strip())
                    ingredients = "\n".join(clean_ingr)

                    # Parse instructions - handles HowToStep, HowToSection, plain strings
                    instructions = item.get("recipeInstructions", [])
                    steps_lines = []
                    if isinstance(instructions, str):
                        steps_lines = [BeautifulSoup(instructions, "html.parser").get_text().strip()]
                    elif isinstance(instructions, list):
                        step_num = 1
                        for step in instructions:
                            if isinstance(step, dict):
                                stype = step.get("@type", "")
                                if stype == "HowToSection":
                                    for sub in step.get("itemListElement", []):
                                        txt = sub.get("text", "").strip() if isinstance(sub, dict) else str(sub)
                                        txt = BeautifulSoup(txt, "html.parser").get_text().strip()
                                        if txt:
                                            steps_lines.append(f"Step {step_num}: {txt}")
                                            step_num += 1
                                else:
                                    txt = step.get("text", step.get("name", "")).strip()
                                    txt = BeautifulSoup(txt, "html.parser").get_text().strip()
                                    if txt:
                                        steps_lines.append(f"Step {step_num}: {txt}")
                                        step_num += 1
                            elif isinstance(step, str) and step.strip():
                                steps_lines.append(f"Step {step_num}: {step.strip()}")
                                step_num += 1

                    steps = "\n".join(steps_lines)

                    # Grab thumbnail image
                    thumb = ""
                    img_data = item.get("image", "")
                    if isinstance(img_data, str):
                        thumb = img_data
                    elif isinstance(img_data, list) and img_data:
                        first = img_data[0]
                        thumb = first.get("url", first) if isinstance(first, dict) else first
                    elif isinstance(img_data, dict):
                        thumb = img_data.get("url", "")

                    if name or ingredients:
                        return {"name": name, "ingredients": ingredients, "steps": steps,
                                "description": desc, "thumbnail_url": thumb, "success": True}
            except Exception:
                continue

        # Priority 2: Heuristic fallback
        title = soup.find("h1")
        name = title.get_text(strip=True) if title else ""

        # Try to grab first meaningful image from og:image or first <img>
        thumb = ""
        og_img = soup.find("meta", property="og:image")
        if og_img and og_img.get("content"):
            thumb = og_img["content"]
        else:
            for img in soup.find_all("img"):
                src = img.get("src", "")
                if src.startswith("http") and any(ext in src.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                    if int(img.get("width", 200)) > 100:
                        thumb = src
                        break

        measure_words = ["cup", "tbsp", "tsp", "gram", " g ", "oz", "ml", "litre",
                         "liter", "pinch", "handful", "clove", "kg", "lb"]
        seen = set()
        ingredients = []
        for tag in soup.find_all(["li", "span"]):
            text = re.sub(r'\s+', ' ', tag.get_text(separator=' ')).strip()
            if any(w in text.lower() for w in measure_words) and 5 < len(text) < 200 and text not in seen:
                seen.add(text)
                ingredients.append(text)

        steps_lines = []
        seen_steps = set()
        for tag in soup.find_all(["li", "p"]):
            text = re.sub(r'\s+', ' ', tag.get_text(separator=' ')).strip()
            if len(text) > 30 and text not in seen_steps:
                if re.match(r'^(step\s*\d+[:\.]?|\d+[\.):])', text, re.IGNORECASE):
                    seen_steps.add(text)
                    steps_lines.append(text)

        return {
            "name": name,
            "ingredients": "\n".join(ingredients[:40]),
            "steps": "\n".join(steps_lines),
            "description": "",
            "thumbnail_url": thumb,
            "success": bool(name or ingredients)
        }

    except Exception as e:
        return {"name": "", "ingredients": "", "steps": "", "description": "", "thumbnail_url": "", "success": False, "error": str(e)}

# ─── Data Structures ─────────────────────────────────────────────────────────────
CATEGORIES = {
    "🫧 Cake Bases": {
        "subcategories": ["Foam/Air-Based", "Butter-Based", "Oil-Based", "Chocolate & Rich", "Nut-Based", "Regional"],
        "emoji": "🎂"
    },
    "🥛 Fillings": {
        "subcategories": ["Fruit-Based", "Cream-Based", "Custard-Based", "Chocolate-Based", "Nut-Based", "Caramel-Based"],
        "emoji": "🍓"
    },
    "🎂 Buttercreams & Frostings": {
        "subcategories": ["American", "Swiss Meringue", "Italian Meringue", "French", "German", "Ermine", "Korean Glossy", "Cream Cheese", "Whipped Cream"],
        "emoji": "🧁"
    },
    "🍫 Ganaches & Glazes": {
        "subcategories": ["Dark Chocolate", "Milk Chocolate", "White Chocolate", "Whipped", "Mirror Glaze", "Fruit Glaze"],
        "emoji": "🍫"
    },
    "🥧 Pies & Tarts": {
        "subcategories": ["Fruit Pies", "Custard Pies", "Nut Pies", "Chocolate Pies", "Classic Tarts"],
        "emoji": "🥧"
    },
    "🍮 Custards & Set Desserts": {
        "subcategories": ["Crème Brûlée", "Flan & Panna Cotta", "Puddings", "Mousses", "Bavarian Cream"],
        "emoji": "🍮"
    },
    "🥐 Viennoiserie": {
        "subcategories": ["Croissants", "Brioche", "Danish Pastries", "Laminated Doughs"],
        "emoji": "🥐"
    },
    "🍪 Cookies & Biscuits": {
        "subcategories": ["Shortbread", "Drop Cookies", "Rolled Cookies", "French Pastries", "Biscotti"],
        "emoji": "🍪"
    },
    "🌍 Global Desserts": {
        "subcategories": ["French", "Italian", "Japanese", "Middle Eastern", "Indian", "American", "Latin American", "Eastern European"],
        "emoji": "🌍"
    },
    "✨ Decorations & Techniques": {
        "subcategories": ["Buttercream Piping", "Sugar Work", "Chocolate Techniques", "Fondant", "Mirror Finish"],
        "emoji": "✨"
    },
}

FLAVOR_PROFILES = {
    "sweetness": ("🍯 Sweetness", "#FFD700"),
    "tartness": ("🍋 Tartness", "#90EE90"),
    "richness": ("🧈 Richness", "#DEB887"),
    "bitterness": ("☕ Bitterness", "#8B4513"),
    "nuttiness": ("🥜 Nuttiness", "#D2691E"),
    "floral": ("🌸 Floral", "#FFB6C1"),
}

TECHNIQUE_VIDEOS = {
    "Piping Techniques": [
        {"title": "Basic Piping Tips & Nozzles Guide", "url": "https://www.youtube.com/results?search_query=basic+piping+tips+buttercream+techniques"},
        {"title": "Rosette & Swirls Tutorial", "url": "https://www.youtube.com/results?search_query=buttercream+rosette+swirl+piping+tutorial"},
        {"title": "Ruffle & Petal Piping", "url": "https://www.youtube.com/results?search_query=ruffle+petal+piping+cake+tutorial"},
        {"title": "Korean Buttercream Flowers", "url": "https://www.youtube.com/results?search_query=korean+buttercream+flower+piping"},
    ],
    "Chocolate Work": [
        {"title": "How to Temper Chocolate", "url": "https://www.youtube.com/results?search_query=how+to+temper+chocolate+tutorial"},
        {"title": "Chocolate Shards & Decorations", "url": "https://www.youtube.com/results?search_query=chocolate+shards+decorations+cake"},
        {"title": "Chocolate Drip Technique", "url": "https://www.youtube.com/results?search_query=chocolate+drip+cake+tutorial"},
        {"title": "Ganache Pours & Glazes", "url": "https://www.youtube.com/results?search_query=ganache+pour+glaze+cake"},
    ],
    "Cake Assembly": [
        {"title": "How to Tort & Fill a Cake", "url": "https://www.youtube.com/results?search_query=how+to+tort+fill+layer+cake"},
        {"title": "Crumb Coating & Smooth Finish", "url": "https://www.youtube.com/results?search_query=crumb+coat+smooth+buttercream+cake"},
        {"title": "Sharp Edges on Cakes", "url": "https://www.youtube.com/results?search_query=sharp+edge+cake+tutorial+buttercream"},
        {"title": "Ombré & Watercolor Effects", "url": "https://www.youtube.com/results?search_query=ombre+watercolor+buttercream+cake"},
    ],
    "Sugar Art": [
        {"title": "Caramel Cages & Spun Sugar", "url": "https://www.youtube.com/results?search_query=caramel+cage+spun+sugar+tutorial"},
        {"title": "Isomalt Decorations", "url": "https://www.youtube.com/results?search_query=isomalt+decorations+tutorial"},
        {"title": "Sugar Flowers from Scratch", "url": "https://www.youtube.com/results?search_query=sugar+flowers+from+scratch+tutorial"},
        {"title": "Royal Icing Decorations", "url": "https://www.youtube.com/results?search_query=royal+icing+decorations+tutorial"},
    ],
    "Mirror Glaze & Entremet": [
        {"title": "Mirror Glaze Step-by-Step", "url": "https://www.youtube.com/results?search_query=mirror+glaze+cake+step+by+step"},
        {"title": "Building an Entremet Cake", "url": "https://www.youtube.com/results?search_query=entremet+mousse+cake+tutorial"},
        {"title": "Marbled Mirror Glaze", "url": "https://www.youtube.com/results?search_query=marble+mirror+glaze+tutorial"},
    ],
    "Laminated Doughs": [
        {"title": "Croissant from Scratch", "url": "https://www.youtube.com/results?search_query=croissant+from+scratch+tutorial"},
        {"title": "Kouign-Amann Technique", "url": "https://www.youtube.com/results?search_query=kouign+amann+tutorial"},
        {"title": "Lamination Explained", "url": "https://www.youtube.com/results?search_query=how+to+laminate+dough+pastry+tutorial"},
    ],
}

CHEF_INSTAGRAMS = [
    {"name": "Claire Saffitz", "handle": "@csaffitz", "specialty": "French pastry, entremet", "url": "https://www.instagram.com/csaffitz/"},
    {"name": "Joshua Weissman", "handle": "@joshuaweissman", "specialty": "Breads, pastries", "url": "https://www.instagram.com/joshuaweissman/"},
    {"name": "Natasha Pickowicz", "handle": "@natasha_pickowicz", "specialty": "Cakes, tarts", "url": "https://www.instagram.com/natasha_pickowicz/"},
    {"name": "Brooke Bellamy", "handle": "@brookebakes", "specialty": "Decorated cakes, buttercream", "url": "https://www.instagram.com/brookebakes/"},
    {"name": "BraveTart (Stella Parks)", "handle": "@bravetart", "specialty": "American classics", "url": "https://www.instagram.com/bravetart/"},
    {"name": "Kirsten Tibballs", "handle": "@kirstentibballs", "specialty": "Chocolate, entremet", "url": "https://www.instagram.com/kirstentibballs/"},
    {"name": "Dominique Ansel", "handle": "@dominiqueansel", "specialty": "French innovation", "url": "https://www.instagram.com/dominiqueansel/"},
    {"name": "Pastry Living (Aya Hasegawa)", "handle": "@pastryliving", "specialty": "Japanese pastry", "url": "https://www.instagram.com/pastryliving/"},
    {"name": "Sugar Geek Show (Liz Marek)", "handle": "@sugargeekshow", "specialty": "Decorated cakes, tutorials", "url": "https://www.instagram.com/sugargeekshow/"},
    {"name": "Bon Appétit", "handle": "@bonappetitmag", "specialty": "Wide range, pro tips", "url": "https://www.instagram.com/bonappetitmag/"},
]

# ─── Helper Functions ─────────────────────────────────────────────────────────────
def render_flavor_bars(row):
    cols = st.columns(3)
    keys = ["flavor_sweetness","flavor_tartness","flavor_richness",
            "flavor_bitterness","flavor_nuttiness","flavor_floral"]
    labels = ["🍯 Sweet","🍋 Tart","🧈 Rich","☕ Bitter","🥜 Nutty","🌸 Floral"]
    for i, (key, label) in enumerate(zip(keys, labels)):
        with cols[i % 3]:
            try:
                val = int(row[key]) if row[key] is not None else 5
            except (ValueError, IndexError, TypeError):
                val = 5
            val = max(1, min(10, val))
            st.markdown(f"**{label}** `{val}/10`")
            st.progress(val / 10)

def render_recipe_card(row, show_delete=False):
    name       = row["name"]
    subcat     = row["subcategory"] or ""
    desc       = row["description"] or ""
    ingr       = row["ingredients"] or ""
    steps      = row["steps"] or ""
    source_url = row["source_url"] or ""
    video_url  = row["video_url"] or ""
    insta_url  = row["instagram_url"] or ""
    difficulty = row["difficulty"] or "Medium"
    tags       = row["tags"] or ""
    rec_id     = row["id"]
    try:
        thumb  = row["thumbnail_url"] or ""
    except Exception:
        thumb  = ""

    # ── Fully clickable card row ────────────────────────────────────────
    expanded_key = f"expanded_{rec_id}"
    if expanded_key not in st.session_state:
        st.session_state[expanded_key] = False

    # Clickable card row
    card_html = f"""
    <div style='display:flex;align-items:center;gap:16px;background:#FFFDF8;
         border:1px solid #E8D5C0;border-radius:16px;padding:12px 16px;
         margin:8px 0;cursor:pointer;box-shadow:0 2px 8px rgba(107,63,42,0.08)'>
        <div style='flex-shrink:0;width:90px;height:90px;border-radius:12px;overflow:hidden;
             background:#F2C4B0;display:flex;align-items:center;justify-content:center;font-size:2em'>
            {'<img src="'+thumb+'" style="width:100%;height:100%;object-fit:cover">' if thumb else '🎂'}
        </div>
        <div style='flex:1;min-width:0'>
            <div style='font-weight:700;font-size:1.05em;color:#2C1A0E'>{name}</div>
            <div style='color:#888;font-size:0.85em;margin:2px 0'>{subcat} {'· '+difficulty if difficulty else ''}</div>
            <div style='color:#666;font-size:0.85em;margin-top:4px;overflow:hidden;
                 text-overflow:ellipsis;white-space:nowrap'>{desc[:130]+'...' if len(desc)>130 else desc}</div>
        </div>
        <div style='color:#C87941;font-size:1.2em'>{'▼' if st.session_state[expanded_key] else '▶'}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    if st.button(f"{'▼ Collapse' if st.session_state[expanded_key] else '▶ Open Recipe & Tweak'}",
                 key=f"toggle_{rec_id}", use_container_width=True):
        st.session_state[expanded_key] = not st.session_state[expanded_key]
        st.rerun()

    if st.session_state[expanded_key]:
        st.markdown("<div style='background:#FFFDF8;border:1px solid #E8D5C0;border-radius:12px;padding:16px;margin-top:4px'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            if tags:
                for tag in tags.split(","):
                    st.markdown(f"<span class='tag-pill'>{tag.strip()}</span>", unsafe_allow_html=True)
                st.write("")
            if ingr:
                st.markdown("**🧂 Ingredients**")
                for line in ingr.strip().split("\n"):
                    if line.strip():
                        st.markdown(f"• {line.strip()}")
            if steps:
                st.markdown("**📋 Steps**")
                for line in steps.strip().split("\n"):
                    if line.strip():
                        st.markdown(f"<p style='color:#2C1A0E;margin:4px 0'>{line.strip()}</p>",
                                    unsafe_allow_html=True)
            links = []
            if source_url: links.append(f"[📖 Source]({source_url})")
            if video_url:  links.append(f"[▶️ Video]({video_url})")
            if insta_url:  links.append(f"[📸 Instagram]({insta_url})")
            if links:
                st.write("")
                st.markdown("  |  ".join(links))
        with col2:
            st.markdown("**Flavor Profile**")
            render_flavor_bars(row)

        # ── Formula-Based Recipe Tweaker ──────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🔧 Tweak This Recipe")

        tw1, tw2 = st.columns(2)
        with tw1:
            orig_servings = st.number_input("Original recipe serves", min_value=1, max_value=50, value=4, key=f"orig_{rec_id}")
        with tw2:
            new_servings  = st.number_input("👥 I want to make for", min_value=1, max_value=100, value=4, key=f"new_{rec_id}")

        health_mode = st.selectbox("🥗 Recipe version",
                                    ["Original", "Healthier", "Indulgent"],
                                    key=f"hlth_{rec_id}")

        st.markdown("**🎨 Flavor adjustments:**")
        fa1, fa2, fa3 = st.columns(3)
        flavor_opts = ["Much Less (×0.5)", "Less (×0.75)", "Same", "More (×1.25)", "Much More (×1.5)"]
        spice_opts  = ["None", "Mild", "Medium", "Hot", "Very Hot"]
        with fa1:
            adj_sweet  = st.selectbox("🍯 Sweetness",  flavor_opts, index=2, key=f"sw_{rec_id}")
            adj_salt   = st.selectbox("🧂 Saltiness",  flavor_opts, index=2, key=f"sa_{rec_id}")
        with fa2:
            adj_bitter = st.selectbox("☕ Bitterness", flavor_opts, index=2, key=f"bi_{rec_id}")
            adj_tart   = st.selectbox("🍋 Tartness",   flavor_opts, index=2, key=f"ta_{rec_id}")
        with fa3:
            adj_rich   = st.selectbox("🧈 Richness",   flavor_opts, index=2, key=f"ri_{rec_id}")
            adj_spicy  = st.selectbox("🌶️ Spiciness",  spice_opts,  index=0, key=f"sp_{rec_id}")

        if st.button("🔧 Generate Tweaked Recipe", key=f"tweak_{rec_id}", use_container_width=True):
            scale = new_servings / max(orig_servings, 1)

            # Multiplier map
            mult_map = {
                "Much Less (×0.5)": 0.5, "Less (×0.75)": 0.75, "Same": 1.0,
                "More (×1.25)": 1.25, "Much More (×1.5)": 1.5
            }
            sw_m = mult_map[adj_sweet]
            sa_m = mult_map[adj_salt]
            bi_m = mult_map[adj_bitter]
            ta_m = mult_map[adj_tart]
            ri_m = mult_map[adj_rich]

            # Sweetener keywords → apply sweetness multiplier
            SWEET_WORDS  = ["sugar","honey","maple syrup","condensed milk","icing sugar",
                             "powdered sugar","caster sugar","brown sugar","golden syrup","molasses","jam","nutella"]
            SALT_WORDS   = ["salt","sea salt","kosher salt","fleur de sel"]
            BITTER_WORDS = ["cocoa","dark chocolate","espresso","coffee","bittersweet","coffee powder"]
            TART_WORDS   = ["lemon juice","lime juice","orange juice","vinegar","cream of tartar",
                             "lemon zest","lime zest","buttermilk","sour cream","yogurt","citric acid"]
            RICH_WORDS   = ["butter","cream","heavy cream","double cream","mascarpone","cream cheese",
                             "egg yolk","coconut cream","full fat","ghee","crème fraîche"]

            # Health substitutions
            HEALTH_SUBS = {
                "sugar":            ("coconut sugar or honey",       0.75),
                "caster sugar":     ("coconut sugar",                0.75),
                "brown sugar":      ("coconut sugar",                0.75),
                "icing sugar":      ("powdered coconut sugar",       0.80),
                "butter":           ("unsalted butter (or coconut oil for dairy-free)", 0.85),
                "heavy cream":      ("coconut cream or light cream", 0.90),
                "double cream":     ("light cream or coconut cream", 0.90),
                "all-purpose flour":("whole wheat flour (or 50/50 mix)", 1.0),
                "plain flour":      ("whole wheat flour (or 50/50 mix)", 1.0),
                "white flour":      ("whole wheat flour",            1.0),
                "cream cheese":     ("low-fat cream cheese",         1.0),
                "milk":             ("low-fat milk or oat milk",     1.0),
            }

            # Indulgent additions by recipe type
            INDULGENT_ADDS = {
                "chocolate": "Add an extra 20% dark chocolate for deeper flavour.",
                "cream":     "Add an extra splash of heavy cream for richness.",
                "butter":    "Brown the butter before using for nutty depth.",
                "vanilla":   "Add ½ tsp extra vanilla extract.",
                "caramel":   "Drizzle salted caramel between layers.",
            }

            # Spice additions
            SPICE_ADDS = {
                "Mild":     "Add ¼ tsp ground cinnamon and a pinch of ginger.",
                "Medium":   "Add ½ tsp cinnamon, ¼ tsp ginger, pinch of cardamom.",
                "Hot":      "Add ½ tsp cinnamon, ¼ tsp cayenne pepper, ¼ tsp chilli flakes.",
                "Very Hot": "Add 1 tsp cinnamon, ½ tsp cayenne pepper, ½ tsp chilli flakes — bold!",
            }

            def parse_quantity(text):
                """Extract leading number/fraction from ingredient string."""
                text = text.strip()
                # Handle fractions like 1/2, 1/4, 3/4
                frac = re.match(r'^(\d+)\s*/\s*(\d+)', text)
                if frac:
                    return float(frac.group(1)) / float(frac.group(2)), text[frac.end():]
                # Handle mixed numbers like 1 1/2
                mixed = re.match(r'^(\d+)\s+(\d+)\s*/\s*(\d+)', text)
                if mixed:
                    whole = int(mixed.group(1))
                    num   = int(mixed.group(2))
                    den   = int(mixed.group(3))
                    return whole + num/den, text[mixed.end():]
                # Handle decimals / plain integers
                num = re.match(r'^(\d+\.?\d*)', text)
                if num:
                    return float(num.group(1)), text[num.end():]
                return None, text

            def format_qty(val):
                """Format a float quantity nicely."""
                if val == int(val):
                    return str(int(val))
                # Try common fractions
                for num, den, label in [(1,4,"¼"),(1,3,"⅓"),(1,2,"½"),(2,3,"⅔"),(3,4,"¾")]:
                    if abs(val - num/den) < 0.04:
                        return label
                for whole in range(1, 20):
                    for num, den, label in [(1,4,"¼"),(1,3,"⅓"),(1,2,"½"),(2,3,"⅔"),(3,4,"¾")]:
                        if abs(val - (whole + num/den)) < 0.04:
                            return f"{whole} {label}"
                return f"{val:.1f}".rstrip('0').rstrip('.')

            def tweak_ingredient(line, scale, sw_m, sa_m, bi_m, ta_m, ri_m,
                                  health_mode, SWEET_WORDS, SALT_WORDS,
                                  BITTER_WORDS, TART_WORDS, RICH_WORDS,
                                  HEALTH_SUBS):
                line_lower = line.lower()
                qty, rest = parse_quantity(line)

                # Detect flavor category
                is_sweet  = any(w in line_lower for w in SWEET_WORDS)
                is_salt   = any(w in line_lower for w in SALT_WORDS)
                is_bitter = any(w in line_lower for w in BITTER_WORDS)
                is_tart   = any(w in line_lower for w in TART_WORDS)
                is_rich   = any(w in line_lower for w in RICH_WORDS)

                flavor_mult = 1.0
                if is_sweet:  flavor_mult *= sw_m
                if is_salt:   flavor_mult *= sa_m
                if is_bitter: flavor_mult *= bi_m
                if is_tart:   flavor_mult *= ta_m
                if is_rich:   flavor_mult *= ri_m

                notes = []

                # Health substitutions
                if health_mode == "Healthier":
                    for keyword, (sub, sub_scale) in HEALTH_SUBS.items():
                        if keyword in line_lower:
                            notes.append(f"→ sub with {sub}")
                            flavor_mult *= sub_scale
                            break

                if qty is not None:
                    new_qty = qty * scale * flavor_mult
                    new_line = f"{format_qty(new_qty)}{rest}"
                else:
                    new_line = line

                if notes:
                    new_line += f"  *({', '.join(notes)})*"

                return new_line

            # ── Process all ingredients ──
            tweaked_lines = []
            orig_lines = [l for l in ingr.strip().split("\n") if l.strip()]
            for line in orig_lines:
                tweaked_lines.append(tweak_ingredient(
                    line, scale, sw_m, sa_m, bi_m, ta_m, ri_m,
                    health_mode, SWEET_WORDS, SALT_WORDS,
                    BITTER_WORDS, TART_WORDS, RICH_WORDS, HEALTH_SUBS
                ))

            # ── Build change notes ──
            change_notes = []
            if scale != 1.0:
                change_notes.append(f"📐 **Scaled** from {orig_servings} → {new_servings} servings (×{scale:.2f})")
            if adj_sweet != "Same":
                change_notes.append(f"🍯 Sweetness {adj_sweet.lower()} — sugar/sweeteners adjusted")
            if adj_salt  != "Same":
                change_notes.append(f"🧂 Saltiness {adj_salt.lower()} — salt adjusted")
            if adj_bitter != "Same":
                change_notes.append(f"☕ Bitterness {adj_bitter.lower()} — cocoa/coffee adjusted")
            if adj_tart  != "Same":
                change_notes.append(f"🍋 Tartness {adj_tart.lower()} — citrus/acid adjusted")
            if adj_rich  != "Same":
                change_notes.append(f"🧈 Richness {adj_rich.lower()} — cream/butter adjusted")
            if adj_spicy != "None":
                change_notes.append(f"🌶️ Spice: {SPICE_ADDS[adj_spicy]}")
            if health_mode == "Healthier":
                change_notes.append("🥗 **Healthier version** — sugar → coconut sugar/honey, butter reduced, whole grain flour suggested where applicable")
            elif health_mode == "Indulgent":
                ingr_lower = ingr.lower()
                for kw, tip in INDULGENT_ADDS.items():
                    if kw in ingr_lower:
                        change_notes.append(f"🍫 **Indulgent tip:** {tip}")
                        break
                else:
                    change_notes.append("🍫 **Indulgent version** — increase richness and flavour intensity")

            # ── Display result ──
            st.markdown("---")
            st.markdown("### ✨ Tweaked Recipe")

            if change_notes:
                st.markdown("**📝 Changes made:**")
                for note in change_notes:
                    st.markdown(f"- {note}")
                st.write("")

            st.markdown(f"**🧂 Ingredients** *(for {new_servings} servings)*")
            result_text = f"TWEAKED RECIPE: {name}\nFor {new_servings} servings\n\n"
            result_text += "CHANGES:\n" + "\n".join(f"- {n}" for n in change_notes) + "\n\n"
            result_text += "INGREDIENTS:\n"
            for line in tweaked_lines:
                st.markdown(f"• {line}")
                result_text += f"• {line}\n"

            if adj_spicy != "None":
                spice_line = f"+ {SPICE_ADDS[adj_spicy]}"
                st.markdown(f"• {spice_line}")
                result_text += f"• {spice_line}\n"

            if steps:
                st.markdown(f"\n**📋 Steps** *(unchanged — scaling is in the ingredients above)*")
                result_text += "\nSTEPS:\n"
                for line in steps.strip().split("\n"):
                    if line.strip():
                        st.markdown(f"<p style='color:#2C1A0E;margin:4px 0'>{line.strip()}</p>",
                                    unsafe_allow_html=True)
                        result_text += line.strip() + "\n"

            st.write("")
            st.download_button("📥 Download tweaked recipe",
                               data=result_text,
                               file_name=f"{name}_tweaked_{new_servings}servings.txt",
                               mime="text/plain",
                               key=f"dl_{rec_id}")

        # ── Tin Size Calculator ───────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🍰 Tin Size Calculator")
        st.caption("Convert this recipe to a different tin size or shape automatically.")

        tin1, tin2, tin3 = st.columns(3)
        SHAPES = ["Round", "Square", "Rectangular", "Loaf", "Bundt/Ring"]
        with tin1:
            orig_shape = st.selectbox("Original tin shape", SHAPES, key=f"osh_{rec_id}")
            if orig_shape == "Rectangular":
                o_w = st.number_input("Original width (cm)", value=20, min_value=5, max_value=60, key=f"ow_{rec_id}")
                o_l = st.number_input("Original length (cm)", value=30, min_value=5, max_value=60, key=f"ol_{rec_id}")
                orig_area = o_w * o_l
            elif orig_shape == "Square":
                o_s = st.number_input("Original side (cm)", value=20, min_value=5, max_value=60, key=f"os_{rec_id}")
                orig_area = o_s * o_s
            elif orig_shape == "Loaf":
                o_w = st.number_input("Original width (cm)", value=11, min_value=5, max_value=40, key=f"ow_{rec_id}")
                o_l = st.number_input("Original length (cm)", value=21, min_value=5, max_value=60, key=f"ol_{rec_id}")
                orig_area = o_w * o_l
            else:  # Round or Bundt
                o_d = st.number_input("Original diameter (cm)", value=20, min_value=5, max_value=60, key=f"od_{rec_id}")
                import math
                orig_area = math.pi * (o_d/2)**2

        with tin2:
            new_shape = st.selectbox("New tin shape", SHAPES, key=f"nsh_{rec_id}")
            if new_shape == "Rectangular":
                n_w = st.number_input("New width (cm)", value=23, min_value=5, max_value=60, key=f"nw_{rec_id}")
                n_l = st.number_input("New length (cm)", value=33, min_value=5, max_value=60, key=f"nl_{rec_id}")
                new_area = n_w * n_l
            elif new_shape == "Square":
                n_s = st.number_input("New side (cm)", value=23, min_value=5, max_value=60, key=f"ns_{rec_id}")
                new_area = n_s * n_s
            elif new_shape == "Loaf":
                n_w = st.number_input("New width (cm)", value=13, min_value=5, max_value=40, key=f"nw_{rec_id}")
                n_l = st.number_input("New length (cm)", value=23, min_value=5, max_value=60, key=f"nl_{rec_id}")
                new_area = n_w * n_l
            else:
                import math
                n_d = st.number_input("New diameter (cm)", value=23, min_value=5, max_value=60, key=f"nd_{rec_id}")
                new_area = math.pi * (n_d/2)**2

        with tin3:
            st.write("")
            tin_scale = new_area / orig_area if orig_area > 0 else 1.0
            st.metric("Scale factor", f"×{tin_scale:.2f}")
            depth_adj = st.checkbox("Adjust for depth too?", key=f"dep_{rec_id}")
            if depth_adj:
                orig_depth = st.number_input("Original depth (cm)", value=5.0, min_value=1.0, max_value=20.0, step=0.5, key=f"odp_{rec_id}")
                new_depth  = st.number_input("New depth (cm)",      value=5.0, min_value=1.0, max_value=20.0, step=0.5, key=f"ndp_{rec_id}")
                tin_scale  = tin_scale * (new_depth / orig_depth)
                st.metric("Final scale (area+depth)", f"×{tin_scale:.2f}")

        if st.button("🍰 Convert to New Tin Size", key=f"tin_{rec_id}", use_container_width=True):
            import math, re as _re
            def _parse_qty(text):
                frac = _re.match(r'^(\d+)\s*/\s*(\d+)', text.strip())
                if frac: return float(frac.group(1))/float(frac.group(2)), text[frac.end():]
                mixed = _re.match(r'^(\d+)\s+(\d+)\s*/\s*(\d+)', text.strip())
                if mixed:
                    return int(mixed.group(1))+int(mixed.group(2))/int(mixed.group(3)), text[mixed.end():]
                num = _re.match(r'^(\d+\.?\d*)', text.strip())
                if num: return float(num.group(1)), text[num.end():]
                return None, text

            def _fmt(v):
                if v == int(v): return str(int(v))
                for n,d,l in [(1,4,"¼"),(1,3,"⅓"),(1,2,"½"),(2,3,"⅔"),(3,4,"¾")]:
                    if abs(v-n/d)<0.05: return l
                for w in range(1,20):
                    for n,d,l in [(1,4,"¼"),(1,3,"⅓"),(1,2,"½"),(2,3,"⅔"),(3,4,"¾")]:
                        if abs(v-(w+n/d))<0.05: return f"{w} {l}"
                return f"{v:.1f}".rstrip('0').rstrip('.')

            # Time/temp adjustments
            time_note = ""
            temp_note = ""
            if tin_scale > 1.3:
                time_note = f"⏱️ **Baking time:** Increase by ~{int((tin_scale-1)*15)}-{int((tin_scale-1)*25)} minutes. Check with skewer."
                temp_note = "🌡️ **Temperature:** Reduce by 10-15°C if baking in a deeper/larger tin to avoid burning edges."
            elif tin_scale < 0.7:
                time_note = f"⏱️ **Baking time:** Reduce by ~{int((1-tin_scale)*15)}-{int((1-tin_scale)*20)} minutes. Check early!"
                temp_note = "🌡️ **Temperature:** You can increase by 5-10°C for smaller/shallower tins."

            st.markdown(f"### 🍰 Converted Recipe — {new_shape} tin")
            st.markdown(f"*Scale factor: ×{tin_scale:.2f} (original area: {orig_area:.0f}cm² → new area: {new_area:.0f}cm²)*")
            if time_note: st.info(time_note)
            if temp_note: st.warning(temp_note)

            tin_result = f"TIN CONVERSION: {name}\nScale: ×{tin_scale:.2f}\n\nINGREDIENTS:\n"
            st.markdown("**🧂 Converted Ingredients:**")
            for line in ingr.strip().split("\n"):
                if line.strip():
                    qty, rest = _parse_qty(line)
                    if qty is not None:
                        new_line = f"{_fmt(qty * tin_scale)}{rest}"
                    else:
                        new_line = line
                    st.markdown(f"• {new_line}")
                    tin_result += f"• {new_line}\n"

            if steps:
                st.markdown("**📋 Steps** *(quantities in steps scaled too)*")
                tin_result += "\nSTEPS:\n"
                for line in steps.strip().split("\n"):
                    if line.strip():
                        st.markdown(f"<p style='color:#2C1A0E;margin:4px 0'>{line.strip()}</p>", unsafe_allow_html=True)
                        tin_result += line.strip() + "\n"

            st.download_button("📥 Download converted recipe", data=tin_result,
                               file_name=f"{name}_tin_converted.txt", mime="text/plain",
                               key=f"tindl_{rec_id}")

        st.markdown("</div>", unsafe_allow_html=True)

        if show_delete:
            st.write("")
            if st.button(f"🗑️ Delete Recipe", key=f"del_{rec_id}"):
                delete_recipe(rec_id)
                st.success("Recipe deleted!")
                st.rerun()

# ─── Auto Categoriser ─────────────────────────────────────────────────────────
def auto_categorise(name, description="", ingredients=""):
    """Guess the best category and subcategory from recipe name/description/ingredients."""
    text = (name + " " + description + " " + ingredients).lower()

    rules = [
        # (category, subcategory, keywords)
        ("🌍 Global Desserts", "Italian",        ["tiramisu", "cannoli", "panna cotta", "panettone", "cassata", "sfogliatelle", "zabaglione"]),
        ("🌍 Global Desserts", "French",         ["eclair", "éclair", "paris-brest", "mille-feuille", "opera cake", "opera torte", "madeleine", "financier", "canele", "canelé", "clafoutis", "tarte tatin", "croissant", "pain au chocolat", "kouign"]),
        ("🌍 Global Desserts", "Japanese",       ["matcha", "mochi", "dorayaki", "taiyaki", "castella", "wagashi", "daifuku"]),
        ("🌍 Global Desserts", "Middle Eastern", ["kunafa", "baklava", "basbousa", "ma'amoul", "umm ali", "halawet"]),
        ("🌍 Global Desserts", "Indian",         ["rasmalai", "gulab jamun", "barfi", "halwa", "kheer", "ladoo", "jalebi"]),
        ("🌍 Global Desserts", "Latin American", ["tres leches", "churro", "alfajor", "brigadeiro", "pastel de nata", "dulce de leche cake"]),
        ("🌍 Global Desserts", "Eastern European",["medovik", "sachertorte", "dobos", "baumkuchen", "schwarzwälder", "black forest"]),
        ("🌍 Global Desserts", "American",       ["cheesecake", "brownie", "cupcake", "banana bread", "red velvet", "pecan pie", "key lime"]),

        ("🥐 Viennoiserie",  "Croissants",      ["croissant", "pain au chocolat", "kouign-amann", "danish", "brioche", "laminated"]),

        ("🍪 Cookies & Biscuits", "French Pastries", ["macaron", "madeleine", "financier", "tuile", "florentine"]),
        ("🍪 Cookies & Biscuits", "Drop Cookies",    ["chocolate chip cookie", "oatmeal cookie", "peanut butter cookie"]),
        ("🍪 Cookies & Biscuits", "Shortbread",      ["shortbread", "sablé", "sable"]),
        ("🍪 Cookies & Biscuits", "Biscotti",        ["biscotti", "cantuccini"]),

        ("🥧 Pies & Tarts",  "Fruit Pies",      ["apple pie", "cherry pie", "blueberry pie", "peach pie", "banoffee"]),
        ("🥧 Pies & Tarts",  "Custard Pies",    ["custard pie", "lemon meringue", "key lime pie", "pumpkin pie"]),
        ("🥧 Pies & Tarts",  "Nut Pies",        ["pecan pie", "walnut pie", "almond tart", "frangipane"]),
        ("🥧 Pies & Tarts",  "Classic Tarts",   ["tart", "tarte", "galette"]),

        ("🍮 Custards & Set Desserts", "Crème Brûlée", ["crème brûlée", "creme brulee"]),
        ("🍮 Custards & Set Desserts", "Flan & Panna Cotta", ["flan", "panna cotta", "posset"]),
        ("🍮 Custards & Set Desserts", "Puddings",     ["bread pudding", "rice pudding", "steamed pudding", "sticky toffee"]),
        ("🍮 Custards & Set Desserts", "Mousses",      ["mousse", "bavarois", "bavarian cream"]),

        ("🎂 Buttercreams & Frostings", "Swiss Meringue",   ["swiss meringue buttercream", "smbc"]),
        ("🎂 Buttercreams & Frostings", "Italian Meringue", ["italian meringue buttercream", "imbc"]),
        ("🎂 Buttercreams & Frostings", "American",         ["american buttercream", "simple buttercream"]),
        ("🎂 Buttercreams & Frostings", "Cream Cheese",     ["cream cheese frosting", "cream cheese buttercream"]),
        ("🎂 Buttercreams & Frostings", "Whipped Cream",    ["whipped cream", "chantilly"]),
        ("🎂 Buttercreams & Frostings", "Korean Glossy",    ["korean buttercream", "korean glossy"]),

        ("🍫 Ganaches & Glazes", "Mirror Glaze",      ["mirror glaze", "mirror cake"]),
        ("🍫 Ganaches & Glazes", "Dark Chocolate",    ["dark chocolate ganache", "dark ganache"]),
        ("🍫 Ganaches & Glazes", "White Chocolate",   ["white chocolate ganache"]),
        ("🍫 Ganaches & Glazes", "Whipped",           ["whipped ganache"]),

        ("🥛 Fillings", "Fruit-Based",     ["compote", "coulis", "curd", "jam filling", "fruit reduction", "confit"]),
        ("🥛 Fillings", "Custard-Based",   ["pastry cream", "crème pâtissière", "creme patissiere", "crème anglaise", "cremeux", "crémeux"]),
        ("🥛 Fillings", "Caramel-Based",   ["salted caramel", "dulce de leche", "butterscotch filling", "caramel filling"]),
        ("🥛 Fillings", "Nut-Based",       ["praline", "frangipane", "pistachio cream filling", "peanut butter filling"]),
        ("🥛 Fillings", "Chocolate-Based", ["ganache filling", "chocolate mousse filling", "truffle filling"]),

        ("🫧 Cake Bases", "Foam/Air-Based",    ["genoise", "génoise", "chiffon", "angel food", "joconde", "dacquoise", "ladyfinger", "savoiardi", "swiss roll", "roulade"]),
        ("🫧 Cake Bases", "Butter-Based",      ["pound cake", "victoria sponge", "madeira", "gateau breton", "butter cake", "loaf cake"]),
        ("🫧 Cake Bases", "Oil-Based",         ["carrot cake", "olive oil cake", "oil cake"]),
        ("🫧 Cake Bases", "Chocolate & Rich",  ["mud cake", "devil's food", "flourless chocolate", "sachertorte base", "black forest base"]),
        ("🫧 Cake Bases", "Nut-Based",         ["almond cake", "pistachio cake", "hazelnut cake", "walnut cake"]),
        ("🫧 Cake Bases", "Regional",          ["tres leches base", "medovik base", "castella base", "opera base"]),

        ("✨ Decorations & Techniques", "Buttercream Piping", ["piping", "rosette", "swirl decoration", "flower piping"]),
        ("✨ Decorations & Techniques", "Chocolate Techniques", ["tempered chocolate", "chocolate shard", "chocolate drip"]),
        ("✨ Decorations & Techniques", "Sugar Work",           ["caramel cage", "spun sugar", "isomalt", "pulled sugar"]),
    ]

    for category, subcategory, keywords in rules:
        for kw in keywords:
            if kw in text:
                return category, subcategory

    # Generic fallback by broad word
    if any(w in text for w in ["cake", "sponge", "layer cake"]):
        return "🫧 Cake Bases", ""
    if any(w in text for w in ["cookie", "biscuit"]):
        return "🍪 Cookies & Biscuits", ""
    if any(w in text for w in ["tart", "pie", "galette"]):
        return "🥧 Pies & Tarts", ""
    if any(w in text for w in ["mousse", "custard", "pudding", "panna"]):
        return "🍮 Custards & Set Desserts", ""
    if any(w in text for w in ["buttercream", "frosting", "icing"]):
        return "🎂 Buttercreams & Frostings", ""
    if any(w in text for w in ["ganache", "glaze"]):
        return "🍫 Ganaches & Glazes", ""
    if any(w in text for w in ["filling", "curd", "compote", "coulis"]):
        return "🥛 Fillings", ""

    return list(CATEGORIES.keys())[0], ""  # default


# ─── Pages ─────────────────────────────────────────────────────────────────────

def page_home():
    st.markdown("""
    <div class='hero-banner'>
        <h1>🎂 My Baking Studio</h1>
        <p>Your personal compendium of recipes, techniques, flavors & inspirations</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM recipes")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT category) FROM recipes")
    cats = c.fetchone()[0]
    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Total Recipes", total)
    with col2:
        st.metric("🗂️ Categories", cats)
    with col3:
        st.metric("👩‍🍳 Chefs to Follow", len(CHEF_INSTAGRAMS))
    with col4:
        st.metric("🎬 Technique Guides", sum(len(v) for v in TECHNIQUE_VIDEOS.values()))

    st.markdown("---")
    st.markdown("### 🗺️ Browse by Category")
    cols = st.columns(2)
    for i, (cat, info) in enumerate(CATEGORIES.items()):
        with cols[i % 2]:
            subcats_preview = ' · '.join(info['subcategories'][:3]) + '...'
            st.markdown(f"<small style='color:#888'>{subcats_preview}</small>", unsafe_allow_html=True)
            if st.button(f"{cat}", key=f"home_cat_{i}", use_container_width=True):
                st.session_state["nav_page"] = "📚 Recipe Library"
                st.session_state["filter_cat"] = cat
                st.rerun()

    st.markdown("---")
    st.markdown("### 📌 Quick Tips")
    tips = [
        "**Room temp butter** is key for most buttercreams — test by pressing; it should leave an indent.",
        "**Mise en place** — weigh & prep all ingredients before you start. Baking is chemistry!",
        "**Macaron feet** form best when shells are properly macaronaged and rest 30 min before baking.",
        "**Mirror glaze** should be applied at 35°C for best flow and shine.",
        "**Ganache ratios**: 1:1 for filling, 2:1 for truffles, 1:2 for pourable glaze.",
    ]
    for tip in tips:
        st.info(tip)


def page_browse():
    st.markdown("<div class='section-header'>📚 Recipe Library</div>", unsafe_allow_html=True)

    # Pick up category from home page button click
    preselect_cat = st.session_state.pop("filter_cat", "All")
    all_cats = ["All"] + list(CATEGORIES.keys())
    preselect_idx = all_cats.index(preselect_cat) if preselect_cat in all_cats else 0

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        selected_cat = st.selectbox("Filter by Category", all_cats, index=preselect_idx)
    with col2:
        search = st.text_input("🔍 Search recipes...", placeholder="e.g. chocolate, ganache, tart...")
    with col3:
        sort_by = st.selectbox("Sort", ["Name", "Sweetness ↑", "Richness ↑"])

    conn = get_db()
    c = conn.cursor()
    if selected_cat == "All":
        if search:
            c.execute("SELECT * FROM recipes WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?",
                      (f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            c.execute("SELECT * FROM recipes")
    else:
        if search:
            c.execute("SELECT * FROM recipes WHERE category=? AND (name LIKE ? OR description LIKE ?)",
                      (selected_cat, f"%{search}%", f"%{search}%"))
        else:
            c.execute("SELECT * FROM recipes WHERE category=?", (selected_cat,))
    rows = c.fetchall()
    conn.close()

    # Sorting
    if sort_by == "Sweetness ↑":
        rows = sorted(rows, key=lambda r: -r[8])
    elif sort_by == "Richness ↑":
        rows = sorted(rows, key=lambda r: -r[10])
    else:
        rows = sorted(rows, key=lambda r: r[1])

    st.markdown(f"**{len(rows)} recipe(s) found**")

    if not rows:
        st.info("No recipes yet! Add some in the 'Add Recipe' or 'Import from URL' section.")
        return

    # Group by category
    grouped = {}
    for r in rows:
        key = r[2] or "Uncategorized"
        grouped.setdefault(key, []).append(r)

    for cat, recipes in grouped.items():
        st.markdown(f"### {cat}")
        for row in recipes:
            render_recipe_card(row, show_delete=True)


def page_add_recipe():
    st.markdown("<div class='section-header'>✏️ Add Your Own Recipe</div>", unsafe_allow_html=True)

    # Live category suggestion (outside the form so it updates as user types)
    preview_name = st.text_input("Recipe Name *", placeholder="e.g. Classic Génoise Sponge", key="add_name_preview")
    if preview_name:
        sug_cat, sug_sub = auto_categorise(preview_name)
        st.info(f"🤖 Suggested category: **{sug_cat}** › {sug_sub or 'General'}")
    else:
        sug_cat, sug_sub = list(CATEGORIES.keys())[0], ""

    all_cats = list(CATEGORIES.keys())
    sug_idx = all_cats.index(sug_cat) if sug_cat in all_cats else 0

    with st.form("add_recipe_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Recipe Name (confirm) *", value=preview_name)
            category = st.selectbox("Category *", all_cats, index=sug_idx)
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Advanced"])
            region = st.text_input("Region / Origin", placeholder="e.g. French, Japanese...")
        with col2:
            subcategory = st.text_input("Sub-category", value=sug_sub, placeholder="e.g. Foam/Air-Based")
            tags = st.text_input("Tags (comma-separated)", placeholder="e.g. chocolate, no-bake, vegan")
            source_url = st.text_input("📖 Recipe Source URL")
            video_url = st.text_input("▶️ YouTube / Video URL")
            instagram_url = st.text_input("📸 Instagram URL")

        description = st.text_area("Short Description", placeholder="What makes this recipe special?", height=80)
        ingredients = st.text_area("Ingredients (one per line) *", placeholder="200g dark chocolate\n100ml heavy cream\n...", height=200)
        steps = st.text_area("Method / Steps", placeholder="Step 1: ...\nStep 2: ...", height=200)
        notes = st.text_area("Personal Notes", placeholder="Tips, substitutions, things to remember...", height=80)

        st.markdown("### 🍭 Flavor Profile (rate 1-10)")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            sweetness = st.slider("🍯 Sweetness", 1, 10, 5)
            richness = st.slider("🧈 Richness", 1, 10, 5)
        with fc2:
            tartness = st.slider("🍋 Tartness", 1, 10, 3)
            bitterness = st.slider("☕ Bitterness", 1, 10, 2)
        with fc3:
            nuttiness = st.slider("🥜 Nuttiness", 1, 10, 2)
            floral = st.slider("🌸 Floral", 1, 10, 1)

        submitted = st.form_submit_button("💾 Save Recipe", use_container_width=True)
        if submitted:
            if not name or not ingredients:
                st.error("Please fill in at least Name and Ingredients.")
            else:
                save_recipe({
                    "name": name, "category": category, "subcategory": subcategory,
                    "description": description, "ingredients": ingredients, "steps": steps,
                    "sweetness": sweetness, "tartness": tartness, "richness": richness,
                    "bitterness": bitterness, "nuttiness": nuttiness, "floral": floral,
                    "source_url": source_url, "video_url": video_url, "instagram_url": instagram_url,
                    "region": region, "difficulty": difficulty, "tags": tags, "notes": notes
                })
                st.success(f"✅ '{name}' saved to your library!")
                st.balloons()


def page_import_url():
    st.markdown("<div class='section-header'>🔗 Import Recipe from URL</div>", unsafe_allow_html=True)
    st.info("Paste any recipe URL and the agent will try to automatically extract the ingredients and steps.")

    url = st.text_input("📎 Recipe URL", placeholder="https://www.seriouseats.com/some-recipe...")

    if st.button("🔍 Extract Recipe from URL") and url:
        with st.spinner("Fetching and extracting recipe..."):
            result = scrape_recipe_from_url(url)
        if result["success"]:
            st.success("✅ Recipe extracted! Review and save below.")
            st.session_state["scraped"] = result
            st.session_state["scraped_url"] = url
        else:
            st.warning(f"Could not fully extract. You can still fill in manually. Error: {result.get('error', 'Unknown')}")
            st.session_state["scraped"] = {"name": "", "ingredients": "", "steps": "", "description": ""}
            st.session_state["scraped_url"] = url

    if "scraped" in st.session_state:
        r = st.session_state["scraped"]

        # Auto-detect category from name + description + ingredients
        guessed_cat, guessed_subcat = auto_categorise(
            r.get("name", ""), r.get("description", ""), r.get("ingredients", "")
        )
        all_cats = list(CATEGORIES.keys())
        cat_idx = all_cats.index(guessed_cat) if guessed_cat in all_cats else 0

        st.markdown("### 📋 Review & Save")
        if guessed_cat != all_cats[0] or guessed_subcat:
            st.success(f"🤖 Auto-detected category: **{guessed_cat}** › {guessed_subcat or 'General'} — change below if needed.")
        else:
            st.warning("⚠️ Could not auto-detect category — please select the correct one below before saving.")

        with st.form("import_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Recipe Name", value=r.get("name", ""))
                category = st.selectbox("Category", all_cats, index=cat_idx)
                difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Advanced"])
            with col2:
                subcategory = st.text_input("Sub-category", value=guessed_subcat)
                tags = st.text_input("Tags")
                video_url = st.text_input("Video URL (optional)")
                instagram_url = st.text_input("Instagram URL (optional)")

            description = st.text_area("Description", value=r.get("description", ""), height=80)
            ingredients = st.text_area("Ingredients", value=r.get("ingredients", ""), height=200)
            steps = st.text_area("Steps / Method", value=r.get("steps", ""), height=200)

            st.markdown("### 🍭 Flavor Profile")
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                sweetness = st.slider("🍯 Sweetness", 1, 10, 5)
                richness = st.slider("🧈 Richness", 1, 10, 5)
            with fc2:
                tartness = st.slider("🍋 Tartness", 1, 10, 3)
                bitterness = st.slider("☕ Bitterness", 1, 10, 2)
            with fc3:
                nuttiness = st.slider("🥜 Nuttiness", 1, 10, 2)
                floral = st.slider("🌸 Floral", 1, 10, 1)

            submitted = st.form_submit_button("💾 Save to Library", use_container_width=True)
            if submitted and name:
                save_recipe({
                    "name": name, "category": category, "subcategory": subcategory,
                    "description": description, "ingredients": ingredients, "steps": steps,
                    "sweetness": sweetness, "tartness": tartness, "richness": richness,
                    "bitterness": bitterness, "nuttiness": nuttiness, "floral": floral,
                    "source_url": st.session_state.get("scraped_url", ""),
                    "video_url": video_url, "instagram_url": instagram_url,
                    "region": "", "difficulty": difficulty, "tags": tags, "notes": "",
                    "thumbnail_url": st.session_state.get("scraped", {}).get("thumbnail_url", "")
                })
                st.success(f"✅ '{name}' saved!")
                del st.session_state["scraped"]
                st.balloons()


def page_flavor_explorer():
    st.markdown("<div class='section-header'>🎨 Flavor Explorer</div>", unsafe_allow_html=True)
    st.markdown("Use the sliders below to find recipes that match the flavor profile you're looking for.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Target Flavor Profile**")
        sw = st.slider("🍯 Sweetness", 1, 10, 7)
        ta = st.slider("🍋 Tartness", 1, 10, 3)
        ri = st.slider("🧈 Richness", 1, 10, 6)
        bi = st.slider("☕ Bitterness", 1, 10, 2)
        nu = st.slider("🥜 Nuttiness", 1, 10, 3)
        fl = st.slider("🌸 Floral", 1, 10, 2)
        tolerance = st.slider("Tolerance (±)", 1, 5, 2)

    with col2:
        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT * FROM recipes WHERE
            ABS(flavor_sweetness - ?) <= ? AND
            ABS(flavor_tartness - ?) <= ? AND
            ABS(flavor_richness - ?) <= ?""",
            (sw, tolerance, ta, tolerance, ri, tolerance))
        matches = c.fetchall()
        conn.close()

        st.markdown(f"### 🎯 {len(matches)} Recipe(s) Matching Your Taste")
        if not matches:
            st.info("No matches yet — add more recipes to your library first!")
        for row in matches:
            render_recipe_card(row)

        st.markdown("---")
        st.markdown("### 🍰 Flavor Pairing Ideas")
        pairing_tips = {
            "High Sweet + High Tart": "Classic! Think lemon curd tarts, passion fruit mousse, or raspberry buttercream.",
            "High Rich + Low Tart": "Indulgent — dark chocolate ganache, caramel mousse, moist pound cake.",
            "High Floral + Low Bitter": "Delicate — rose panna cotta, lavender cream, elderflower jelly.",
            "High Nutty + Medium Rich": "Earthy comfort — praline filling, frangipane tarts, hazelnut buttercream.",
            "High Bitter + Low Sweet": "Sophisticated — dark chocolate tart, espresso entremet, cocoa sponge.",
        }
        for combo, suggestion in pairing_tips.items():
            st.markdown(f"**{combo}**: {suggestion}")


def page_techniques():
    st.markdown("<div class='section-header'>🎬 Technique Videos & Guides</div>", unsafe_allow_html=True)
    st.info("Click any link to open the YouTube search for that technique. Find your favourite tutorial and come back to save the link to a recipe!")

    for category, videos in TECHNIQUE_VIDEOS.items():
        st.markdown(f"### {category}")
        cols = st.columns(2)
        for i, v in enumerate(videos):
            with cols[i % 2]:
                st.markdown(f"""
                <div class='recipe-card'>
                    <b>{v['title']}</b><br>
                    <a href='{v['url']}' target='_blank' style='color:#C87941'>▶️ Search on YouTube →</a>
                </div>
                """, unsafe_allow_html=True)


def page_chefs():
    st.markdown("<div class='section-header'>👩‍🍳 Chef Inspirations</div>", unsafe_allow_html=True)
    st.markdown("These are some incredible pastry chefs and bakers to follow for daily inspiration!")

    cols = st.columns(2)
    for i, chef in enumerate(CHEF_INSTAGRAMS):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='recipe-card'>
                <b>{chef['name']}</b> &nbsp;<span class='tag-pill'>{chef['handle']}</span><br>
                <small style='color:#888'>{chef['specialty']}</small><br><br>
                <a href='{chef['url']}' target='_blank' style='color:#C87941'>📸 Open Instagram →</a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📺 YouTube Channels to Bookmark")
    yt_channels = [
        ("Binging with Babish", "Modern takes & techniques", "https://www.youtube.com/@BabishCulinaryUniverse"),
        ("Joshua Weissman", "Scratch baking & pastry", "https://www.youtube.com/@JoshuaWeissman"),
        ("Sugar Geek Show", "Cake decorating tutorials", "https://www.youtube.com/@SugarGeekShow"),
        ("Chef's Table: Pastry", "Documentary-style deep dives", "https://www.youtube.com/results?search_query=chef%27s+table+pastry"),
        ("Kirsten Tibballs", "Professional chocolate & pastry", "https://www.youtube.com/@kirstentibballs"),
        ("Adam Ragusea", "Science of baking explained", "https://www.youtube.com/@aragusea"),
        ("Nino's Home", "Elegant Japanese pastry", "https://www.youtube.com/@ninoshome"),
        ("École Valrhona", "Chocolate techniques", "https://www.youtube.com/results?search_query=ecole+valrhona+tutorial"),
    ]
    cols2 = st.columns(2)
    for i, (name, desc, url) in enumerate(yt_channels):
        with cols2[i % 2]:
            st.markdown(f"""
            <div class='recipe-card'>
                <b>{name}</b><br>
                <small style='color:#888'>{desc}</small><br>
                <a href='{url}' target='_blank' style='color:#C87941'>▶️ Watch on YouTube →</a>
            </div>
            """, unsafe_allow_html=True)


def page_global_index():
    st.markdown("<div class='section-header'>🌍 World Dessert Index</div>", unsafe_allow_html=True)
    st.markdown("Explore classic desserts organized by region and style.")

    WORLD_INDEX = {
        "🇫🇷 French": {
            "Classics": ["Éclair", "Paris-Brest", "Mille-Feuille", "Tarte Tatin", "Opera Cake", "Madeleines", "Financiers", "Canelés"],
            "Techniques": ["Pâte Choux", "Pâte Sablée", "Feuilletage (Puff Pastry)", "Crème Pâtissière"],
        },
        "🇮🇹 Italian": {
            "Classics": ["Tiramisu", "Cannoli", "Panettone", "Panna Cotta", "Cassata", "Sfogliatelle"],
            "Techniques": ["Sabayon", "Zabaglione", "Italian Meringue"],
        },
        "🇯🇵 Japanese": {
            "Classics": ["Castella", "Matcha Roll Cake", "Mochi", "Dorayaki", "Taiyaki", "Japanese Cotton Cheesecake"],
            "Techniques": ["Tangzhong", "Mochi stretching", "Japanese-style whipped cream"],
        },
        "🇱🇧🇹🇷 Middle Eastern": {
            "Classics": ["Kunafa", "Baklava", "Basbousa", "Ma'amoul", "Umm Ali", "Halawet el Jibn"],
            "Techniques": ["Kataifi pastry", "Orange blossom water flavoring", "Rose water infusion"],
        },
        "🇮🇳 Indian": {
            "Classics": ["Rasmalai Cake", "Gulab Jamun Cheesecake", "Barfi", "Kheer", "Halwa", "Mishti Doi"],
            "Techniques": ["Cardamom & saffron infusion", "Condensed milk reduction"],
        },
        "🇺🇸 American": {
            "Classics": ["New York Cheesecake", "Brownies", "Cupcakes", "Banana Bread", "Red Velvet", "Pecan Pie"],
            "Techniques": ["American Buttercream", "Cream cheese frosting"],
        },
        "🇲🇽🇧🇷 Latin American": {
            "Classics": ["Tres Leches", "Churros", "Flan", "Alfajores", "Brigadeiro", "Pastel de Nata"],
            "Techniques": ["Dulce de Leche making", "Tres leches soaking"],
        },
        "🇷🇺🇩🇪 European": {
            "Classics": ["Medovik (Russian Honey Cake)", "Schwarzwälder Kirschtorte", "Sachertorte", "Baumkuchen", "Dobos Torte"],
            "Techniques": ["Sour cream frostings", "Layer cake construction"],
        },
    }

    selected_region = st.selectbox("Select Region", list(WORLD_INDEX.keys()))
    data = WORLD_INDEX[selected_region]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🍰 Classic Desserts")
        for item in data.get("Classics", []):
            yt_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(item + ' recipe tutorial')}"
            st.markdown(f"• **{item}** — [▶️ Watch]({yt_url})")
    with col2:
        st.markdown("#### 🛠️ Key Techniques")
        for item in data.get("Techniques", []):
            yt_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(item + ' tutorial')}"
            st.markdown(f"• **{item}** — [▶️ Watch]({yt_url})")


def page_full_index():
    st.markdown("<div class='section-header'>📖 Complete Baking Index</div>", unsafe_allow_html=True)
    st.markdown("Your full reference guide — click any item to search for recipes and tutorials.")

    FULL_INDEX = {
        "🫧 Cake Bases": {
            "Foam / Air-Based": ["Genoise", "Sponge Cake", "Chiffon", "Angel Food", "Japanese Cotton Cheesecake", "Joconde", "Biscuit Roll", "Dacquoise", "Ladyfingers (Savoiardi)"],
            "Butter-Based": ["Pound Cake", "Madeira Cake", "Butter Cake", "Victoria Sponge", "Marble Cake", "Tea Cakes", "Loaf Cakes", "Gateau Breton"],
            "Oil-Based": ["Carrot Cake", "Olive Oil Cake", "Chocolate Oil Cake", "Red Velvet"],
            "Chocolate & Rich": ["Mud Cake", "Devil's Food Cake", "Flourless Chocolate Cake", "Sachertorte", "Black Forest Base"],
            "Nut-Based": ["Almond Cake", "Pistachio Cake", "Hazelnut Cake", "Walnut Cake"],
            "Regional": ["Basbousa", "Tres Leches", "Castella", "Opera Cake", "Medovik", "Tiramisu Base"],
        },
        "🥛 Fillings": {
            "Fruit-Based": ["Compote", "Coulis", "Jam", "Lemon Curd", "Passionfruit Curd", "Fruit Reduction", "Confit"],
            "Cream-Based": ["Whipped Cream", "Stabilized Cream", "Diplomat Cream", "Mousseline"],
            "Custard-Based": ["Pastry Cream", "Crème Pâtissière", "Crème Anglaise", "Bavarian Cream", "Crémeux"],
            "Chocolate-Based": ["Dark Ganache", "Whipped Ganache", "Chocolate Mousse", "Truffle Filling"],
            "Nut-Based": ["Praline Paste", "Frangipane", "Pistachio Cream", "Peanut Butter Filling"],
            "Caramel-Based": ["Salted Caramel", "Dulce de Leche", "Butterscotch"],
        },
        "🎂 Buttercreams": {
            "Types": ["American", "Swiss Meringue", "Italian Meringue", "French", "German", "Ermine (Flour-based)", "Korean Glossy", "Cream Cheese", "Chocolate Buttercream"],
        },
        "🍫 Ganaches & Glazes": {
            "Ganaches": ["Dark Chocolate", "Milk Chocolate", "White Chocolate", "Whipped Ganache", "Water Ganache", "Flavoured Ganache"],
            "Glazes": ["Mirror Glaze", "Neutral Glaze", "Chocolate Glaze", "Caramel Glaze", "Fruit Glaze", "Royal Icing"],
        },
        "🍪 Cookies & Biscuits": {
            "Types": ["Shortbread", "Sugar Cookies", "Chocolate Chip", "Macarons", "Madeleines", "Biscotti", "Florentines", "Tuiles"],
        },
        "🥧 Pies & Tarts": {
            "Pies": ["Apple Pie", "Pumpkin Pie", "Pecan Pie", "Key Lime Pie", "Banoffee Pie", "Lemon Meringue Pie"],
            "Tarts": ["Fruit Tart", "Chocolate Tart", "Tarte Tatin", "Bakewell Tart", "Custard Tart"],
        },
        "🍮 Custards & Set Desserts": {
            "Types": ["Crème Brûlée", "Flan", "Panna Cotta", "Bread Pudding", "Rice Pudding", "Clafoutis", "Posset"],
        },
        "✨ Decorating Techniques": {
            "Piping": ["Rosettes", "Swirls", "Ruffles", "Petals", "Stars", "Basketweave", "Rope border"],
            "Sugar Work": ["Caramel Cage", "Spun Sugar", "Pulled Sugar", "Blown Sugar", "Isomalt Shards"],
            "Chocolate": ["Tempering", "Shards & Curls", "Chocolate Drip", "Chocolate Flowers", "Spray"],
            "Fondant": ["Draping", "Figures", "Embossing", "Ruffles"],
        },
    }

    selected_section = st.selectbox("Jump to Section", list(FULL_INDEX.keys()))
    st.write("")
    section = FULL_INDEX[selected_section]

    for subcat, items in section.items():
        st.markdown(f"**{subcat}**")
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                yt_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(item + ' recipe baking')}"
                recipe_url = f"https://www.google.com/search?q={urllib.parse.quote(item + ' best recipe')}"
                st.markdown(f"🔹 **{item}**<br><small>[Recipe]({recipe_url}) · [Video]({yt_url})</small>", unsafe_allow_html=True)
        st.write("")



# ─── Recipe Finder ────────────────────────────────────────────────────────────
def page_recipe_finder():
    st.markdown("<div class='section-header'>🔍 Recipe Finder & Comparator</div>", unsafe_allow_html=True)
    st.markdown("Type any dessert — the app finds and extracts real recipes from top baking sites directly inside the app.")

    search_term = st.text_input("🔍 What do you want to bake?",
                                 placeholder="e.g. black forest cake, tiramisu, crème brûlée...")

    # These sites have reliable JSON-LD recipe data
    TRUSTED_SITES = [
        "recipetineats.com",
        "sallysbakingaddiction.com",
        "preppykitchen.com",
        "handletheheat.com",
        "seriouseats.com",
        "bbcgoodfood.com",
        "sugarspunrun.com",
        "kingarthurbaking.com",
        "tasteofhome.com",
        "cloudykitchen.com",
        "joyfoodsunshine.com",
        "livewellbakeoften.com",
    ]

    def google_search_recipe_urls(term, sites, max_results=10):
        """Use Google to find direct recipe page URLs for a given term on specific sites."""
        found_urls = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

        for site in sites:
            if len(found_urls) >= max_results:
                break
            try:
                # Google site-specific search
                query = urllib.parse.quote(f'{term} recipe site:{site}')
                google_url = f"https://www.google.com/search?q={query}&num=3"
                resp = requests.get(google_url, headers=headers, timeout=10)
                soup = BeautifulSoup(resp.text, "html.parser")

                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    # Google wraps URLs in /url?q=
                    if "/url?q=" in href:
                        actual = href.split("/url?q=")[1].split("&")[0]
                        actual = urllib.parse.unquote(actual)
                        if site in actual and "http" in actual:
                            # Filter out category/search/tag pages
                            skip_patterns = [
                                "?s=", "/search", "/category/", "/tag/",
                                "/page/", "/author/", "#", "google.com",
                                "youtube.com", "/feed", "wp-json"
                            ]
                            if not any(p in actual for p in skip_patterns):
                                # Must have a meaningful slug
                                path_parts = actual.rstrip("/").split("/")
                                if path_parts and len(path_parts[-1]) > 8:
                                    if actual not in found_urls:
                                        found_urls.append((site, actual))
                                        break
            except Exception:
                continue

        return found_urls

    def scrape_recipe(url, site_name):
        """Extract full recipe from a URL using JSON-LD first."""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            resp = requests.get(url, headers=headers, timeout=12)
            soup = BeautifulSoup(resp.text, "html.parser")

            # ── JSON-LD (most reliable) ────────────────────────────────────
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    raw = script.string
                    if not raw: continue
                    data = json.loads(raw)
                    items = data.get("@graph", [data]) if isinstance(data, dict) else data
                    if not isinstance(items, list): items = [items]

                    for item in items:
                        rtype = item.get("@type", "")
                        if isinstance(rtype, list): rtype = " ".join(rtype)
                        if "Recipe" not in rtype: continue

                        name = item.get("name", "")
                        desc = item.get("description", "")

                        # Ingredients
                        raw_ingr = item.get("recipeIngredient", [])
                        ingredients = "\n".join(
                            re.sub(r'\s+', ' ', i).strip()
                            for i in raw_ingr if isinstance(i, str) and i.strip()
                        )

                        # Instructions
                        instructions = item.get("recipeInstructions", [])
                        steps_lines = []
                        step_num = 1
                        if isinstance(instructions, str):
                            steps_lines = [BeautifulSoup(instructions, "html.parser").get_text().strip()]
                        elif isinstance(instructions, list):
                            for step in instructions:
                                if isinstance(step, dict):
                                    if step.get("@type") == "HowToSection":
                                        for sub in step.get("itemListElement", []):
                                            txt = sub.get("text","").strip() if isinstance(sub,dict) else str(sub)
                                            txt = BeautifulSoup(txt,"html.parser").get_text().strip()
                                            if txt:
                                                steps_lines.append(f"Step {step_num}: {txt}")
                                                step_num += 1
                                    else:
                                        txt = step.get("text", step.get("name","")).strip()
                                        txt = BeautifulSoup(txt,"html.parser").get_text().strip()
                                        if txt:
                                            steps_lines.append(f"Step {step_num}: {txt}")
                                            step_num += 1
                                elif isinstance(step, str) and step.strip():
                                    steps_lines.append(f"Step {step_num}: {step.strip()}")
                                    step_num += 1

                        steps = "\n".join(steps_lines)

                        # Thumbnail
                        thumb = ""
                        img = item.get("image", "")
                        if isinstance(img, str): thumb = img
                        elif isinstance(img, list) and img:
                            first = img[0]
                            thumb = first.get("url", first) if isinstance(first, dict) else str(first)
                        elif isinstance(img, dict): thumb = img.get("url", "")

                        # Extra metadata
                        prep_time = item.get("prepTime", "")
                        cook_time = item.get("cookTime", "")
                        servings  = item.get("recipeYield", "")

                        # og:image fallback
                        if not thumb:
                            og = soup.find("meta", property="og:image")
                            if og: thumb = og.get("content", "")

                        if name and ingredients:
                            return {
                                "name": name, "description": desc,
                                "ingredients": ingredients, "steps": steps,
                                "thumbnail_url": thumb, "source_url": url,
                                "site_name": site_name,
                                "prep_time": prep_time, "cook_time": cook_time,
                                "servings": servings, "success": True
                            }
                except Exception:
                    continue

            return {"success": False, "site_name": site_name, "source_url": url}

        except Exception as e:
            return {"success": False, "site_name": site_name, "source_url": url, "error": str(e)}

    # ── Search button ────────────────────────────────────────────────────────
    if st.button("🔍 Find & Extract Recipes", use_container_width=True) and search_term:
        st.session_state["finder_term"] = search_term
        st.session_state["finder_extracted"] = []
        st.session_state["finder_compare"] = {}

        progress_bar = st.progress(0)
        status_box   = st.empty()

        status_box.info("🔎 Searching Google for top recipe pages...")
        found_urls = google_search_recipe_urls(search_term, TRUSTED_SITES, max_results=10)

        extracted = []
        for i, (site, url) in enumerate(found_urls):
            site_label = site.replace(".com","").replace("www.","").replace("-"," ").title()
            status_box.info(f"📥 Extracting recipe from **{site_label}** ({i+1}/{len(found_urls)})...")
            progress_bar.progress((i + 1) / max(len(found_urls), 1))

            result = scrape_recipe(url, site_label)
            if result["success"]:
                extracted.append(result)

        progress_bar.empty()
        status_box.empty()
        st.session_state["finder_extracted"] = extracted

        if not extracted:
            st.warning("⚠️ Could not extract recipes automatically. Try the manual URL import instead — go to 🔗 Import from URL and paste any recipe link.")

    # ── Display results ───────────────────────────────────────────────────────
    if st.session_state.get("finder_extracted"):
        term    = st.session_state["finder_term"]
        recipes = st.session_state["finder_extracted"]

        st.markdown(f"### 🍰 Found **{len(recipes)}** recipes for: *{term}*")

        tab_labels = [f"#{i+1} {r['site_name']}" for i, r in enumerate(recipes)]
        tabs = st.tabs(tab_labels)
        compare_data = st.session_state.get("finder_compare", {})

        for i, (tab, r) in enumerate(zip(tabs, recipes)):
            with tab:
                # Header
                hc1, hc2 = st.columns([1, 3])
                with hc1:
                    if r.get("thumbnail_url"):
                        st.markdown(
                            f'<img src="{r["thumbnail_url"]}" style="width:100%;border-radius:12px;'
                            f'max-height:180px;object-fit:cover" onerror="this.style.display=\'none\'">',
                            unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background:#F2C4B0;border-radius:12px;height:140px;"
                                    "display:flex;align-items:center;justify-content:center;font-size:3em'>🎂</div>",
                                    unsafe_allow_html=True)
                with hc2:
                    st.markdown(f"### {r['name']}")
                    if r.get("description"):
                        st.markdown(f"<small style='color:#555'>{r['description'][:220]}</small>",
                                    unsafe_allow_html=True)
                    # Meta row
                    meta = []
                    if r.get("prep_time"): meta.append(f"⏱ Prep: {r['prep_time'].replace('PT','').replace('M',' min').replace('H',' hr')}")
                    if r.get("cook_time"): meta.append(f"🔥 Cook: {r['cook_time'].replace('PT','').replace('M',' min').replace('H',' hr')}")
                    if r.get("servings"):  meta.append(f"👥 Serves: {r['servings']}")
                    if meta: st.markdown("  ·  ".join(meta))
                    st.markdown(f"[📖 View on {r['site_name']}]({r['source_url']})")
                    mc1, mc2 = st.columns(2)
                    ingr_count  = len([l for l in r['ingredients'].split('\n') if l.strip()])
                    steps_count = len([l for l in r['steps'].split('\n') if l.strip()])
                    mc1.metric("Ingredients", ingr_count)
                    mc2.metric("Steps", steps_count)

                st.markdown("---")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**🧂 Ingredients**")
                    for line in r['ingredients'].split('\n'):
                        if line.strip():
                            st.markdown(f"• {line.strip()}")
                with c2:
                    st.markdown("**📋 Steps**")
                    for line in r['steps'].split('\n'):
                        if line.strip():
                            st.markdown(f"<p style='color:#2C1A0E;margin:4px 0'>{line.strip()}</p>",
                                        unsafe_allow_html=True)

                st.markdown("---")
                bc1, bc2, bc3 = st.columns(3)
                with bc1:
                    if st.button("💾 Save to Library", key=f"save_f_{i}"):
                        guessed_cat, guessed_sub = auto_categorise(
                            r['name'], r.get('description',''), r['ingredients'])
                        save_recipe({
                            "name": r['name'],
                            "category": guessed_cat, "subcategory": guessed_sub,
                            "description": r.get("description",""),
                            "ingredients": r['ingredients'], "steps": r['steps'],
                            "sweetness":5,"tartness":3,"richness":5,
                            "bitterness":2,"nuttiness":2,"floral":1,
                            "source_url": r['source_url'],
                            "video_url":"","instagram_url":"",
                            "region":"","difficulty":"Medium",
                            "tags": term, "notes":"",
                            "thumbnail_url": r.get("thumbnail_url","")
                        })
                        st.success("✅ Saved to your Recipe Library!")

                with bc2:
                    in_compare = compare_data.get(i, False)
                    label = "✅ In Comparator" if in_compare else "⚖️ Add to Compare"
                    if st.button(label, key=f"cmp_f_{i}"):
                        compare_data[i] = not in_compare
                        st.session_state["finder_compare"] = compare_data
                        st.rerun()

                with bc3:
                    dl_text = (f"Recipe: {r['name']}\nSource: {r['source_url']}\n\n"
                               f"INGREDIENTS:\n{r['ingredients']}\n\nSTEPS:\n{r['steps']}")
                    st.download_button("📥 Download .txt", data=dl_text,
                                       file_name=f"{r['name'].replace(' ','_')}.txt",
                                       mime="text/plain", key=f"dl_f_{i}")

        # ── Side-by-side comparator ──────────────────────────────────────────
        compare_data   = st.session_state.get("finder_compare", {})
        selected_idxs  = [i for i, v in compare_data.items() if v]

        if len(selected_idxs) >= 2:
            st.markdown("---")
            st.markdown("### ⚖️ Side-by-Side Comparison")
            sel = [recipes[i] for i in selected_idxs if i < len(recipes)]

            # Thumbnails + stats header
            hcols = st.columns(len(sel))
            for j, r in enumerate(sel):
                with hcols[j]:
                    if r.get("thumbnail_url"):
                        st.markdown(f'<img src="{r["thumbnail_url"]}" style="width:100%;border-radius:8px;height:110px;object-fit:cover">',
                                    unsafe_allow_html=True)
                    st.markdown(f"**{r['site_name']}**")
                    ingr_c  = len([l for l in r['ingredients'].split('\n') if l.strip()])
                    steps_c = len([l for l in r['steps'].split('\n') if l.strip()])
                    st.metric("Ingredients", ingr_c)
                    st.metric("Steps", steps_c)
                    st.markdown(f"[📖 Source]({r['source_url']})")

            # Ingredients side by side
            st.markdown("**🧂 Ingredients:**")
            icols = st.columns(len(sel))
            for j, r in enumerate(sel):
                with icols[j]:
                    st.markdown(f"**{r['site_name']}**")
                    for line in r['ingredients'].split('\n'):
                        if line.strip():
                            st.markdown(f"<small>• {line.strip()}</small>", unsafe_allow_html=True)

            # Steps side by side
            st.markdown("**📋 Steps:**")
            scols = st.columns(len(sel))
            for j, r in enumerate(sel):
                with scols[j]:
                    st.markdown(f"**{r['site_name']}**")
                    for line in r['steps'].split('\n'):
                        if line.strip():
                            st.markdown(f"<small style='color:#2C1A0E'>{line.strip()}</small>",
                                        unsafe_allow_html=True)

            # Verdict
            st.markdown("---")
            st.markdown("### 🏆 Quick Verdict")
            simplest    = min(sel, key=lambda r: len([l for l in r['ingredients'].split('\n') if l.strip()]))
            most_detail = max(sel, key=lambda r: len([l for l in r['steps'].split('\n') if l.strip()]))
            quickest    = min(sel, key=lambda r: len([l for l in r['steps'].split('\n') if l.strip()]))
            st.success(f"🥇 **Fewest ingredients** (easiest to shop for): **{simplest['site_name']}**")
            st.info(f"📋 **Most detailed instructions**: **{most_detail['site_name']}**")
            st.info(f"⚡ **Fewest steps** (quickest method): **{quickest['site_name']}**")

        elif len(selected_idxs) == 1:
            st.info("⚖️ Select at least one more recipe tab and click **'Add to Compare'** to compare recipes side by side.")



# ─── Practice Schedule ────────────────────────────────────────────────────────
def page_schedule():
    st.markdown("<div class='section-header'>📅 Baking Practice Schedule</div>", unsafe_allow_html=True)
    st.markdown("Build your personal weekly baking practice plan. Work through skills systematically!")

    SKILL_CURRICULUM = {
        "🟢 Beginner": [
            ("Week 1",  "Basic Sponge Cake",        "Master a simple Victoria sponge — mixing, baking, testing doneness.",
             ["https://www.youtube.com/results?search_query=victoria+sponge+beginner+tutorial"]),
            ("Week 2",  "American Buttercream",      "Learn to make a stable buttercream and apply a crumb coat.",
             ["https://www.youtube.com/results?search_query=american+buttercream+tutorial+beginner"]),
            ("Week 3",  "Simple Cookies",            "Shortbread or sugar cookies — practice consistency in rolling and baking.",
             ["https://www.youtube.com/results?search_query=shortbread+cookies+beginner"]),
            ("Week 4",  "Pound Cake / Loaf Cake",    "Learn the creaming method — butter + sugar technique.",
             ["https://www.youtube.com/results?search_query=pound+cake+tutorial"]),
            ("Week 5",  "Simple Tart Shell",         "Pâte sablée — blind baking and preventing shrinkage.",
             ["https://www.youtube.com/results?search_query=tart+shell+pate+sablee+tutorial"]),
            ("Week 6",  "Whipped Cream & Filling",   "Stabilized whipped cream, diplomat cream, filling between layers.",
             ["https://www.youtube.com/results?search_query=how+to+fill+cake+layers"]),
        ],
        "🟡 Intermediate": [
            ("Week 7",  "Swiss Meringue Buttercream","Cook egg whites + sugar, whip to glossy SMBC — the gold standard.",
             ["https://www.youtube.com/results?search_query=swiss+meringue+buttercream+tutorial"]),
            ("Week 8",  "Chiffon / Genoise Sponge",  "Air-based cakes — folding technique, preventing deflation.",
             ["https://www.youtube.com/results?search_query=genoise+sponge+tutorial"]),
            ("Week 9",  "Ganache & Chocolate Work",  "Perfect ganache ratios, chocolate drip, tempering basics.",
             ["https://www.youtube.com/results?search_query=chocolate+ganache+drip+cake+tutorial"]),
            ("Week 10", "Pastry Cream",               "Crème pâtissière — cooking to right consistency, no lumps.",
             ["https://www.youtube.com/results?search_query=pastry+cream+creme+patissiere+tutorial"]),
            ("Week 11", "Smooth Cake Finish",         "Sharp edges, smooth sides, ombré — bench scraper technique.",
             ["https://www.youtube.com/results?search_query=smooth+buttercream+cake+sharp+edges+tutorial"]),
            ("Week 12", "Macarons",                   "French macaronage — folding, piping, feet formation, filling.",
             ["https://www.youtube.com/results?search_query=french+macaron+tutorial+beginner"]),
        ],
        "🔴 Advanced": [
            ("Week 13", "Italian Meringue Buttercream","Hot sugar syrup + meringue — silkiest buttercream.",
             ["https://www.youtube.com/results?search_query=italian+meringue+buttercream+tutorial"]),
            ("Week 14", "Croissants",                 "Lamination — butter block, folding, proofing, the honeycomb interior.",
             ["https://www.youtube.com/results?search_query=croissant+from+scratch+tutorial"]),
            ("Week 15", "Mirror Glaze Entremet",      "Mousse cake construction, insert layers, mirror glaze at 35°C.",
             ["https://www.youtube.com/results?search_query=mirror+glaze+entremet+tutorial"]),
            ("Week 16", "Sugar & Isomalt Work",       "Caramel cages, spun sugar, isomalt shards and decorations.",
             ["https://www.youtube.com/results?search_query=sugar+decoration+caramel+cage+tutorial"]),
            ("Week 17", "Buttercream Flowers",        "Korean-style piping — rose, chrysanthemum, ranunculus.",
             ["https://www.youtube.com/results?search_query=korean+buttercream+flowers+tutorial"]),
            ("Week 18", "Chocolate Showpiece",        "Tempering, moulding, transfer sheets, chocolate decorations.",
             ["https://www.youtube.com/results?search_query=chocolate+showpiece+decoration+tutorial"]),
        ],
    }

    # My schedule tracker in session state
    if "my_schedule" not in st.session_state:
        st.session_state["my_schedule"] = {}

    tab1, tab2, tab3 = st.tabs(["📋 Full Curriculum", "✅ My Progress", "➕ Custom Skill"])

    with tab1:
        for level, weeks in SKILL_CURRICULUM.items():
            st.markdown(f"### {level}")
            for week, skill, desc, links in weeks:
                done_key = f"done_{week}_{skill}"
                is_done = st.session_state["my_schedule"].get(done_key, False)
                c1, c2 = st.columns([5, 1])
                with c1:
                    status = "✅" if is_done else "⬜"
                    st.markdown(f"""
                    <div class='recipe-card' style='{"opacity:0.6" if is_done else ""}'>
                        <b>{status} {week}: {skill}</b><br>
                        <small style='color:#666'>{desc}</small><br>
                        <a href='{links[0]}' target='_blank' style='color:#C87941;font-size:0.85em'>▶️ Watch tutorial →</a>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("✅ Done" if not is_done else "↩️ Redo",
                                  key=f"btn_{week}_{skill}"):
                        st.session_state["my_schedule"][done_key] = not is_done
                        st.rerun()

    with tab2:
        done_count = sum(1 for v in st.session_state["my_schedule"].values() if v)
        total = sum(len(w) for w in SKILL_CURRICULUM.values())
        st.markdown(f"### 🏆 Progress: {done_count}/{total} skills completed")
        st.progress(done_count / total)

        if done_count > 0:
            st.markdown("**Completed skills:**")
            for level, weeks in SKILL_CURRICULUM.items():
                for week, skill, desc, _ in weeks:
                    done_key = f"done_{week}_{skill}"
                    if st.session_state["my_schedule"].get(done_key):
                        st.markdown(f"✅ {week}: **{skill}**")
        if done_count < total:
            # Find next skill
            for level, weeks in SKILL_CURRICULUM.items():
                for week, skill, desc, links in weeks:
                    done_key = f"done_{week}_{skill}"
                    if not st.session_state["my_schedule"].get(done_key):
                        st.markdown("---")
                        st.markdown(f"### 👉 Up Next: {week} — {skill}")
                        st.markdown(f"_{desc}_")
                        st.markdown(f"[▶️ Watch tutorial]({links[0]})")
                        break
                else:
                    continue
                break

    with tab3:
        st.markdown("### ➕ Add a Custom Practice Week")
        with st.form("custom_skill_form"):
            cs_week = st.text_input("Week label", placeholder="e.g. Week 19")
            cs_skill = st.text_input("Skill name", placeholder="e.g. Opera Cake")
            cs_desc  = st.text_area("Description", placeholder="What will you practice?")
            cs_link  = st.text_input("Tutorial link (YouTube or website)")
            if st.form_submit_button("➕ Add to My Schedule"):
                if cs_week and cs_skill:
                    key = f"custom_{cs_week}_{cs_skill}"
                    st.session_state["my_schedule"][f"desc_{key}"] = cs_desc
                    st.session_state["my_schedule"][f"link_{key}"] = cs_link
                    st.session_state["my_schedule"][f"added_{key}"] = True
                    st.success(f"Added '{cs_skill}' to your schedule!")

        # Show custom skills
        custom_skills = [(k,v) for k,v in st.session_state["my_schedule"].items() if k.startswith("added_")]
        if custom_skills:
            st.markdown("**Your custom skills:**")
            for key, _ in custom_skills:
                base = key.replace("added_", "")
                skill_name = base.split("_", 2)[-1] if "_" in base else base
                desc  = st.session_state["my_schedule"].get(f"desc_{base}", "")
                link  = st.session_state["my_schedule"].get(f"link_{base}", "")
                done  = st.session_state["my_schedule"].get(f"done_{base}", False)
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"{'✅' if done else '⬜'} **{skill_name}** — {desc}")
                    if link: st.markdown(f"[▶️ Tutorial]({link})")
                with c2:
                    if st.button("✅/↩️", key=f"custbtn_{base}"):
                        st.session_state["my_schedule"][f"done_{base}"] = not done
                        st.rerun()


# ─── Main App ────────────────────────────────────────────────────────────────────
init_db()

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0'>
        <div style='font-size:3em'>🎂</div>
        <div style='font-family:Georgia; font-size:1.3em; font-weight:bold'>Baking Studio</div>
        <div style='font-size:0.85em; opacity:0.7'>Your sweet compendium</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    pages = [
        "🏠 Home",
        "📚 Recipe Library",
        "🔍 Recipe Finder & Compare",
        "✏️ Add Recipe",
        "🔗 Import from URL",
        "🎨 Flavor Explorer",
        "📅 Practice Schedule",
        "🎬 Techniques & Videos",
        "👩‍🍳 Chef Inspirations",
        "🌍 World Dessert Index",
        "📖 Full Baking Index",
    ]

    # Support programmatic navigation from home page category buttons
    default_idx = 0
    if "nav_page" in st.session_state:
        nav = st.session_state.pop("nav_page")
        if nav in pages:
            default_idx = pages.index(nav)

    page = st.radio("Navigate", pages, index=default_idx)

    st.markdown("---")
    st.markdown("<small style='opacity:0.6'>Made with ❤️ for a passionate baker</small>", unsafe_allow_html=True)

if page == "🏠 Home":
    page_home()
elif page == "📚 Recipe Library":
    page_browse()
elif page == "🔍 Recipe Finder & Compare":
    page_recipe_finder()
elif page == "✏️ Add Recipe":
    page_add_recipe()
elif page == "🔗 Import from URL":
    page_import_url()
elif page == "🎨 Flavor Explorer":
    page_flavor_explorer()
elif page == "📅 Practice Schedule":
    page_schedule()
elif page == "🎬 Techniques & Videos":
    page_techniques()
elif page == "👩‍🍳 Chef Inspirations":
    page_chefs()
elif page == "🌍 World Dessert Index":
    page_global_index()
elif page == "📖 Full Baking Index":
    page_full_index()
