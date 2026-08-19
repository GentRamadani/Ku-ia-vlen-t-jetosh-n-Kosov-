import os

from google import genai
from google.genai import types


# ============================================================
# Gemini - AI Insights
# ============================================================


def generate_ai_insight(
    ranking,
    employment_weight,
    education_weight,
    air_quality_weight,
    community_weight,
    community_preference
):
    """
    Generates a short AI explanation for the personalized
    municipality recommendation.

    IMPORTANT:
    Gemini does not calculate the ranking.
    It only explains results already calculated by scoring.py.
    """

    # --------------------------------------------------------
    # Check API key
    # --------------------------------------------------------

    if not os.getenv("GEMINI_API_KEY"):
        return (
            "AI Insight nuk është aktiv sepse "
            "GEMINI_API_KEY nuk është konfiguruar."
        )

    client = genai.Client()

    # --------------------------------------------------------
    # Get top municipalities
    # --------------------------------------------------------

    top3 = ranking.head(3)

    best = top3.iloc[0]
    second = top3.iloc[1]
    third = top3.iloc[2]

    # --------------------------------------------------------
    # Community preference
    # --------------------------------------------------------

    if community_preference == "quiet":
        lifestyle = (
            "ambient më i qetë dhe më pak i përqendruar"
        )
    else:
        lifestyle = (
            "ambient më urban dhe më i përqendruar"
        )

    # --------------------------------------------------------
    # Factual context
    # --------------------------------------------------------

    context = f"""
REZULTATI I PERSONALIZUAR

Prioritetet e përdoruesit:
- Punësimi: {employment_weight}
- Arsimi: {education_weight}
- Cilësia e ajrit: {air_quality_weight}
- Komuniteti / urbanizimi: {community_weight}
- Preferenca e jetesës: {lifestyle}

KOMUNA #1
Komuna: {best["Municipality"]}
Living Score: {best["LivingScore"]:.1f}/100
Jobs Score: {best["JobsScore"]:.1f}/100
Education Score: {best["EducationScore"]:.1f}/100
Air Quality Score: {best["AirQualityScore"]:.1f}/100
Community Score: {best["CommunityScore"]:.1f}/100
Popullsia 2024: {best["Population2024"]:.0f}
Higher Education Rate: {best["HigherEducationRate"]:.1f}%
AQI 24h: {best["AQI24h"]:.1f}
Employed per 1000 residents: {best["EmployedPer1000"]:.1f}

KOMUNA #2
Komuna: {second["Municipality"]}
Living Score: {second["LivingScore"]:.1f}/100
Jobs Score: {second["JobsScore"]:.1f}/100
Education Score: {second["EducationScore"]:.1f}/100
Air Quality Score: {second["AirQualityScore"]:.1f}/100
Community Score: {second["CommunityScore"]:.1f}/100

KOMUNA #3
Komuna: {third["Municipality"]}
Living Score: {third["LivingScore"]:.1f}/100
Jobs Score: {third["JobsScore"]:.1f}/100
Education Score: {third["EducationScore"]:.1f}/100
Air Quality Score: {third["AirQualityScore"]:.1f}/100
Community Score: {third["CommunityScore"]:.1f}/100
"""

    # --------------------------------------------------------
    # System instructions
    # --------------------------------------------------------

    system_instruction = """
Ti je analist i të dhënave për një aplikacion që ndihmon
qytetarët të krahasojnë komunat e Kosovës.

Shkruaj në gjuhën shqipe.

Detyra jote është vetëm të SHPJEGOSH rezultatin që është
llogaritur nga aplikacioni.

Rregulla:

1. Mos shpik asnjë statistikë.
2. Përdor vetëm të dhënat e dhëna.
3. Mos thuaj se një komunë është objektivisht
   "komuna më e mirë në Kosovë".
4. Thuaj se është përshtatja më e mirë sipas
   prioriteteve të zgjedhura.
5. Përmend arsyen kryesore pse komuna #1 doli e para.
6. Përmend një dobësi ose trade-off.
7. Përmend komunën #2 si alternativë.
8. Mbaje përgjigjen të shkurtër.
9. Maksimumi rreth 120 fjalë.
10. Mos shpik metodologji ose të dhëna.
11. Mos deklaro lidhje shkak-pasojë mes indikatorëve.
12. Ruaj emrat e komunave saktësisht siç janë dhënë.

Struktura:

Një paragraf i shkurtër me rekomandimin.

Pastaj:

**Çfarë duhet të dish:** një fjali me trade-off.

**Alternativë:** një fjali për komunën #2.
"""

    # --------------------------------------------------------
    # Call Gemini
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=context,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            )
        )

        return response.text

    except Exception as error:

        return (
            "AI Insight nuk mund të gjenerohej për momentin.\n"
            f"Gabim: {type(error).__name__}\n"
            f"Detaje: {str(error)}"
        )