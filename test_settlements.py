from data_loader import load_settlements_data


df_settlements = load_settlements_data()


print("\nFirst 10 rows:")
print(df_settlements.head(10))


print("\nShape:")
print(df_settlements.shape)


print("\nColumns:")
print(df_settlements.columns.tolist())


print("\nTotal municipalities:")
print(df_settlements["Municipality"].nunique())


print("\nSettlement statistics:")
print(df_settlements["Settlements"].describe())