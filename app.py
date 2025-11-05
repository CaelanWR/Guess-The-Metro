import base64
import html
import math
import random
from textwrap import wrap
from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html as components_html

# ========== METRO CONFIGURATION ==========
METROS = {
    'Memphis': {
        'name': 'Memphis, TN',
        'state': 'Tennessee',
        'highlights': [
            "FedEx keeps Memphis the global air cargo capital with the world's busiest cargo airport.",
            "Healthcare anchors like St. Jude and Methodist Le Bonheur fuel a fast-growing biosciences corridor.",
            "Advanced manufacturers and logistics firms lean on the Mississippi River port and rail crossroads for scale.",
            "Cultural energy plus low costs continue to attract professional services and tech expansions."
        ]
    },
    'Charlotte': {
        'name': 'Charlotte, NC',
        'state': 'North Carolina',
        'highlights': [
            "Bank of America and Wells Fargo anchor Charlotte as the nation's second-largest banking center after New York.",
            "The metro's finance sector employs over 60,000 workers with competitive salaries and rapid growth.",
            "Charlotte Douglas International Airport is a major American Airlines hub, driving logistics employment.",
            "Healthcare systems like Atrium Health are expanding rapidly, creating thousands of high-skill jobs."
        ]
    },
    'DC': {
        'name': 'Washington DC',
        'state': 'District of Columbia',
        'highlights': [
            "Federal government agencies dominate employment with over 350,000 workers in the metro area.",
            "The highest average salaries in the dataset reflect government and contractor pay premiums.",
            "Professional services firms like Booz Allen Hamilton cluster around federal contracts.",
            "Technology sector growing rapidly as defense and intelligence agencies modernize systems."
        ]
    },
    'Pittsburgh': {
        'name': 'Pittsburgh, PA',
        'state': 'Pennsylvania',
        'highlights': [
            "UPMC (University of Pittsburgh Medical Center) is the region's largest employer with over 40,000 workers.",
            "Carnegie Mellon and University of Pittsburgh anchor a growing tech and robotics ecosystem.",
            "Healthcare and education sectors dominate, creating stable, high-skill employment.",
            "Former steel town successfully transitioned to 'eds and meds' economy with tech growth."
        ]
    },
    'Houston': {
        'name': 'Houston, TX',
        'state': 'Texas',
        'highlights': [
            "ExxonMobil, Shell, and dozens of energy companies make Houston the global energy capital.",
            "The energy sector provides high-paying jobs with strong five-year growth projections.",
            "MD Anderson Cancer Center and Texas Medical Center create a healthcare employment powerhouse.",
            "Port of Houston ranks first in U.S. foreign tonnage, driving massive logistics employment."
        ]
    }
}

# List of all metro names for dropdown (will exclude answer)
# 150+ US metropolitan areas with state abbreviations
ALL_METRO_NAMES = [
    'Akron, OH', 'Albany, NY', 'Albuquerque, NM', 'Allentown, PA', 'Amarillo, TX',
    'Anchorage, AK', 'Ann Arbor, MI', 'Asheville, NC', 'Atlanta, GA', 'Augusta, GA',
    'Austin, TX', 'Bakersfield, CA', 'Baltimore, MD', 'Baton Rouge, LA', 'Beaumont, TX',
    'Boise, ID', 'Boston, MA', 'Boulder, CO', 'Bridgeport, CT', 'Brownsville, TX',
    'Buffalo, NY', 'Cape Coral, FL', 'Cedar Rapids, IA', 'Charleston, SC', 'Charlotte, NC',
    'Chattanooga, TN', 'Chicago, IL', 'Cincinnati, OH', 'Clarksville, TN', 'Cleveland, OH',
    'Colorado Springs, CO', 'Columbia, SC', 'Columbus, GA', 'Columbus, OH', 'Corpus Christi, TX',
    'Dallas, TX', 'Dayton, OH', 'Daytona Beach, FL', 'Deltona, FL', 'Denver, CO',
    'Des Moines, IA', 'Detroit, MI', 'Durham, NC', 'El Paso, TX', 'Eugene, OR',
    'Evansville, IN', 'Fargo, ND', 'Fayetteville, AR', 'Fayetteville, NC', 'Flint, MI',
    'Fort Collins, CO', 'Fort Myers, FL', 'Fort Wayne, IN', 'Fort Worth, TX', 'Fresno, CA',
    'Gainesville, FL', 'Grand Rapids, MI', 'Green Bay, WI', 'Greensboro, NC', 'Greenville, SC',
    'Harrisburg, PA', 'Hartford, CT', 'Honolulu, HI', 'Houston, TX', 'Huntsville, AL',
    'Indianapolis, IN', 'Jackson, MS', 'Jacksonville, FL', 'Jersey City, NJ', 'Kalamazoo, MI',
    'Kansas City, MO', 'Killeen, TX', 'Knoxville, TN', 'Lafayette, LA', 'Lakeland, FL',
    'Lancaster, PA', 'Lansing, MI', 'Laredo, TX', 'Las Vegas, NV', 'Lexington, KY',
    'Lincoln, NE', 'Little Rock, AR', 'Los Angeles, CA', 'Louisville, KY', 'Lubbock, TX',
    'Madison, WI', 'Manchester, NH', 'McAllen, TX', 'Memphis, TN', 'Miami, FL',
    'Milwaukee, WI', 'Minneapolis, MN', 'Mobile, AL', 'Modesto, CA', 'Montgomery, AL',
    'Myrtle Beach, SC', 'Nashville, TN', 'New Haven, CT', 'New Orleans, LA', 'New York, NY',
    'Newark, NJ', 'Norfolk, VA', 'North Port, FL', 'Ogden, UT', 'Oklahoma City, OK',
    'Omaha, NE', 'Orlando, FL', 'Oxnard, CA', 'Palm Bay, FL', 'Pensacola, FL',
    'Peoria, IL', 'Philadelphia, PA', 'Phoenix, AZ', 'Pittsburgh, PA', 'Portland, ME',
    'Portland, OR', 'Providence, RI', 'Provo, UT', 'Raleigh, NC', 'Reading, PA',
    'Reno, NV', 'Richmond, VA', 'Riverside, CA', 'Rochester, NY', 'Rockford, IL',
    'Sacramento, CA', 'Salem, OR', 'Salinas, CA', 'Salt Lake City, UT', 'San Antonio, TX',
    'San Diego, CA', 'San Francisco, CA', 'San Jose, CA', 'Santa Barbara, CA', 'Santa Rosa, CA',
    'Savannah, GA', 'Scranton, PA', 'Seattle, WA', 'Shreveport, LA', 'Spokane, WA',
    'Springfield, IL', 'Springfield, MA', 'Springfield, MO', 'St Louis, MO', 'Stamford, CT',
    'Stockton, CA', 'Syracuse, NY', 'Tacoma, WA', 'Tallahassee, FL', 'Tampa, FL',
    'Toledo, OH', 'Topeka, KS', 'Trenton, NJ', 'Tucson, AZ', 'Tulsa, OK',
    'Tuscaloosa, AL', 'Tyler, TX', 'Utica, NY', 'Vallejo, CA', 'Virginia Beach, VA',
    'Visalia, CA', 'Waco, TX', 'Washington DC', 'Wichita, KS', 'Wilmington, NC',
    'Winston-Salem, NC', 'Worcester, MA', 'York, PA', 'Youngstown, OH'
]

# ========== DEVELOPER CONFIGURATION ==========
UI_SCALE = 1.0
CHART_HEIGHT_SCALE = 0.88
CHART_TEXT_SCALE = 0.90

CHART_CONFIG = {
    'treemap': {
        'scale': 1.1, 
        'text': 1.0,
        'margin': {'t': 20, 'l': 18, 'r': 18, 'b': 22}
    },
    'salary': {
        'scale': 0.9,
        'text': 1.0,
        'margin': {'t': 20, 'l': 18, 'r': 80, 'b': 24}
    },
    'growth_bar': {
        'scale': 0.9,
        'text': 1.0,
        'margin': {'t': 20, 'l': 18, 'r': 14, 'b': 24}
    },
    'growth_line': {
        'scale': 0.9,
        'text': 1.0,
        'margin': {'t': 20, 'l': 18, 'r': 14, 'b': 24}
    },
    'percentiles': {
        'scale': 0.9,
        'text': 0.80,
        'margin': {'t': 50, 'l': 14, 'r': 14, 'b': 20}
    },
    'score_distribution': {
        'scale': 1.3,
        'text': 1.4,
        'margin': {'t': 50, 'l': 40, 'r': 30, 'b': 40}
    },
    'employers': {
        'scale': 1.2,
        'text': 1.5,
        'margin': {'t': 70, 'l': 16, 'r': 100, 'b': 36}
    },
    'hud_score': {
        'height': 40,
        'margin': {'t': 2, 'b': 2, 'l': 4, 'r': 4},
        'text': 1.6
    }
}

HINTS = [None] * 5

SCORE_DISTRIBUTION_PROFILES = {
    'Memphis': {'mean': 33, 'std': 7},
    'Charlotte': {'mean': 41, 'std': 6},
    'DC': {'mean': 39, 'std': 5},
    'Pittsburgh': {'mean': 31, 'std': 8},
    'Houston': {'mean': 44, 'std': 5}
}

DEFAULT_SCORE_PROFILE = {'mean': 36, 'std': 7}

# ========== COLOR PALETTES ==========
REVELIO_PALETTE = {
    "primary": "#0066FF",
    "secondary": "#00CC88",
    "accent": "#FF6B6B",
    "purple": "#8B5CF6",
    "gray": "#64748B",
    "light_gray": "#94A3B8",
    "grid": "#E2E8F0",
    "text": "#1E293B",
    "background": "#FFFFFF",
    "subtle_bg": "#F8FAFC",
}

SECTOR_COLORS = {
    'Logistics & Transportation': '#4A90E2',
    'Healthcare': '#50C878',
    'Manufacturing': '#9B7EDE',
    'Retail & Hospitality': '#FF9F6B',
    'Professional Services': '#5BC0BE',
    'Technology': '#A78BFA',
    'Education': '#FB7185',
    'Financial Services': '#60A5FA',
    'Construction': '#FCD34D',
    'Government': '#94A3B8',
    'Energy & Utilities': '#F59E0B',
    'Real Estate': '#10B981',
    'Media & Entertainment': '#EC4899',
    'Non-Profit': '#6366F1'
}

BASE_DIR = Path(globals().get("__file__", Path.cwd())).resolve().parent
INTRO_LOGO_PATH = BASE_DIR / "city-data-chart.png"


@st.cache_data(show_spinner=False)
def get_intro_logo_base64() -> str:
    """Return base64 string for the header logo, if available."""
    try:
        logo_bytes = INTRO_LOGO_PATH.read_bytes()
    except FileNotFoundError:
        return ""
    except OSError:
        return ""
    return base64.b64encode(logo_bytes).decode("utf-8")

def build_city_fact_list_html(metro_key: str) -> str:
    """Return HTML bullet list of metro labor market highlights"""
    highlights = METROS[metro_key]['highlights']
    return "".join(f"<li>{html.escape(item)}</li>" for item in highlights)

def get_percentile_suffix(value: int) -> str:
    """Return ordinal suffix with Percentile label for gauge numbers."""
    if 10 <= value % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')
    return f"{suffix} Percentile"


def show_celebration_animation() -> None:
    """Render a celebratory confetti animation in a standalone component."""
    animation_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <style>
            :root {
                color-scheme: light;
            }
            body {
                margin: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: transparent;
            }
            .stage {
                position: relative;
                width: 100%;
                height: 100%;
                border-radius: 18px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                gap: 14px;
                background: radial-gradient(circle at center, rgba(0, 204, 136, 0.18), rgba(0, 102, 255, 0.08));
                box-shadow: 0 18px 44px rgba(15, 23, 42, 0.18);
            }
            .stage::after {
                content: '';
                position: absolute;
                inset: -45%;
                background: conic-gradient(from 0deg, rgba(0, 102, 255, 0.35), rgba(139, 92, 246, 0.22), rgba(255, 107, 107, 0.35), rgba(0, 204, 136, 0.35), rgba(0, 102, 255, 0.35));
                animation: swirl 9s linear infinite;
                opacity: 0.35;
                z-index: 0;
            }
            .title {
                font-size: 2rem;
                font-weight: 800;
                color: #0F172A;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                text-align: center;
                z-index: 1;
            }
            .subtitle {
                font-size: 1.05rem;
                font-weight: 600;
                color: #1E293B;
                text-align: center;
                z-index: 1;
            }
            .burst {
                position: absolute;
                width: 140px;
                height: 140px;
                border-radius: 50%;
                border: 4px solid rgba(255, 255, 255, 0.9);
                z-index: 0;
                animation: ping 1.8s ease-out infinite;
            }
            .burst.delay {
                animation-delay: 0.6s;
            }
            .confetti {
                position: absolute;
                top: -12%;
                width: 12px;
                height: 18px;
                border-radius: 4px;
                opacity: 0;
                animation: fall 2.8s linear infinite;
            }
            @keyframes fall {
                0% {
                    transform: translate3d(0, -160px, 0) scale(var(--scale, 1)) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                60% {
                    opacity: 1;
                }
                100% {
                    transform: translate3d(0, 360px, 0) scale(var(--scale, 1)) rotate(var(--rotation, 720deg));
                    opacity: 0;
                }
            }
            @keyframes ping {
                0% {
                    transform: scale(0.5);
                    opacity: 0.8;
                }
                60% {
                    transform: scale(1.4);
                    opacity: 0.1;
                }
                100% {
                    transform: scale(1.6);
                    opacity: 0;
                }
            }
            @keyframes swirl {
                to {
                    transform: rotate(360deg);
                }
            }
        </style>
    </head>
    <body>
        <div class="stage">
            <div class="burst"></div>
            <div class="burst delay"></div>
            <div class="title">Metro Master!</div>
            <div class="subtitle">You nailed today's mystery city.</div>
        </div>
        <script>
            const stage = document.querySelector('.stage');
            const colors = ['#FF6B6B', '#FAD232', '#00CC88', '#8B5CF6', '#60A5FA', '#FF9F6B'];
            for (let i = 0; i < 180; i++) {
                const piece = document.createElement('span');
                piece.className = 'confetti';
                piece.style.setProperty('--scale', (0.7 + Math.random() * 0.9).toFixed(2));
                piece.style.setProperty('--rotation', (360 + Math.random() * 720).toFixed(2) + 'deg');
                piece.style.left = (Math.random() * 100).toFixed(2) + '%';
                piece.style.animationDelay = (Math.random() * 1.2).toFixed(2) + 's';
                piece.style.background = colors[i % colors.length];
                stage.appendChild(piece);
            }
            setTimeout(() => {
                document.body.style.transition = 'opacity 0.7s ease';
                document.body.style.opacity = '0';
            }, 3200);
        </script>
    </body>
    </html>
    """
    components_html(animation_html, height=260, width=None)

# ========== CSS INJECTION ==========
def inject_css():
    """Injects CSS with utility classes and existing styles"""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {{
            font-size: {UI_SCALE * 100:.0f}%;
        }}

        html, body {{
            background-color: {REVELIO_PALETTE["subtle_bg"]};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }}

        section.main > div:first-child {{
            padding-top: 1.5rem;
        }}

        .block-container {{
            padding: 0.7rem 0.85rem 0.6rem;
            max-width: 960px;
        }}

        .maxw,
        .maxw-tight {{
            max-width: 880px;
            margin-left: auto;
            margin-right: auto;
        }}

        h1 {{
            color: {REVELIO_PALETTE["text"]};
            font-weight: 700;
            font-size: 1.35rem;
            letter-spacing: -0.02em;
            margin: 0 0 0.3rem;
        }}

        h2,
        h3,
        h4 {{
            color: {REVELIO_PALETTE["text"]};
            font-weight: 600;
            margin: 0.2rem 0;
        }}

        h2 {{ font-size: 0.95rem; }}
        h3 {{ font-size: 0.9rem; }}
        h4 {{ font-size: 0.88rem; }}

        p {{
            margin: 0.08rem 0;
            line-height: 1.35;
            font-size: 0.9rem;
        }}

        .stCaption {{
            color: {REVELIO_PALETTE["light_gray"]} !important;
            font-size: 0.78rem !important;
            margin-top: 0.05rem !important;
        }}

        .card {{
            background: white;
            padding: 0.55rem 0.75rem;
            border-radius: 12px;
            border: 1px solid {REVELIO_PALETTE["grid"]};
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        }}

        .card.control-card {{
            padding: 0.7rem 0.85rem;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }}

        .card.control-card [data-testid="column"] {{
            padding: 0 !important;
        }}

        .card.control-card div[data-testid="stHorizontalBlock"] {{
            gap: 0.48rem;
        }}

        .card.control-card [data-testid="stSelectbox"] label {{
            display: none;
        }}

        .card.control-card [data-testid="column"] + [data-testid="column"] {{
            margin-left: 0.45rem;
        }}

        .card.control-card [data-testid="stSelectbox"] > div:first-child {{
            margin-bottom: 0;
        }}

        .card.control-card .stSelectbox div[data-baseweb="select"] {{
            border-radius: 999px;
        }}

        .card.control-card .stButton {{
            margin-top: 0 !important;
        }}

        .card.control-card .stButton button {{
            width: 100%;
        }}

        .page-header {{
            margin: 0 auto 0.5rem;
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 0.6rem;
        }}

        .page-header__logo {{
            width: 52px;
            height: auto;
        }}

        .stack-tight {{
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
        }}

        .layout-split {{
            display: flex;
            gap: 0.8rem;
            align-items: flex-start;
        }}

        .hud {{
            display: grid;
            grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.6fr);
            gap: 12px;
            align-items: center;
            width: 100%;
            padding: 10px 14px;
            background: white;
            border: 1px solid {REVELIO_PALETTE["grid"]};
            border-radius: 14px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
            margin: 0 auto 0.5rem;
        }}

        .hud-block {{
            display: flex;
            flex-direction: column;
            gap: 0.22rem;
        }}

        .hud-label {{
            font-size: 11px;
            font-weight: 600;
            color: {REVELIO_PALETTE["gray"]};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 0;
        }}

        .badge {{
            border: 1px solid {REVELIO_PALETTE["primary"]};
            padding: 0.45rem 1.1rem;
            border-radius: 999px;
            background: {REVELIO_PALETTE["primary"]};
            font-weight: 600;
            font-size: 0.9rem;
            color: white;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.35rem;
            box-shadow: 0 8px 20px rgba(0, 102, 255, 0.22);
        }}

        .guess-slot-list {{
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
            margin-bottom: 0.65rem;
        }}

        .guess-slot {{
            padding: 0.55rem 0.75rem;
            border-radius: 10px;
            border: 1px solid {REVELIO_PALETTE["grid"]};
            background: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 44px;
            gap: 0.75rem;
        }}

        .guess-slot-filled {{
            color: {REVELIO_PALETTE["text"]};
            font-weight: 600;
        }}

        .guess-slot-empty {{
            border-style: dashed;
            background: rgba(226, 232, 240, 0.4);
            color: {REVELIO_PALETTE["light_gray"]};
            font-weight: 500;
        }}

        .guess-slot-wrong {{
            border-color: {REVELIO_PALETTE["accent"]};
            background: rgba(255, 107, 107, 0.12);
            color: {REVELIO_PALETTE["accent"]};
        }}
        
        @keyframes guessShake {{
            0%, 100% {{
                transform: translateX(0);
            }}
            20%, 60% {{
                transform: translateX(-6px);
            }}
            40%, 80% {{
                transform: translateX(6px);
            }}
        }}

        .guess-slot-shake {{
            animation: guessShake 0.45s ease;
        }}

        .guess-slot-correct {{
            border-color: {REVELIO_PALETTE["secondary"]};
            background: rgba(0, 204, 136, 0.14);
            color: {REVELIO_PALETTE["secondary"]};
        }}

        .guess-slot-index {{
            font-size: 0.78rem;
            font-weight: 600;
            color: {REVELIO_PALETTE["gray"]};
            letter-spacing: 0.05em;
        }}

        .guess-slot-value {{
            font-size: 0.92rem;
            font-weight: 600;
        }}

        .loss-banner,
        .win-banner {{
            display: none;
        }}

        .loss-subtext {{
            font-size: 0.95rem;
            color: {REVELIO_PALETTE["gray"]};
            margin-top: 0.6rem;
            text-align: center;
        }}

        .result-card {{
            text-align: center;
            background: white;
            border-radius: 16px;
            border: 1px solid {REVELIO_PALETTE["grid"]};
            box-shadow: 0 16px 38px rgba(15, 23, 42, 0.12);
            padding: 1.4rem 1.8rem 1.5rem;
        }}

        .result-card h3 {{
            margin: 0;
            font-size: 1.6rem;
            font-weight: 700;
            color: {REVELIO_PALETTE["text"]};
        }}

        .result-card p {{
            margin: 0.6rem 0 0.8rem;
            font-size: 1.03rem;
            line-height: 1.5;
        }}

        .result-card ul {{
            margin: 0.4rem auto 0;
            padding-left: 1.2rem;
            max-width: 520px;
            text-align: left;
        }}

        .result-card li {{
            margin-bottom: 0.35rem;
            font-size: 0.98rem;
        }}

        [data-testid="stHorizontalBlock"] {{
            gap: 0.6rem;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 3px;
            background: white;
            padding: 3px;
            border-radius: 10px;
            border: 1px solid {REVELIO_PALETTE["grid"]};
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
            margin: 0;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 10px 12px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            font-weight: 700;
        }}

        .stTabs {{
            margin: 0 !important;
            padding: 0 !important;
        }}

        [data-testid="stPlotlyChart"] {{
            background: transparent;
            padding: 0;
            margin: 0;
            max-width: 920px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: visible !important;
        }}

        [data-testid="stPlotlyChart"] > div {{
            width: 100% !important;
            margin: 0 auto;
            overflow: visible !important;
        }}

        .stButton button {{
            border-radius: 999px;
            font-weight: 500;
            padding: 0.48rem 1rem;
            border: 1px solid {REVELIO_PALETTE["grid"]};
            transition: all 0.18s ease;
        }}

        .stButton button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.1);
        }}

        .stButton button:focus {{
            outline: 2px solid {REVELIO_PALETTE["primary"]};
            outline-offset: 2px;
        }}

        .stButton button[kind="primary"] {{
            background-color: {REVELIO_PALETTE["primary"]};
            color: white;
            border-color: {REVELIO_PALETTE["primary"]};
        }}

        .stButton button[kind="secondary"] {{
            background-color: transparent;
            color: {REVELIO_PALETTE["gray"]};
            border-color: {REVELIO_PALETTE["grid"]};
        }}

        .guess-history {{
            background: white;
            padding: 0.75rem 0.95rem;
            border-radius: 10px;
            border: 1px solid {REVELIO_PALETTE["grid"]};
            margin: 0.7rem 0;
            box-shadow: 0 12px 26px rgba(15, 23, 42, 0.05);
        }}

        .guess-item,
        .guess-remaining {{
            display: inline-flex;
            padding: 6px 14px;
            border-radius: 999px;
            font-weight: 500;
            font-size: 0.8rem;
            margin: 4px 8px 4px 0;
        }}

        .guess-item {{
            background: {REVELIO_PALETTE["accent"]};
            color: white;
        }}

        .guess-remaining {{
            background: {REVELIO_PALETTE["grid"]};
            color: {REVELIO_PALETTE["light_gray"]};
        }}

        .stAlert {{
            padding: 0.7rem 0.9rem;
            font-size: 0.93rem;
            border-radius: 9px;
            margin: 0.45rem 0;
        }}

        hr {{
            margin: 0.18rem 0 0.4rem;
            border: none;
            border-top: 1px solid {REVELIO_PALETTE["grid"]};
        }}

        .stSelectbox {{
            margin-bottom: 0;
        }}

        .anim-x {{
            position: fixed;
            top: 14%;
            left: 50%;
            transform: translate(-50%, 0);
            font-size: 4.4rem;
            color: {REVELIO_PALETTE["accent"]};
            font-weight: 700;
            text-shadow: 0 12px 28px rgba(255, 107, 107, 0.45);
            z-index: 9999;
            animation: rise-x 1.05s ease-out forwards;
            pointer-events: none;
        }}

        @keyframes rise-x {{
            0% {{ opacity: 0; transform: translate(-50%, 18px) scale(0.92); }}
            35% {{ opacity: 1; transform: translate(-50%, -6px) scale(1.03); }}
            100% {{ opacity: 0; transform: translate(-50%, -44px) scale(0.96); }}
        }}

        .guess-toast {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.92);
            background: rgba(255, 255, 255, 0.98);
            color: {REVELIO_PALETTE["accent"]};
            padding: 1.2rem 2rem;
            border-radius: 18px;
            border: 2px solid rgba(255, 107, 107, 0.35);
            box-shadow: 0 32px 60px rgba(15, 23, 42, 0.25);
            font-weight: 700;
            font-size: 1.35rem;
            text-align: center;
            z-index: 9998;
            min-width: min(90vw, 420px);
            animation: toastFade 3.2s ease forwards;
        }}

        .guess-toast span {{
            display: block;
            margin-top: 0.4rem;
            font-size: 1rem;
            font-weight: 500;
            color: {REVELIO_PALETTE["gray"]};
        }}

        @keyframes toastFade {{
            0% {{ opacity: 0; transform: translate(-50%, -40%) scale(0.88); }}
            18% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.0); }}
            82% {{ opacity: 1; transform: translate(-50%, -52%) scale(1.0); }}
            100% {{ opacity: 0; transform: translate(-50%, -64%) scale(0.96); }}
        }}

        *:focus-visible {{
            outline: 2px solid {REVELIO_PALETTE["primary"]};
            outline-offset: 2px;
        }}

        [data-testid="stDialog"] {{
            background: rgba(15, 23, 42, 0.35);
        }}

        [data-testid="stDialog"] > div {{
            background: white;
            border-radius: 16px;
            padding: 0;
            max-width: 820px;
            width: min(88vw, 820px);
            box-shadow: 0 22px 48px rgba(15, 23, 42, 0.14);
        }}

        .intro-modal {{
            padding: 1.8rem 2.2rem 1.6rem;
            background: white;
            border-radius: 16px;
            text-align: center;
        }}

        .intro-modal h3 {{
            font-size: 1.8rem;
            margin-bottom: 1rem;
            color: {REVELIO_PALETTE["text"]};
        }}

        .intro-modal p {{
            font-size: 1.05rem;
            line-height: 1.55;
            margin-bottom: 0.65rem;
        }}

        .intro-modal ul {{
            margin: 0.4rem auto 0.6rem;
            padding: 0;
            max-width: 520px;
            text-align: left;
        }}

        .intro-modal li {{
            font-size: 1.02rem;
            margin-bottom: 0.35rem;
        }}

        .city-modal {{
            padding: 1.6rem 2rem 1.4rem;
            background: white;
            border-radius: 16px;
            text-align: center;
        }}

        .city-modal h3 {{
            font-size: 1.6rem;
            margin-bottom: 0.75rem;
            color: {REVELIO_PALETTE["text"]};
        }}

        .city-modal p {{
            margin-bottom: 0.6rem;
            font-size: 1.05rem;
            line-height: 1.58;
        }}

        .city-modal ul {{
            margin: 0.4rem auto 0.4rem;
            padding: 0;
            max-width: 520px;
            text-align: left;
        }}

        .city-modal li {{
            font-size: 1rem;
            margin-bottom: 0.35rem;
        }}

        @media (max-width: 900px) {{
            .hud {{
                grid-template-columns: 1fr;
                gap: 10px;
            }}
            .layout-split {{
                flex-direction: column;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)

# ========== PLOTLY TEMPLATE ==========
def register_plotly_template():
    """Register custom Plotly template 'revelio_min'"""
    revelio_template = go.layout.Template()
    
    revelio_template.layout = go.Layout(
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            size=15,
            color=REVELIO_PALETTE["text"]
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            showgrid=True,
            gridcolor=REVELIO_PALETTE["grid"],
            gridwidth=1,
            zeroline=False,
            showline=False,
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=REVELIO_PALETTE["grid"],
            gridwidth=1,
            zeroline=False,
            showline=False,
            tickfont=dict(size=14)
        ),
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.05,
            yanchor="bottom",
            bgcolor="rgba(255, 255, 255, 0)",
            font=dict(size=14)
        ),
        colorway=[
            REVELIO_PALETTE["primary"],
            REVELIO_PALETTE["secondary"],
            REVELIO_PALETTE["purple"],
            REVELIO_PALETTE["gray"]
        ]
    )
    
    # Register template
    import plotly.io as pio
    pio.templates["revelio_min"] = revelio_template
    pio.templates.default = "revelio_min"

# ========== INTRO MODAL ==========
@st.dialog("How to Play", width="large")
def show_intro_modal():
    """Display game rules in a modal dialog"""
    st.markdown("""
    <div class="intro-modal">
        <h3>Welcome to Guess the Metro! </h3>
        <p><strong>Your mission:</strong> Identify the mystery US metropolitan area using workforce data clues.</p>
        <p><strong>How it works:</strong></p>
        <ul>
            <li>You start with <strong>50 points</strong> and <strong>5 guesses</strong>.</li>
            <li>The first hint (Industry Breakdown) is free.</li>
            <li>Every incorrect guess reveals the next hint and costs <strong>10 points</strong>.</li>
            <li>Make the correct call before you run out of guesses (or points!).</li>
        </ul>
        <p><strong>Strategy tip:</strong> Study each hint carefully before guessing. The fewer guesses you need, the higher your score!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Got it — Let's Play!", type="primary", use_container_width=True):
        st.session_state["hide_intro"] = True
        st.rerun()

def reset_intro():
    """Reset the intro modal flag"""
    if "hide_intro" in st.session_state:
        del st.session_state["hide_intro"]
    st.session_state.win_animation_pending = False


def mock_score_distribution(metro_key: str, sample_size: int = 480) -> list[int]:
    """Return a deterministic set of mock scores for a metro."""
    profile = SCORE_DISTRIBUTION_PROFILES.get(metro_key, DEFAULT_SCORE_PROFILE)
    rng = random.Random(f"{metro_key}-scores")
    mean = profile.get('mean', DEFAULT_SCORE_PROFILE['mean'])
    std = max(profile.get('std', DEFAULT_SCORE_PROFILE['std']), 1)
    bins = list(range(0, 51, 10))

    weights = []
    for score in bins:
        z = (score - mean) / std
        weight = math.exp(-0.5 * z * z) + 0.25  # add baseline so tails stay represented
        weights.append(weight)

    draws_needed = max(sample_size - len(bins), 0)
    sampled = rng.choices(bins, weights=weights, k=draws_needed)

    # Ensure every score bucket is represented at least once
    sampled.extend(bins)
    rng.shuffle(sampled)
    return sampled


def render_score_distribution(metro_key: str, player_score: int) -> None:
    """Show histogram of mock player scores with player's score highlighted."""
    scores = mock_score_distribution(metro_key)
    if not scores:
        return
    player_score = max(0, min(50, int(round(player_score / 10) * 10)))

    counts = Counter(scores)
    total_samples = sum(counts.values())
    if total_samples == 0:
        return

    average_score = sum(score * count for score, count in counts.items()) / total_samples
    less_than = sum(count for score, count in counts.items() if score < player_score)
    equal_to = counts.get(player_score, 0)
    percent_outscored = less_than / total_samples * 100
    percent_tied = equal_to / total_samples * 100
    percent_outscored = max(0.0, min(100.0, percent_outscored))

    # Create histogram data with bin counts
    bin_edges = list(range(-5, 56, 10))
    bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)]

    # Count scores in each bin
    bin_counts = []
    for i in range(len(bin_edges)-1):
        count = sum(1 for s in scores if bin_edges[i] <= s < bin_edges[i+1])
        bin_counts.append(count)

    # Convert to percentages
    bin_percentages = [count / total_samples * 100 for count in bin_counts]

    # Determine which bin contains the player's score
    player_bin_idx = None
    for i in range(len(bin_edges)-1):
        if bin_edges[i] <= player_score < bin_edges[i+1]:
            player_bin_idx = i
            break

    # Create colors list - accent color for player's bin, purple for others
    bar_colors = []
    bar_names = []
    for i in range(len(bin_centers)):
        if i == player_bin_idx:
            bar_colors.append(REVELIO_PALETTE["accent"])
            bar_names.append('Your score')
        else:
            bar_colors.append(REVELIO_PALETTE["purple"])
            bar_names.append('Other players')

    fig = go.Figure()

    # Add bars one by one so we can control colors
    for i, (center, percentage, color, name) in enumerate(zip(bin_centers, bin_percentages, bar_colors, bar_names)):
        is_player_bin = (i == player_bin_idx)
        fig.add_trace(go.Bar(
            x=[center],
            y=[percentage],
            width=9,  # Slightly less than 10 to create small gaps
            marker=dict(
                color=color,
                line=dict(width=2 if is_player_bin else 0, color='white' if is_player_bin else color)
            ),
            opacity=1.0 if is_player_bin else 0.85,
            name=name,
            legendgroup=name,
            showlegend=(i == player_bin_idx or (i == 0 and player_bin_idx is None) or (i == 1 and player_bin_idx == 0)),
            hovertemplate=f'Score: {int(bin_edges[i])}-{int(bin_edges[i+1]-1)}<br>Share: {percentage:.1f}%<extra></extra>'
        ))

    fig.update_layout(
        height=get_chart_height('score_distribution', 450),
        margin=get_margin('score_distribution', {'t': 50, 'l': 40, 'r': 30, 'b': 40}),
        paper_bgcolor='white',
        plot_bgcolor='white',
        bargap=0.08,
        barmode='group',
        showlegend=True,
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.12,
            yanchor="bottom",
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor=REVELIO_PALETTE["grid"],
            borderwidth=1,
            font=dict(size=get_text_size('score_distribution', 16), weight=600)
        ),
        xaxis=dict(
            title='Player Score (out of 50)',
            title_font=dict(size=get_text_size('score_distribution', 18), weight=600),
            tickfont=dict(size=get_text_size('score_distribution', 16)),
            tickmode='array',
            tickvals=list(range(0, 51, 10)),
            range=[-2, 52]
        ),
        yaxis=dict(
            title='Share of Players',
            title_font=dict(size=get_text_size('score_distribution', 18), weight=600),
            tickfont=dict(size=get_text_size('score_distribution', 16)),
            ticksuffix='%'
        )
    )

    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True  # Disable zoom/pan interactions
    })

    percentile_text = f"{percent_outscored:.1f}%"
    tie_text = ""
    if percent_tied > 0:
        tie_text = f" Another <strong style='color: {REVELIO_PALETTE['primary']}; font-size: 1.2rem;'>{percent_tied:.1f}%</strong> matched your score."

    # Make the summary text larger and more prominent
    st.markdown(
        f"<div style='font-size: 1.15rem; line-height: 1.6; margin-top: 1rem; padding: 0.8rem 1rem; "
        f"background: {REVELIO_PALETTE['subtle_bg']}; border-radius: 8px; border-left: 4px solid {REVELIO_PALETTE['accent']};'>"
        f"You outscored <strong style='color: {REVELIO_PALETTE['accent']}; font-size: 1.25rem;'>{percentile_text}</strong> "
        f"of today's players for <strong>{METROS[metro_key]['name']}</strong>.{tie_text}"
        f"</div>",
        unsafe_allow_html=True
    )
    st.caption("Score distribution is simulated placeholder data for the prototype.")

def render_result_card(won: bool, metro_key: str) -> None:
    """Render centered summary of game outcome with metro facts"""
    guesses = st.session_state.get("guesses_made", 0)
    score = st.session_state.get("score", 0)
    metro_info = METROS[metro_key]
    metro_name = metro_info['name']  # Already includes state abbreviation
    
    headline = f"Game Over — The city was {metro_name}"
    if won:
        summary = f"You cracked the case in {guesses} guesses and banked {score}/50 points."
    else:
        summary = f"{metro_name} kept its secret after {guesses} guesses. Final score: {score}/50."
    
    fact_list = build_city_fact_list_html(metro_key)
    st.markdown(
        f"""
        <div class="result-card">
            <h3>{headline}</h3>
            <p>{html.escape(summary)}</p>
            <p>Labor market highlights:</p>
            <ul>{fact_list}</ul>
        </div>
        """,
        unsafe_allow_html=True
    )

@st.dialog("Metro Snapshot", width="large")
def show_result_modal(metro_key: str):
    """Display metro highlights after the round ends"""
    won = st.session_state.get("game_won", False)
    score = st.session_state.get("score", 0)
    metro_info = METROS[metro_key]
    metro_name = metro_info['name']  # Already includes state abbreviation
    
    highlight_items = build_city_fact_list_html(metro_key)
    status_line = "You cracked the mystery metro!" if won else f"{metro_name} slipped away this time."
    
    st.markdown(
        f"""
        <div class="city-modal">
            <h3>Game Over — The city was {metro_name}</h3>
            <p>{html.escape(status_line)} The metro area was <strong>{html.escape(metro_name)}</strong>.</p>
            <p><strong>Final score:</strong> {score}/50.</p>
            <p>Labor market highlights:</p>
            <ul>{highlight_items}</ul>
            <p>Ready for another challenge? Head back to the game board.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### How other players scored today")
    render_score_distribution(metro_key, score)

    if st.button("Back to game", type="primary", use_container_width=True):
        st.session_state.show_result_modal = False
        st.rerun()

# ========== CHART SIZING HELPERS ==========
def get_chart_height(chart_type, base_height):
    """Scale chart height based on individual chart configuration"""
    scale = CHART_CONFIG.get(chart_type, {}).get('scale', 1.0)
    return int(base_height * scale * CHART_HEIGHT_SCALE)

def get_text_size(chart_type, base_size):
    """Scale text size based on individual chart configuration"""
    scale = CHART_CONFIG.get(chart_type, {}).get('text', 1.0)
    return int(base_size * scale * CHART_TEXT_SCALE)

def get_margin(chart_type, defaults=None):
    """Get margin configuration for a chart type"""
    margin = CHART_CONFIG.get(chart_type, {}).get('margin', defaults or {})
    return margin if margin else defaults

def score_bar(score: int, max_score: int) -> go.Figure:
    """Render a compact stacked score bar showing achieved vs remaining points"""
    max_score = max(max_score, 1)
    clamped_score = max(0, min(score, max_score))
    remainder = max(max_score - clamped_score, 0)
    cfg = CHART_CONFIG.get('hud_score', {})
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[clamped_score],
        y=['score'],
        orientation='h',
        marker=dict(color=REVELIO_PALETTE["secondary"]),
        hovertemplate='Score: %{x:,.0f}<extra></extra>',
        showlegend=False
    ))
    
    fig.add_trace(go.Bar(
        x=[remainder],
        y=['score'],
        orientation='h',
        marker=dict(color=REVELIO_PALETTE["grid"]),
        hovertemplate='Remaining: %{x:,.0f}<extra></extra>',
        showlegend=False
    ))
    
    fig.update_traces(marker_line=dict(width=0))
    fig.update_layout(
        barmode='stack',
        height=cfg.get('height', 44),
        margin=cfg.get('margin', {'t': 6, 'b': 6, 'l': 6, 'r': 6}),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(range=[0, max_score], visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True)
    )
    
    label_size = max(11, int(round(13 * cfg.get('text', 1))))
    fig.add_annotation(
        x=0,
        y='score',
        xanchor='left',
        yanchor='middle',
        text=f"Score: {clamped_score:,}",
        font=dict(size=label_size, color=REVELIO_PALETTE["text"], family='Inter'),
        showarrow=False
    )
    
    return fig

def render_hud(score: int, max_score: int, guesses: list[str], max_guesses: int,
               total_hints: int, revealed_hints: int) -> None:
    """Render the compact top-of-page HUD"""
    with st.container():
        st.markdown('<div class="hud maxw-tight">', unsafe_allow_html=True)
        col_score, col_hints = st.columns([1.4, 0.6])

        with col_score:
            with st.container():
                st.markdown('<div class="hud-block">', unsafe_allow_html=True)
                st.markdown('<div class="hud-label">Score</div>', unsafe_allow_html=True)
                st.plotly_chart(
                    score_bar(score, max_score),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )
                st.markdown('</div>', unsafe_allow_html=True)

        with col_hints:
            with st.container():
                st.markdown('<div class="hud-block">', unsafe_allow_html=True)
                st.markdown('<div class="hud-label">Hints</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="badge">Hints: {revealed_hints}/{total_hints}</div>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Guess the Metro",
    layout="wide",
    page_icon="city-data-chart.png"
)

# Initialize CSS and Plotly template
inject_css()
register_plotly_template()

# ========== DATA LOADING ==========
@st.cache_data
def load_metro_data(metro_key: str):
    """Load data for a specific metro"""
    metro_folder = metro_key.lower().replace(' ', '_')
    
    industry = pd.read_csv(f'game_data/{metro_folder}/industry.csv')
    salary = pd.read_csv(f'game_data/{metro_folder}/salary.csv')
    noncollege = pd.read_csv(f'game_data/{metro_folder}/noncollege_employers.csv')
    college = pd.read_csv(f'game_data/{metro_folder}/college_employers.csv')
    time_series = pd.read_csv(f'game_data/{metro_folder}/time_series.csv')
    education = pd.read_csv(f'game_data/{metro_folder}/education.csv')
    growth = pd.read_csv(f'game_data/{metro_folder}/growth.csv')
    
    # Create percentiles data (mock for now - you could add this to your data generation)
    percentiles = pd.DataFrame({
        'metric': ['Total Employment', 'Average Salary', 'Average Tenure', 'Healthcare Jobs', 'Tech Jobs'],
        'percentile': [45, 38, 52, 78, 65]  # These would vary by metro in real data
    })
    
    # Convert time_series to growth format for backward compatibility
    growth_from_ts = time_series[['year', 'total_employees', 'new_hires', 'departures', 'net_growth']].copy()
    growth_from_ts['growth_rate'] = growth_from_ts['net_growth'] / growth_from_ts['total_employees'] * 100
    
    return industry, salary, noncollege, college, growth_from_ts, percentiles

# ========== SESSION STATE INIT ==========
if 'revealed_hints' not in st.session_state:
    # Select random metro
    st.session_state.mystery_metro = random.choice(list(METROS.keys()))
    st.session_state.revealed_hints = [0]
    st.session_state.guesses_made = 0
    st.session_state.score = 50
    st.session_state.game_over = False
    st.session_state.last_guess_wrong = False
    st.session_state.guess_history = []
    st.session_state.show_result_modal = False
    st.session_state.game_won = False
    st.session_state.win_animation_pending = False
else:
    st.session_state.setdefault('show_result_modal', False)
    st.session_state.setdefault('game_won', False)
    st.session_state.setdefault('mystery_metro', random.choice(list(METROS.keys())))
    st.session_state.setdefault('win_animation_pending', False)

# Load data for current mystery metro
mystery_metro = st.session_state.mystery_metro
industry, salary, noncollege, college, growth, percentiles = load_metro_data(mystery_metro)

# Show intro modal on first load
if "hide_intro" not in st.session_state:
    show_intro_modal()

header_logo_markup = ""
page_logo_base64 = get_intro_logo_base64()
if page_logo_base64:
    header_logo_markup = (
        f'<img src="data:image/png;base64,{page_logo_base64}" '
        'alt="Guess the Metro logo" class="page-header__logo" />'
    )

st.markdown(
    f'<div class="page-header maxw-tight"><h1>Guess the Metro</h1>{header_logo_markup}</div>',
    unsafe_allow_html=True
)

render_hud(
    score=st.session_state.score,
    max_score=50,
    guesses=st.session_state.guess_history,
    max_guesses=5,
    total_hints=len(HINTS),
    revealed_hints=len(st.session_state.revealed_hints)
)

if st.session_state.get('win_animation_pending'):
    show_celebration_animation()
    st.balloons()
    st.session_state.win_animation_pending = False

if st.session_state.get('show_result_modal'):
    show_result_modal(mystery_metro)

shake_latest_guess = st.session_state.get('last_guess_wrong', False)


# Flash ❌ animation when guess is wrong (no text alerts)
if st.session_state.last_guess_wrong:
    message = st.session_state.get('wrong_guess_message')
    max_guesses = 5
    has_more_guesses = not st.session_state.get('game_over', False) and st.session_state.get('guesses_made', 0) < max_guesses
    has_more_hints = len(st.session_state.revealed_hints) < len(HINTS)
    if isinstance(message, (tuple, list)) and len(message) >= 2:
        title, detail = message[0], message[1]
    else:
        title = str(message) if message else "Incorrect!"
        detail = "Next hint unlocking..." if has_more_guesses and has_more_hints else "No more hints remaining."
    title_html = html.escape(title)
    detail_html = html.escape(detail)
    st.markdown(
        f'<div class="guess-toast">{title_html}<span>{detail_html}</span></div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="anim-x">❌</div>', unsafe_allow_html=True)
    st.session_state.last_guess_wrong = False
    st.session_state.pop('wrong_guess_message', None)

# ========== HINT FUNCTIONS ==========
def show_industry_treemap():
    """Optimized treemap with sector labels on larger boxes and subsectors inside, plus color legend"""
    st.markdown("#### Industry Breakdown")
    st.markdown("_Share of total employment by sector and industry_")

    # Filter out very small sectors (less than 1% of total)
    total_headcount = industry['headcount'].sum()
    industry_filtered = industry[industry['headcount'] >= total_headcount * 0.01].copy()
    industry_filtered['share_of_total'] = industry_filtered['headcount'] / total_headcount
    industry_filtered['subsector_display'] = industry_filtered['subsector']

    # Calculate sector-level shares for determining box sizes
    sector_shares = industry_filtered.groupby('sector')['share_of_total'].sum().to_dict()

    def format_cell_text(row):
        """Format cell text based on size to prevent overlap - subsector only"""
        share = row['share_of_total']

        # Hide text for very small cells
        if share < 0.015:
            return ''

        # Large cells (>8%): Show full detail with wrapping
        if share >= 0.08:
            lines = wrap(row['subsector'], width=20)[:2]
            text = "<br>".join(f"<span style='font-size:88%;'>{line}</span>" for line in lines)
            percent = f"<span style='font-size:110%; font-weight:700;'>{share:.1%}</span>"
            return f"{text}<br>{percent}"

        # Medium-large cells (5-8%): Show abbreviated text
        elif share >= 0.05:
            lines = wrap(row['subsector'], width=18)[:2]
            text = "<br>".join(f"<span style='font-size:84%;'>{line}</span>" for line in lines)
            percent = f"<span style='font-size:105%; font-weight:700;'>{share:.1%}</span>"
            return f"{text}<br>{percent}"

        # Medium cells (3-5%): Show shortened text
        elif share >= 0.03:
            lines = wrap(row['subsector'], width=16)[:1]
            text = f"<span style='font-size:82%;'>{lines[0]}</span>"
            percent = f"<span style='font-size:100%; font-weight:700;'>{share:.1%}</span>"
            return f"{text}<br>{percent}"

        # Small cells (1.5-3%): Percentage only
        else:
            return f"<span style='font-size:85%; font-weight:700;'>{share:.1%}</span>"

    industry_filtered['cell_text'] = industry_filtered.apply(format_cell_text, axis=1)

    # Format sector labels - show sector name on ALL boxes, sized appropriately
    def format_sector_label(sector_name):
        sector_share = sector_shares.get(sector_name, 0)
        # Large sector boxes (>15% of total)
        if sector_share >= 0.15:
            lines = wrap(sector_name, width=20)
            text = "<br>".join(f"<span style='font-size:150%; font-weight:800;'>{line}</span>" for line in lines)
            return text
        # Medium-large boxes (10-15%)
        elif sector_share >= 0.10:
            lines = wrap(sector_name, width=18)
            text = "<br>".join(f"<span style='font-size:130%; font-weight:800;'>{line}</span>" for line in lines)
            return text
        # Medium boxes (5-10%)
        elif sector_share >= 0.05:
            lines = wrap(sector_name, width=15)
            text = "<br>".join(f"<span style='font-size:110%; font-weight:700;'>{line}</span>" for line in lines[:1])
            return text
        # Small boxes (2-5%)
        elif sector_share >= 0.02:
            # Abbreviated name for small boxes
            short_name = sector_name.split(' ')[0] if ' ' in sector_name else sector_name[:12]
            return f"<span style='font-size:95%; font-weight:700;'>{short_name}</span>"
        else:
            # Very small boxes - just show first word or abbreviation
            short_name = sector_name.split(' ')[0][:8]
            return f"<span style='font-size:85%; font-weight:600;'>{short_name}</span>"

    sector_text_lookup = {sector: format_sector_label(sector) for sector in sector_shares.keys()}

    fig = px.treemap(
        industry_filtered,
        path=['sector', 'subsector_display'],
        values='headcount',
        color='sector',
        color_discrete_map=SECTOR_COLORS,
        hover_data={'headcount': ':,.0f', 'share_of_total': ':.1%'},
        custom_data=[
            industry_filtered['subsector'],
            industry_filtered['sector'],
            industry_filtered['share_of_total'],
            industry_filtered['cell_text']
        ]
    )

    trace = fig.data[0]
    text_values = []
    for label, parent, custom in zip(trace.labels, trace.parents, trace.customdata):
        if parent == '':
            # This is a sector (parent box) - show sector label
            text_values.append(sector_text_lookup.get(label, ''))
        else:
            # This is a subsector (child box) - show subsector label
            cell_text = custom[3] if len(custom) > 3 else ''
            text_values.append(cell_text)

    trace.text = text_values
    trace.texttemplate = '%{text}'
    trace.textposition = 'middle center'

    fig.update_traces(
        textinfo="text",
        textfont=dict(
            size=get_text_size('treemap', 14),
            color='white',
            family='Inter',
            weight=600
        ),
        marker=dict(
            line=dict(width=1.5, color='white'),
            pad=dict(t=8, l=5, r=5, b=8)
        ),
        hovertemplate=(
            '<b>%{label}</b><br>'
            'Employees: %{value:,.0f}<br>'
            'Share of total: %{percentRoot:.1%}<extra></extra>'
        ),
    )

    fig.update_layout(
        height=get_chart_height('treemap', 600),
        margin=get_margin('treemap', {'t': 26, 'l': 22, 'r': 22, 'b': 28}),
        uniformtext=dict(
            minsize=8,
            mode='hide'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': False,  # Keep interactivity for treemap drill-down
        'doubleClick': 'reset'  # Double-click to reset zoom
    })

    # Add helpful navigation hint
    st.caption("💡 Click a sector to zoom in. Double-click anywhere or click the top bar to zoom back out.")

    # Add color legend below the treemap
    st.markdown("**Sector Colors:**")

    # Get unique sectors present in the filtered data
    present_sectors = sorted(industry_filtered['sector'].unique())

    # Create legend HTML with color boxes
    legend_items = []
    for sector in present_sectors:
        color = SECTOR_COLORS.get(sector, REVELIO_PALETTE['gray'])
        legend_items.append(
            f'<span style="display:inline-flex; align-items:center; margin-right:16px; margin-bottom:8px;">'
            f'<span style="display:inline-block; width:16px; height:16px; background-color:{color}; '
            f'border-radius:3px; margin-right:6px; border:1px solid white;"></span>'
            f'<span style="font-size:0.85rem; color:{REVELIO_PALETTE["text"]};">{sector}</span>'
            f'</span>'
        )

    legend_html = f'<div style="display:flex; flex-wrap:wrap; margin-top:8px;">{"".join(legend_items)}</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

def show_salary_range_spread():
    st.markdown("#### Salary Range by Industry")
    
    # Get top 8 sectors by average salary
    salary_sorted = salary.sort_values('avg_salary', ascending=False).head(8)
    
    fig = go.Figure()
    
    colors = [SECTOR_COLORS.get(sec, REVELIO_PALETTE['gray']) for sec in salary_sorted['sector']]
    
    # Add the salary ranges as error bars with dots at the average
    for idx, row in salary_sorted.iterrows():
        sector = row['sector']
        avg = row['avg_salary']
        min_sal = row['min_salary']
        max_sal = row['max_salary']
        color = SECTOR_COLORS.get(sector, REVELIO_PALETTE['gray'])
        
        # Add range line
        fig.add_trace(go.Scatter(
            x=[min_sal, max_sal],
            y=[sector, sector],
            mode='lines',
            line=dict(color=color, width=3),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add min marker
        fig.add_trace(go.Scatter(
            x=[min_sal],
            y=[sector],
            mode='markers',
            marker=dict(size=8, color=color, symbol='line-ns', line=dict(width=2, color='white')),
            showlegend=False,
            hovertemplate=f'<b>{sector}</b><br>Min: ${min_sal:,.0f}<extra></extra>'
        ))
        
        # Add max marker
        fig.add_trace(go.Scatter(
            x=[max_sal],
            y=[sector],
            mode='markers',
            marker=dict(size=8, color=color, symbol='line-ns', line=dict(width=2, color='white')),
            showlegend=False,
            hovertemplate=f'<b>{sector}</b><br>Max: ${max_sal:,.0f}<extra></extra>'
        ))
        
        # Add average marker (larger dot)
        fig.add_trace(go.Scatter(
            x=[avg],
            y=[sector],
            mode='markers+text',
            marker=dict(size=12, color=color, line=dict(width=2, color='white')),
            text=f'${avg/1000:.0f}k',
            textposition='top center',
            textfont=dict(size=get_text_size('salary', 13), color=REVELIO_PALETTE['text'], family='Inter', weight=600),
            showlegend=False,
            hovertemplate=f'<b>{sector}</b><br>Average: ${avg:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        height=get_chart_height('salary', 400),
        showlegend=False,
        xaxis_title='Salary Range',
        yaxis_title='',
        margin=get_margin('salary', {'t': 26, 'l': 18, 'r': 92, 'b': 30}),
        yaxis=dict(
            tickfont=dict(size=get_text_size('salary', 14), weight=500),
            categoryorder='total ascending'
        ),
        xaxis=dict(
            title_font=dict(size=get_text_size('salary', 14)),
            tickfont=dict(size=get_text_size('salary', 13)),
            tickformat='$,.0f'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True  # Disable zoom/pan interactions
    })

def show_growth_area():
    st.markdown("#### Employment Growth")
    
    fig = go.Figure()
    colors = [REVELIO_PALETTE['secondary'] if g > 0 else REVELIO_PALETTE['accent'] for g in growth['net_growth']]
    bar_text = [f'{x/1000:+.0f}k' for x in growth['net_growth']]
    
    fig.add_trace(go.Bar(
        x=growth['year'],
        y=growth['net_growth'],
        marker=dict(color=colors, line=dict(color='white', width=0)),
        text=bar_text,
        textposition='outside',
        cliponaxis=False,
        textfont=dict(
            size=get_text_size('growth_bar', 14),
            color=REVELIO_PALETTE['text'],
            family='Inter',
            weight=600
        ),
        hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=get_chart_height('growth_bar', 320),
        showlegend=False,
        margin=get_margin('growth_bar', {'t': 26, 'l': 22, 'r': 16, 'b': 30}),
        xaxis=dict(
            title='Year',
            title_font=dict(size=get_text_size('growth_bar', 14)),
            tickfont=dict(size=get_text_size('growth_bar', 14))
        ),
        yaxis=dict(
            title='Net Growth',
            title_font=dict(size=get_text_size('growth_bar', 14)),
            tickfont=dict(size=get_text_size('growth_bar', 14))
        ),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True  # Disable zoom/pan interactions
    })

def show_metro_comparison():
    st.markdown("#### Percentile Rank vs Other U.S. Metros")
    
    # Metro-specific percentiles (made up but plausible)
    metro_percentiles = {
        'Memphis': {
            '5-Year Employment Growth': 55,
            'Number of Workers': 45,
            'Average Salary': 38,
            'Salary Growth': 42
        },
        'Charlotte': {
            '5-Year Employment Growth': 78,
            'Number of Workers': 62,
            'Average Salary': 71,
            'Salary Growth': 68
        },
        'DC': {
            '5-Year Employment Growth': 35,
            'Number of Workers': 88,
            'Average Salary': 94,
            'Salary Growth': 52
        },
        'Pittsburgh': {
            '5-Year Employment Growth': 48,
            'Number of Workers': 38,
            'Average Salary': 55,
            'Salary Growth': 45
        },
        'Houston': {
            '5-Year Employment Growth': 72,
            'Number of Workers': 81,
            'Average Salary': 76,
            'Salary Growth': 58
        }
    }
    
    # Get percentiles for current mystery metro
    metro_key = st.session_state.mystery_metro
    percentile_data = metro_percentiles[metro_key]
    
    # Create 4 gauge charts
    metrics = list(percentile_data.keys())
    cols = st.columns(2)
    
    for idx, metric in enumerate(metrics):
        col = cols[idx % 2]
        percentile = percentile_data[metric]
        
        with col:
            # Color coding: green if high, blue if medium, purple if low
            if percentile >= 65:
                gauge_color = REVELIO_PALETTE['secondary']  # Green
            elif percentile >= 45:
                gauge_color = REVELIO_PALETTE['primary']     # Blue
            else:
                gauge_color = REVELIO_PALETTE['purple']       # Purple
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=percentile,
                title={
                    'text': f"<b>{metric}</b>",
                    'font': {'size': get_text_size('percentiles', 20), 'color': REVELIO_PALETTE['text'], 'family': 'Inter'}
                },
                gauge={
                    'axis': {
                        'range': [0, 100],
                        'tickwidth': 1,
                        'tickcolor': REVELIO_PALETTE['light_gray'],
                        'tickfont': {'size': get_text_size('percentiles', 11)}
                    },
                    'bar': {'color': gauge_color, 'thickness': 0.75},
                    'bgcolor': "white",
                    'borderwidth': 1,
                    'bordercolor': REVELIO_PALETTE['grid'],
                    'steps': [
                        {'range': [0, 50], 'color': '#F8FAFC'},
                        {'range': [50, 100], 'color': '#E2E8F0'}
                    ],
                    'threshold': {
                        'line': {'color': REVELIO_PALETTE['light_gray'], 'width': 2},
                        'thickness': 0.75,
                        'value': 50
                    }
                },
                number={
                    'suffix': get_percentile_suffix(percentile),
                    'font': {'size': get_text_size('percentiles', 32), 'color': REVELIO_PALETTE['text'], 'family': 'Inter', 'weight': 700}
                }
            ))
            
            fig.update_layout(
                height=get_chart_height('percentiles', 240),
                margin=get_margin('percentiles', {'l': 16, 'r': 16, 't': 50, 'b': 20}),
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True  # Disable zoom/pan interactions
    })


def show_top_employers_bars():
    st.markdown("### Top Three Employers by Education Level")
    
    # Combine both datasets with labels
    noncollege_top = noncollege.sort_values('headcount', ascending=False).head(3).copy()
    college_top = college.sort_values('headcount', ascending=False).head(3).copy()
    
    noncollege_top['category'] = 'Non-College Grads'
    college_top['category'] = 'College Grads'
    
    # Combine and sort by headcount
    combined = pd.concat([noncollege_top, college_top]).sort_values('headcount', ascending=True)
    
    # Create color map
    colors = [REVELIO_PALETTE['purple'] if cat == 'Non-College Grads' else REVELIO_PALETTE['secondary'] 
              for cat in combined['category']]
    
    # Create single bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=combined['company'],
        x=combined['headcount'],
        orientation='h',
        marker=dict(color=colors, line=dict(color='white', width=0)),
        text=[f'{x//1000}k' if x >= 1000 else str(x) for x in combined['headcount']],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(size=get_text_size('employers', 13), color=REVELIO_PALETTE['text'], family='Inter', weight=600),
        hovertemplate='<b>%{y}</b><br>%{customdata}<br>Employees: %{x:,.0f}<extra></extra>',
        customdata=combined['category'],
        showlegend=False
    ))
    
    # Add manual legend using annotations
    fig.add_annotation(
        x=0.02, y=1.1,
        xref='paper', yref='paper',
        text=f'<span style="font-size:18px;font-weight:600;color:{REVELIO_PALETTE["purple"]};">● Non-College Grads</span>'
             f'&nbsp;&nbsp;&nbsp;'
             f'<span style="font-size:18px;font-weight:600;color:{REVELIO_PALETTE["secondary"]};">● College Grads</span>',
        showarrow=False,
        xanchor='left',
        font=dict(size=18, family='Inter')
    )
    
    fig.update_layout(
        height=get_chart_height('employers', 420),
        showlegend=False,
        xaxis_title='Employee Count',
        yaxis_title='',
        margin=get_margin('employers', {'t': 70, 'l': 18, 'r': 100, 'b': 36}),
        yaxis=dict(tickfont=dict(size=get_text_size('employers', 12), weight=500)),
        xaxis=dict(
            title_font=dict(size=get_text_size('employers', 13)),
            tickfont=dict(size=get_text_size('employers', 12))
        ),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'staticPlot': True  # Disable zoom/pan interactions
    })

# ========== HINTS SETUP ==========
HINTS[:] = [
    {'name': 'Industry Breakdown', 'function': show_industry_treemap, 'penalty': 0, 'icon': ''},
    {'name': 'Salary Ranges', 'function': show_salary_range_spread, 'penalty': 200, 'icon': '', 'priority': 2},
    {'name': 'Employment Growth', 'function': show_growth_area, 'penalty': 200, 'icon': '', 'priority': 1},
    {'name': 'Metro Comparison', 'function': show_metro_comparison, 'penalty': 150, 'icon': ''},
    {'name': 'Top Employers', 'function': show_top_employers_bars, 'penalty': 150, 'icon': ''},
]

# ========== DISPLAY HINTS ==========
st.markdown('<div class="maxw-tight layout-split">', unsafe_allow_html=True)
col_hints, col_controls = st.columns([2.2, 1])

with col_hints:
    if len(st.session_state.revealed_hints) > 0:
        with st.spinner("Loading hint..." if st.session_state.get('last_guess_wrong', False) else ""):
            reversed_hints = list(reversed(st.session_state.revealed_hints))
            
            # Show the newest (most recently revealed) hint by default
            st.markdown("#### 🔍 Latest Hint")
            HINTS[reversed_hints[0]]['function']()
            
            # If there are older hints, show them in an expander
            if len(reversed_hints) > 1:
                with st.expander(f"📋 View Previous Hints ({len(reversed_hints) - 1})"):
                    for hint_idx in reversed_hints[1:]:
                        st.markdown(f"**Hint {hint_idx + 1}: {HINTS[hint_idx]['name']}**")
                        HINTS[hint_idx]['function']()
                        if hint_idx != reversed_hints[-1]:
                            st.markdown("---")

with col_controls:
    if not st.session_state.game_over:
        st.markdown('<div class="card control-card">', unsafe_allow_html=True)
        st.markdown("#### Make Your Guess")

        # Use the full metro list so the correct answer stays selectable
        available_metros = ALL_METRO_NAMES

        max_slots = 5
        guesses = st.session_state.guess_history or []
        st.markdown('<div class="guess-slot-list">', unsafe_allow_html=True)
        
        
        for idx in range(1, max_slots + 1):
            filled = idx <= len(guesses)
            if filled:
                entry = guesses[idx - 1]
                if isinstance(entry, dict):
                    display_value = entry.get('value', '')
                    status = entry.get('status', 'wrong')
                else:
                    display_value = str(entry)
                    status = 'wrong'
                status_class = 'guess-slot-correct' if status == 'correct' else 'guess-slot-wrong'
                slot_class = f"guess-slot {status_class}"
                if shake_latest_guess and idx == len(guesses) and status != 'correct':
                    slot_class += " guess-slot-shake"
            else:
                display_value = f"Guess {idx}"
                slot_class = "guess-slot guess-slot-empty"
            escaped_value = html.escape(display_value)
            slot_markup = (
                f'<div class="{slot_class}">'
                f'<span class="guess-slot-index">{idx}</span>'
                f'<span class="guess-slot-value">{escaped_value}</span>'
                '</div>'
            )
            st.markdown(slot_markup, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Wrap in form to prevent rerun on dropdown change
        # Use a unique key based on game state to force form reset on new game
        form_key = f"guess_form_{st.session_state.guesses_made}"
        
        with st.form(form_key):
            guess = st.selectbox(
                "Select a metropolitan area:",
                options=[''] + available_metros,
                label_visibility="collapsed"
            )

            submit_clicked = st.form_submit_button(
                "Submit Guess",
                type="primary",
                use_container_width=True
            )

        # Only process submission if button was clicked AND a valid guess was made
        # Only process submission if button was clicked AND a valid guess was made
        # Only process submission if button was clicked AND a valid guess was made
        if submit_clicked and guess and guess != '':
            import time
            
            st.session_state.guesses_made += 1
            correct_answer = METROS[mystery_metro]['name']

            if guess == correct_answer:
                st.session_state.guess_history.append({'value': guess, 'status': 'correct'})
                st.session_state.last_guess_wrong = False
                st.session_state.game_over = True
                st.session_state.game_won = True
                st.session_state.show_result_modal = True
                st.session_state.win_animation_pending = True
                st.rerun()
            else:
                st.session_state.guess_history.append({'value': guess, 'status': 'wrong'})
                st.session_state.last_guess_wrong = True
                remaining_guesses = max_slots - st.session_state.guesses_made
                has_more_hints = len(st.session_state.revealed_hints) < len(HINTS)
                if remaining_guesses > 0 and has_more_hints:
                    st.session_state.wrong_guess_message = ("Incorrect!", "Next hint unlocking...")
                else:
                    st.session_state.wrong_guess_message = ("Incorrect!", "No more hints remaining.")
                st.session_state.game_won = False
                st.session_state.score = max(st.session_state.score - 10, 0)

                if st.session_state.guesses_made >= 5:
                    st.session_state.game_over = True
                    st.session_state.game_won = False
                    st.session_state.score = 0
                    st.session_state.show_result_modal = True
                    st.session_state.win_animation_pending = False
                    st.rerun()
                else:
                    # Set flag to show animation first, then reveal hint
                    st.session_state.showing_wrong_animation = True
                    st.rerun()
        elif submit_clicked:
            # User clicked submit without selecting a metro
            st.warning("⚠️ Please select a metropolitan area first!")

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # GAME OVER SECTION - YOU WERE MISSING THIS ENTIRE BLOCK
        st.markdown('<div class="stack-tight">', unsafe_allow_html=True)
        render_result_card(st.session_state.game_won, mystery_metro)

        col_replay, col_reset = st.columns([1.4, 1])

        with col_replay:
            if st.button("Play Again", type="primary", use_container_width=True):
                # Select a new random metro
                st.session_state.mystery_metro = random.choice(list(METROS.keys()))
                st.session_state.revealed_hints = [0]
                st.session_state.guesses_made = 0
                st.session_state.score = 50
                st.session_state.game_over = False
                st.session_state.last_guess_wrong = False
                st.session_state.guess_history = []
                st.session_state.show_result_modal = False
                st.session_state.game_won = False
                st.session_state.win_animation_pending = False
                st.rerun()

        with col_reset:
            if st.button("Reset Intro", use_container_width=True):
                reset_intro()
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle the animation -> new hint flow after the UI has rendered
if st.session_state.get('showing_wrong_animation', False):
    import time

    st.session_state.showing_wrong_animation = False
    time.sleep(1.1)  # Let shake + X animation complete

    if len(st.session_state.revealed_hints) < len(HINTS):
        next_hint_idx = len(st.session_state.revealed_hints)
        st.session_state.revealed_hints.append(next_hint_idx)

    st.rerun()
