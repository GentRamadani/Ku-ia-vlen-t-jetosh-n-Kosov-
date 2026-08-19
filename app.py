import os

import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

from data_loader import load_master_data
from scoring import calculate_living_score

from ai_insights import generate_ai_insight


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Ku ia vlen të jetosh në Kosovë?",
    page_icon="🇽🇰",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 19px;
        color: #777;
        margin-bottom: 25px;
    }

    .best-card {
        padding: 25px;
        border-radius: 18px;
        background-color: rgba(120, 120, 120, 0.08);
        border: 1px solid rgba(120, 120, 120, 0.20);
        margin-bottom: 20px;
    }

    .best-name {
        font-size: 34px;
        font-weight: 800;
    }

    .best-score {
        font-size: 48px;
        font-weight: 900;
    }

    .small-label {
        font-size: 14px;
        color: #888;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA
# ============================================================

CACHE_FILE = "data/master_data_cache.csv"


@st.cache_data(ttl=3600)
def get_data():
    """
    Try to load fresh data from the APIs.

    If ASKdata/Open-Meteo is temporarily unavailable,
    use the last successfully saved local snapshot.
    """

    try:
        # Try live APIs
        df = load_master_data()

        # Save successful result as local fallback
        os.makedirs(
            "data",
            exist_ok=True
        )

        df.to_csv(
            CACHE_FILE,
            index=False
        )

        return df, "live"

    except requests.exceptions.RequestException:

        # API unavailable -> use saved snapshot
        if os.path.exists(CACHE_FILE):

            df = pd.read_csv(
                CACHE_FILE
            )

            return df, "cache"

        # No API and no cache yet
        raise


try:

    master, data_mode = get_data()

except Exception as error:

    st.error(
        "Nuk arritëm t'i marrim të dhënat dhe "
        "nuk ekziston ende një cache lokale."
    )

    st.exception(error)

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🇽🇰 Ku ia vlen të jetosh në Kosovë?'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Zgjidh prioritetet e tua dhe zbulo komunën '
    'që përshtatet më së miri me stilin tënd të jetesës.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATA STATUS
# ============================================================

if data_mode == "live":

    st.success(
        "🟢 Të dhënat janë marrë live nga API-të.",
        icon=None
    )

else:

    st.warning(
        "🟡 ASKdata është përkohësisht i paarritshëm. "
        "Po përdoret snapshot-i i fundit i ruajtur."
    )


# ============================================================
# SIDEBAR - USER PREFERENCES
# ============================================================

with st.sidebar:

    st.header("🎯 Prioritetet e tua")

    st.caption(
        "Nuk është e nevojshme që peshat të bëjnë 100%. "
        "Aplikacioni i normalizon automatikisht."
    )

    employment_weight = st.slider(
        "💼 Punësimi",
        min_value=0,
        max_value=100,
        value=35,
        step=5
    )

    education_weight = st.slider(
        "🎓 Arsimi",
        min_value=0,
        max_value=100,
        value=20,
        step=5
    )

    air_quality_weight = st.slider(
        "🌳 Cilësia e ajrit",
        min_value=0,
        max_value=100,
        value=30,
        step=5
    )

    community_weight = st.slider(
        "🏘️ Komuniteti / urbanizimi",
        min_value=0,
        max_value=100,
        value=15,
        step=5
    )

    st.divider()

    st.subheader("🏡 Çfarë ambienti preferon?")

    community_choice = st.radio(
        "Stili i jetesës",
        options=[
            "🏙️ Më urban",
            "🌲 Më i qetë"
        ],
        index=0
    )

    if community_choice == "🌲 Më i qetë":
        community_preference = "quiet"
    else:
        community_preference = "urban"

    st.divider()

    total_selected_weight = (
        employment_weight
        + education_weight
        + air_quality_weight
        + community_weight
    )

    st.metric(
        "Totali i peshave",
        total_selected_weight
    )

    if total_selected_weight == 0:

        st.warning(
            "Zgjidh të paktën një prioritet më të madh se 0."
        )

        st.stop()


# ============================================================
# CALCULATE PERSONALIZED SCORE
# ============================================================

ranking = calculate_living_score(
    master,

    employment_weight=employment_weight,
    education_weight=education_weight,
    air_quality_weight=air_quality_weight,
    community_weight=community_weight,

    community_preference=community_preference
)


best = ranking.iloc[0]


# ============================================================
# BEST MATCH
# ============================================================

st.subheader("🥇 Zgjedhja më e mirë për ty")

st.markdown(
    f"""
<div class="best-card">
<div class="small-label">PERSONALIZED BEST MATCH</div>
<div class="best-name">{best["Municipality"]}</div>
<div class="best-score">{best["LivingScore"]:.1f}/100</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# COMPONENT METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💼 Jobs Score",
        f'{best["JobsScore"]:.1f}/100'
    )


with col2:

    st.metric(
        "🎓 Education Score",
        f'{best["EducationScore"]:.1f}/100'
    )


with col3:

    st.metric(
        "🌳 Air Quality Score",
        f'{best["AirQualityScore"]:.1f}/100'
    )


with col4:

    st.metric(
        "🏘️ Community Score",
        f'{best["CommunityScore"]:.1f}/100'
    )


# ============================================================
# AI INSIGHT
# ============================================================

st.divider()

st.subheader("🤖 AI Insight")

st.caption(
    "AI shpjegon rezultatet e llogaritura nga aplikacioni. "
    "Nuk vendos vetë renditjen."
)

if st.button(
    "✨ Gjenero shpjegimin me AI",
    use_container_width=True
):

    with st.spinner(
        "Gemini po analizon rezultatet..."
    ):

        ai_insight = generate_ai_insight(
            ranking=ranking,
            employment_weight=employment_weight,
            education_weight=education_weight,
            air_quality_weight=air_quality_weight,
            community_weight=community_weight,
            community_preference=community_preference
        )

    st.info(ai_insight)

# ============================================================
# TOP 5
# ============================================================

st.divider()

st.subheader("🏆 Top 5 komunat për ty")

top5 = ranking.head(5).copy()

top5_display = top5[
    [
        "Rank",
        "Municipality",
        "LivingScore"
    ]
].copy()

top5_display.columns = [
    "Renditja",
    "Komuna",
    "Living Score"
]

st.dataframe(
    top5_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# KOSOVO MAP
# ============================================================

st.divider()

st.subheader("🗺️ Harta e Kosovës")

st.caption(
    "Madhësia e pikës dhe intensiteti vizual bazohen "
    "në Personalized Living Score."
)


map_data = ranking[
    [
        "Municipality",
        "Latitude",
        "Longitude",
        "LivingScore",
        "JobsScore",
        "EducationScore",
        "AirQualityScore",
        "CommunityScore"
    ]
].copy()


# Radius based on Living Score
map_data["radius"] = (
    4000
    + map_data["LivingScore"] * 110
)


layer = pdk.Layer(
    "ScatterplotLayer",

    data=map_data,

    get_position=[
        "Longitude",
        "Latitude"
    ],

    get_radius="radius",

    get_fill_color=[
        30,
        140,
        200,
        170
    ],

    pickable=True,

    auto_highlight=True
)


view_state = pdk.ViewState(
    latitude=42.60,
    longitude=20.90,
    zoom=7.3,
    pitch=0
)


tooltip = {
    "html": """
        <b>{Municipality}</b><br/>
        ⭐ Living Score: {LivingScore}<br/>
        💼 Jobs: {JobsScore}<br/>
        🎓 Education: {EducationScore}<br/>
        🌳 Air: {AirQualityScore}<br/>
        🏘️ Community: {CommunityScore}
    """,

    "style": {
        "backgroundColor": "#111111",
        "color": "white"
    }
}


deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
)


st.pydeck_chart(
    deck,
    use_container_width=True
)


# ============================================================
# FULL RANKING
# ============================================================

st.divider()

st.subheader("📊 Renditja e plotë")


ranking_display = ranking[
    [
        "Rank",
        "Municipality",
        "LivingScore",
        "JobsScore",
        "EducationScore",
        "AirQualityScore",
        "CommunityScore",
        "Population2024",
        "CurrentAQI"
    ]
].copy()


ranking_display.columns = [
    "Renditja",
    "Komuna",
    "Living Score",
    "Jobs",
    "Education",
    "Air Quality",
    "Community",
    "Popullsia 2024",
    "AQI aktual"
]


st.dataframe(
    ranking_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MUNICIPALITY DETAILS
# ============================================================

st.divider()

st.subheader("🔍 Shiko një komunë")


selected_municipality = st.selectbox(
    "Zgjidh komunën",
    options=ranking["Municipality"].tolist()
)


selected = ranking[
    ranking["Municipality"]
    == selected_municipality
].iloc[0]


detail1, detail2, detail3, detail4 = st.columns(4)


with detail1:

    st.metric(
        "⭐ Living Score",
        f'{selected["LivingScore"]:.1f}'
    )


with detail2:

    st.metric(
        "👥 Popullsia 2024",
        f'{selected["Population2024"]:,.0f}'
    )


with detail3:

    st.metric(
        "🎓 Arsim i lartë",
        f'{selected["HigherEducationRate"]:.1f}%'
    )


with detail4:

    st.metric(
        "🌳 AQI 24h",
        f'{selected["AQI24h"]:.1f}'
    )


detail5, detail6, detail7 = st.columns(3)


with detail5:

    st.metric(
        "💼 Të punësuar / 1,000 banorë",
        f'{selected["EmployedPer1000"]:.1f}'
    )


with detail6:

    st.metric(
        "🏘️ Vendbanime",
        f'{selected["Settlements"]:.0f}'
    )


with detail7:

    st.metric(
        "👥 Banorë / vendbanim",
        f'{selected["PopulationPerSettlement"]:.0f}'
    )


# ============================================================
# METHODOLOGY
# ============================================================

st.divider()

with st.expander(
    "ℹ️ Si llogaritet Personalized Living Score?"
):

    st.markdown(
        """
        **Living Score** kombinon katër dimensione:

        - 💼 **Jobs Score** — bazuar në numrin e të
          punësuarve për 1,000 banorë.

        - 🎓 **Education Score** — bazuar në përqindjen
          e popullsisë 15+ me arsim të lartë.

        - 🌳 **Air Quality Score** — bazuar në mesataren
          e European AQI gjatë 24 orëve të fundit.
          AQI më i ulët = score më i mirë.

        - 🏘️ **Community Score** — bazuar në raportin
          popullsi / vendbanime dhe preferencën
          Urban ose Quiet.

        Indikatorët transformohen në score 0–100 duke
        përdorur renditjen percentile mes komunave.

        Peshat që zgjedh përdoruesi normalizohen
        automatikisht.
        """
    )


# ============================================================
# DATA SOURCES
# ============================================================

with st.expander(
    "📚 Burimet e të dhënave"
):

    st.markdown(
        """
        **ASKdata**
        - Population estimates by municipality
        - Census 2024 employment
        - Census 2024 education
        - Number of settlements by municipality

        **Open-Meteo / CAMS**
        - European AQI
        - PM2.5
        - PM10
        - NO₂
        - O₃
        """
    )