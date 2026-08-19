from data_loader import load_master_data
from scoring import calculate_living_score
from ai_insights import generate_ai_insight


master = load_master_data()


employment_weight = 35
education_weight = 20
air_quality_weight = 30
community_weight = 15
community_preference = "urban"


ranking = calculate_living_score(
    master,
    employment_weight=employment_weight,
    education_weight=education_weight,
    air_quality_weight=air_quality_weight,
    community_weight=community_weight,
    community_preference=community_preference
)


insight = generate_ai_insight(
    ranking,
    employment_weight,
    education_weight,
    air_quality_weight,
    community_weight,
    community_preference
)


print("\n====================================")
print("AI INSIGHT")
print("====================================\n")

print(insight)