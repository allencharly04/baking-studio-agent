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
        created_at TEXT
    )""")
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
         region, difficulty, tags, notes, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (data['name'], data['category'], data['subcategory'], data['description'],
         data['ingredients'], data['steps'],
         data['sweetness'], data['tartness'], data['richness'], data['bitterness'],
         data['nuttiness'], data['floral'],
         data['source_url'], data['video_url'], data['instagram_url'],
         data['region'], data['difficulty'], data['tags'], data['notes'],
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

                    if name or ingredients:
                        return {"name": name, "ingredients": ingredients, "steps": steps, "description": desc, "success": True}
            except Exception:
                continue

        # Priority 2: Heuristic fallback
        title = soup.find("h1")
        name = title.get_text(strip=True) if title else ""

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
            "success": bool(name or ingredients)
        }

    except Exception as e:
        return {"name": "", "ingredients": "", "steps": "", "description": "", "success": False, "error": str(e)}

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
    # Use column names (works regardless of column order in old DBs)
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

    with st.expander(f"**{name}** — _{subcat}_  |  ⚙️ {difficulty}", expanded=False):
        col1, col2 = st.columns([3, 2])
        with col1:
            if desc:
                st.markdown(f"_{desc}_")
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

        with col2:
            st.markdown("**Flavor Profile**")
            render_flavor_bars(row)
            st.write("")
            links = []
            if source_url: links.append(f"[📖 Recipe Source]({source_url})")
            if video_url:  links.append(f"[▶️ Video Tutorial]({video_url})")
            if insta_url:  links.append(f"[📸 Instagram]({insta_url})")
            if links:
                st.markdown("  |  ".join(links))

        if show_delete:
            if st.button(f"🗑️ Delete", key=f"del_{rec_id}"):
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
                    "region": "", "difficulty": difficulty, "tags": tags, "notes": ""
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
        "✏️ Add Recipe",
        "🔗 Import from URL",
        "🎨 Flavor Explorer",
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
elif page == "✏️ Add Recipe":
    page_add_recipe()
elif page == "🔗 Import from URL":
    page_import_url()
elif page == "🎨 Flavor Explorer":
    page_flavor_explorer()
elif page == "🎬 Techniques & Videos":
    page_techniques()
elif page == "👩‍🍳 Chef Inspirations":
    page_chefs()
elif page == "🌍 World Dessert Index":
    page_global_index()
elif page == "📖 Full Baking Index":
    page_full_index()
