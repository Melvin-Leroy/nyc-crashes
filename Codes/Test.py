import pandas as pd


pd.options.display.max_columns = None

df = pd.read_csv("data_1000.csv")

# Drop some columns
columns_names_to_drop = ["off_street_name", "cross_street_name", "contributing_factor_vehicle_3",
                         "contributing_factor_vehicle_4", "contributing_factor_vehicle_5", "vehicle_type_code_3",
                         "vehicle_type_code_4", "vehicle_type_code_5", "collision_id"]
df = df.drop(columns_names_to_drop, axis=1)

# Remove white spaces before and after strings.
df["borough"] = df["borough"].str.strip()
df["on_street_name"] = df["on_street_name"].str.strip()
df["location"] = df["location"].str.strip()
df["contributing_factor_vehicle_1"] = df["contributing_factor_vehicle_1"].str.strip()
df["contributing_factor_vehicle_2"] = df["contributing_factor_vehicle_2"].str.strip()
df["vehicle_type_code1"] = df["vehicle_type_code1"].str.strip()
df["vehicle_type_code2"] = df["vehicle_type_code2"].str.strip()

# Capitalize some columns
df["borough"] = df["borough"].str.capitalize()
df["on_street_name"] = df["on_street_name"].str.capitalize()
df["vehicle_type_code1"] = df["vehicle_type_code1"].str.capitalize()
df["vehicle_type_code2"] = df["vehicle_type_code2"].str.capitalize()

# Consolidate some values
df["vehicle_type_code1"] = df["vehicle_type_code1"].replace("Station wagon/sport utility vehicle",
                                                            "Sport utility / station wagon")
df["vehicle_type_code2"] = df["vehicle_type_code2"].replace("Station wagon/sport utility vehicle",
                                                            "Sport utility / station wagon")

# Replace NaN values
df["vehicle_type_code1"] = df["vehicle_type_code1"].fillna("Unknown")
df["vehicle_type_code2"] = df["vehicle_type_code2"].fillna("Unknown")
df["contributing_factor_vehicle_1"] = df["contributing_factor_vehicle_1"].fillna("Unspecified")
df["contributing_factor_vehicle_2"] = df["contributing_factor_vehicle_2"].fillna("Unspecified")

print(df.info())

# Select all nan rows
df_na = df[df.isna().any(axis=1)]
df_not_na = df.dropna()

df_not_na = df_not_na.set_index("location")

print(df_not_na.head())

df = df_na.join(df_not_na, on="location", how="left", lsuffix="_old", rsuffix="_new")

print(df.info())
print(df.head())



"""
# Change dtypes.
df["crash_date"] = pd.to_datetime(df["crash_date"])
df["zip_code"] = df["zip_code"].astype(int)
"""
"""
print(df.info())
print(df.head())

df.to_csv("Results.csv", index=False)
"""