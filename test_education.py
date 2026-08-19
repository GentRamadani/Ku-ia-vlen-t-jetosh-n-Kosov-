from data_loader import load_education_data


df_education = load_education_data()


print("\nFirst 10 rows:")
print(df_education.head(10))


print("\nShape:")
print(df_education.shape)


print("\nColumns:")
print(df_education.columns.tolist())


print("\nEducation statistics:")
print(
    df_education["HigherEducationRate"].describe()
)