from data_loader import load_master_data


df = load_master_data()


print("\n==============================")
print("MASTER DATASET")
print("==============================\n")


print(df.head(10))


print("\nShape:")
print(df.shape)


print("\nColumns:")
print(df.columns.tolist())


print("\nMunicipalities:")
print(df["Municipality"].tolist())


print("\nTotal municipalities:")
print(df["Municipality"].nunique())


print("\nMissing values:")
print(df.isna().sum())


print("\nImportant indicators:")
print(
    df[
        [
            "Municipality",
            "Population2024",
            "Employed",
            "EmployedPer1000",
            "HigherEducationRate",
            "Settlements",
            "PopulationPerSettlement",
            "AQI24h"
        ]
    ].head(20)
)