from data_loader import load_master_data
from scoring import calculate_living_score


# Load all data
master = load_master_data()


# Calculate personalized score
ranking = calculate_living_score(
    master,

    employment_weight=35,
    education_weight=20,
    air_quality_weight=30,
    community_weight=15,

    community_preference="urban"
)


print("\n====================================")
print("PERSONALIZED LIVING SCORE")
print("====================================\n")


print(
    ranking[
        [
            "Rank",
            "Municipality",
            "LivingScore",
            "JobsScore",
            "EducationScore",
            "AirQualityScore",
            "CommunityScore"
        ]
    ].head(10)
)


print("\nBest municipality:")
print(
    ranking.iloc[0][
        [
            "Municipality",
            "LivingScore"
        ]
    ]
)


print("\nTop 5:")
print(
    ranking[
        [
            "Rank",
            "Municipality",
            "LivingScore"
        ]
    ].head(5)
)