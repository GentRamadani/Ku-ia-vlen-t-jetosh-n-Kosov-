import pandas as pd


# ============================================================
# Helper functions
# ============================================================

def percentile_score(series, higher_is_better=True):
    """
    Converts a numeric indicator into a 0-100 score
    using percentile ranking.

    higher_is_better=True:
        Higher raw value -> higher score.

    higher_is_better=False:
        Lower raw value -> higher score.
    """

    numeric_series = pd.to_numeric(
        series,
        errors="coerce"
    )

    if higher_is_better:
        scores = numeric_series.rank(
            method="average",
            pct=True,
            ascending=True
        ) * 100

    else:
        scores = numeric_series.rank(
            method="average",
            pct=True,
            ascending=False
        ) * 100

    return scores


# ============================================================
# Component Scores
# ============================================================

def calculate_component_scores(
    df,
    community_preference="urban"
):
    """
    Creates the individual 0-100 scores used
    by the Personalized Living Score.

    community_preference:
        "urban" -> more concentrated municipality preferred
        "quiet" -> less concentrated municipality preferred
    """

    result = df.copy()

    # --------------------------------------------------------
    # Jobs
    # Higher employed persons per 1,000 residents = better
    # --------------------------------------------------------

    result["JobsScore"] = percentile_score(
        result["EmployedPer1000"],
        higher_is_better=True
    )

    # --------------------------------------------------------
    # Education
    # Higher percentage with higher education = better
    # --------------------------------------------------------

    result["EducationScore"] = percentile_score(
        result["HigherEducationRate"],
        higher_is_better=True
    )

    # --------------------------------------------------------
    # Air Quality
    # Lower AQI = better
    # --------------------------------------------------------

    result["AirQualityScore"] = percentile_score(
        result["AQI24h"],
        higher_is_better=False
    )

    # --------------------------------------------------------
    # Community / urbanity
    # --------------------------------------------------------

    if community_preference == "quiet":

        result["CommunityScore"] = percentile_score(
            result["PopulationPerSettlement"],
            higher_is_better=False
        )

    else:

        result["CommunityScore"] = percentile_score(
            result["PopulationPerSettlement"],
            higher_is_better=True
        )

    return result


# ============================================================
# Personalized Living Score
# ============================================================

def calculate_living_score(
    df,
    employment_weight=35,
    education_weight=20,
    air_quality_weight=30,
    community_weight=15,
    community_preference="urban"
):
    """
    Calculates the Personalized Living Score.

    Weights do NOT need to sum to 100.
    They are normalized automatically.

    Example:
        employment_weight = 40
        education_weight = 20
        air_quality_weight = 30
        community_weight = 10

    Returns:
        pd.DataFrame sorted from best to worst.
    """

    result = calculate_component_scores(
        df,
        community_preference=community_preference
    )

    # --------------------------------------------------------
    # Validate weights
    # --------------------------------------------------------

    weights = {
        "employment": float(employment_weight),
        "education": float(education_weight),
        "air_quality": float(air_quality_weight),
        "community": float(community_weight)
    }

    for name, value in weights.items():

        if value < 0:
            raise ValueError(
                f"{name} weight cannot be negative."
            )

    total_weight = sum(
        weights.values()
    )

    if total_weight == 0:
        raise ValueError(
            "At least one weight must be greater than 0."
        )

    # --------------------------------------------------------
    # Normalize weights
    # --------------------------------------------------------

    employment_weight_normalized = (
        weights["employment"]
        / total_weight
    )

    education_weight_normalized = (
        weights["education"]
        / total_weight
    )

    air_quality_weight_normalized = (
        weights["air_quality"]
        / total_weight
    )

    community_weight_normalized = (
        weights["community"]
        / total_weight
    )

    # --------------------------------------------------------
    # Personalized Living Score
    # --------------------------------------------------------

    result["LivingScore"] = (
        result["JobsScore"]
        * employment_weight_normalized

        +

        result["EducationScore"]
        * education_weight_normalized

        +

        result["AirQualityScore"]
        * air_quality_weight_normalized

        +

        result["CommunityScore"]
        * community_weight_normalized
    )

    result["LivingScore"] = (
        result["LivingScore"]
        .round(1)
    )

    # Round component scores
    score_columns = [
        "JobsScore",
        "EducationScore",
        "AirQualityScore",
        "CommunityScore"
    ]

    result[score_columns] = (
        result[score_columns]
        .round(1)
    )

    # --------------------------------------------------------
    # Ranking
    # --------------------------------------------------------

    result = result.sort_values(
        "LivingScore",
        ascending=False
    ).reset_index(drop=True)

    result["Rank"] = (
        result.index + 1
    )

    return result