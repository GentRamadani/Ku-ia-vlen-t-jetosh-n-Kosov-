import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="About | Ku ia vlen të jetosh në Kosovë?",
    page_icon="ℹ️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .about-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .about-subtitle {
        font-size: 20px;
        color: #888;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    .about-text {
        font-size: 17px;
        line-height: 1.7;
    }

    .highlight-box {
        padding: 22px;
        border-radius: 16px;
        background-color: rgba(120, 120, 120, 0.08);
        border: 1px solid rgba(120, 120, 120, 0.20);
        margin-top: 15px;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="about-title">ℹ️ About This Project</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="about-subtitle">'
    'Ku ia vlen të jetosh në Kosovë?'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
    """
    <div class="about-text">

    <b>“Ku ia vlen të jetosh në Kosovë?”</b> is a data-driven
    web application designed to help people explore which
    municipality in Kosovo may best match their personal
    priorities and lifestyle.

    <br><br>

    The idea behind the project is simple:
    <b>there is no single “best” municipality for everyone.</b>

    A young professional looking for job opportunities may value
    different things than a family, a student, or someone who
    prefers a quieter environment.

    <br><br>

    Instead of giving everyone the same answer, the application
    creates a <b>Personalized Living Score</b> based on what
    matters most to each user.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TARGET USERS
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Who Is This For?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    The project is mainly designed for:

    - **Young professionals** deciding where to build their career and live.
    - **Students and young adults** thinking about where they may want to settle in the future.
    - **Families** comparing municipalities before moving.
    - **Citizens** who want to better understand how their municipality compares with others.
    - **People considering relocation within Kosovo** who want a simple, data-based starting point for their decision.

    The goal is not to tell people where they *must* live,
    but to help them make a more informed decision using real data.
    """
)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">⚙️ How Does It Work?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    Users choose how important different factors are to them.

    The current version focuses on four main dimensions:
    """
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        ### 💼 Employment

        How strong the municipality performs in terms of
        employment relative to its population.

        ### 🎓 Education

        The share of the population with higher levels
        of education.
        """
    )


with col2:

    st.markdown(
        """
        ### 🌳 Air Quality

        Recent air-quality conditions based on the
        European Air Quality Index.

        ### 🏘️ Community & Urbanization

        Helps distinguish between more concentrated urban
        environments and quieter, less concentrated municipalities.
        """
    )


st.markdown(
    """
    Users can increase or decrease the importance of each factor
    and also choose whether they prefer a **more urban** or a
    **quieter** environment.

    The application then recalculates the ranking and shows the
    municipalities that best match those preferences.
    """
)


# ============================================================
# DATA SOURCES
# ============================================================

st.markdown(
    '<div class="section-title">📊 Our Data Sources</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    The project combines multiple data sources instead of relying
    on a single dataset.

    Most official statistics come from
    **ASKdata — the Kosovo Agency of Statistics**, including:

    - Population by municipality
    - Employment data from the 2024 Census
    - Education data from the 2024 Census
    - Number of settlements by municipality

    For environmental information, the application also uses
    **Open-Meteo Air Quality data**, including:

    - European Air Quality Index
    - PM2.5
    - PM10
    - NO₂
    - O₃

    These sources are combined by municipality so that they
    contribute to one overall decision-making tool rather than
    being displayed as separate datasets.
    """
)


# ============================================================
# AUTOMATION
# ============================================================

st.markdown(
    '<div class="section-title">🔄 Automated Data Collection</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    The application is designed to minimize manual data handling.

    Instead of requiring users to upload CSV files, the project
    automatically retrieves data from **ASKdata APIs** and the
    **Open-Meteo API**.

    The data is then prepared, matched across municipalities,
    and used by the scoring system automatically.

    To make the application more reliable during temporary API
    outages, the project also keeps a local cached version of the
    most recently loaded data.

    This allows the app to continue working even if one of the
    external data services is temporarily unavailable.
    """
)


# ============================================================
# PERSONALIZED LIVING SCORE
# ============================================================

st.markdown(
    '<div class="section-title">⭐ Personalized Living Score</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    The main feature of the application is the
    **Personalized Living Score**.

    Rather than creating one fixed ranking for Kosovo, the score
    changes according to the user's priorities.

    For example, someone who gives more importance to employment
    and education may receive a very different recommendation
    from someone who prioritizes clean air and a quieter environment.

    The final result includes:

    - A personalized score for every municipality
    - A Top 5 ranking
    - Individual scores for employment, education, air quality, and community
    - A map of Kosovo showing the municipalities
    - Detailed information for each municipality

    This makes the application a **decision-support tool**,
    not just a statistics dashboard.
    """
)


# ============================================================
# AI INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">🤖 AI Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    The application also includes an
    **AI-generated explanation powered by Google Gemini**.

    The AI does **not** decide which municipality ranks first.

    The ranking and scores are calculated by the application's
    data model first. The AI then receives those results and
    explains them in simple language.

    The AI can explain:

    - Why a municipality ranked first for the user's priorities
    - What its strongest characteristics are
    - What trade-off the user should consider
    - Which municipality could be a good alternative

    This makes the results easier to understand for users who
    may not be familiar with statistical indicators.
    """
)


# ============================================================
# WHY IT MATTERS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Why This Project Matters</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    Many public datasets contain valuable information, but they
    can be difficult for ordinary citizens to interpret or combine.

    This project turns those statistics into a question that people
    can immediately understand:
    """
)

st.markdown(
    """
    <div class="highlight-box">

    <h3>
    “Based on what matters to me, where in Kosovo might be
    a good place to live?”
    </h3>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    By combining official statistics, live environmental data,
    personalized analysis, and AI-generated explanations, the
    application aims to make public data more accessible and
    useful for real-life decisions.
    """
)