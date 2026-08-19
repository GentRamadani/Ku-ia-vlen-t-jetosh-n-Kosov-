from data_loader import load_air_quality_data


df_air = load_air_quality_data()


print("\nFirst 10 rows:")
print(df_air.head(10))


print("\nShape:")
print(df_air.shape)


print("\nColumns:")
print(df_air.columns.tolist())


print("\nTotal municipalities:")
print(df_air["Municipality"].nunique())


print("\nAQI statistics:")
print(df_air["AQI24h"].describe())


print("\nBest air quality:")
print(
    df_air
    .sort_values("AQI24h")
    [
        [
            "Municipality",
            "CurrentAQI",
            "AQI24h"
        ]
    ]
    .head(10)
)