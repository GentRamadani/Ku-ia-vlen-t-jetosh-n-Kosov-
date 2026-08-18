from data_loader import load_employment_data


df_employment = load_employment_data()


print("\nFirst 10 rows:")
print(df_employment.head(10))


print("\nShape:")
print(df_employment.shape)


print("\nColumns:")
print(df_employment.columns.tolist())


print("\nTotal municipalities:")
print(df_employment["Municipality"].nunique())


print("\nEmployment statistics:")
print(df_employment["Employed"].describe())