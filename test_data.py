from data_loader import load_population_data


df_population = load_population_data()


print("\nFirst 10 rows:")
print(df_population.head(10))


print("\nShape:")
print(df_population.shape)


print("\nColumns:")
print(df_population.columns.tolist())


print("\nMunicipalities:")
print(df_population["Municipality"].unique())