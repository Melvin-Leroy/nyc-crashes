import pandas as pd


from geopy.geocoders import Nominatim


def parse(row: pd.DataFrame, column_name: str):
    geolocator = Nominatim(user_agent="Melvin")
    location = geolocator.reverse((row.loc["latitude"], row.loc["longitude"]))
    print(location.raw["address"])
    if "postcode" in location.raw["address"].keys() and \
            "suburb" in location.raw["address"].keys() and \
            "road" in location.raw["address"].keys():
        if column_name == "zip_code":
            location = location.raw["address"]["postcode"]
            if ":" in location:
                location = location.split(":")
                return location[0]
            elif "-" in location:
                location = location.split("-")
                return location[0]
            else:
                return location

        elif column_name == "borough":
            return location.raw["address"]["suburb"]
        elif column_name == "on_street_name":
            if pd.isnull(row["on_street_name"]):
                return location.raw["address"]["road"]
            else:
                return row["on_street_name"]
    else:
        return None


pd.options.display.max_columns = None

df = pd.read_csv("data_200.csv")

print(df.info())

# Drop some columns
columns_names_to_drop = ["off_street_name", "cross_street_name", "contributing_factor_vehicle_3",
                         "contributing_factor_vehicle_4", "contributing_factor_vehicle_5", "vehicle_type_code_3",
                         "vehicle_type_code_4", "vehicle_type_code_5"]
df = df.drop(columns_names_to_drop, axis=1)

# Drop lines without lat and long
df = df.drop(df[df.latitude.isna()].index)
df = df.drop(df[df.longitude.isna()].index)
df = df.drop(df[df.longitude < -100].index)

# Remove white spaces before and after string.
df["borough"] = df["borough"].str.strip()
df["on_street_name"] = df["on_street_name"].str.strip()
df["location"] = df["location"].str.strip()
df["contributing_factor_vehicle_1"] = df["contributing_factor_vehicle_1"].str.strip()
df["contributing_factor_vehicle_2"] = df["contributing_factor_vehicle_2"].str.strip()
df["vehicle_type_code1"] = df["vehicle_type_code1"].str.strip()
df["vehicle_type_code2"] = df["vehicle_type_code2"].str.strip()

# Capitalize some columns and merge some data
df["borough"] = df["borough"].str.capitalize()
df["on_street_name"] = df["on_street_name"].str.capitalize()
df["vehicle_type_code1"] = df["vehicle_type_code1"].str.capitalize()
df["vehicle_type_code2"] = df["vehicle_type_code2"].str.capitalize()
df["vehicle_type_code1"] = df["vehicle_type_code1"].replace("Station wagon/sport utility vehicle",
                                                            "Sport utility / station wagon")
df["vehicle_type_code2"] = df["vehicle_type_code2"].replace("Station wagon/sport utility vehicle",
                                                            "Sport utility / station wagon")

# Replace NaN values
df["vehicle_type_code1"] = df["vehicle_type_code1"].fillna("Unknown")
df["vehicle_type_code2"] = df["vehicle_type_code2"].fillna("Unknown")
df["contributing_factor_vehicle_1"] = df["contributing_factor_vehicle_1"].fillna("Unspecified")
df["contributing_factor_vehicle_2"] = df["contributing_factor_vehicle_2"].fillna("Unspecified")

# Adding missing values from lat and long
zip_list = [parse(row, "zip_code") for index, row in df.iterrows()]
df["zip_code"] = zip_list
borough_list = [parse(row, "borough") for index, row in df.iterrows()]
df["borough"] = borough_list
street_list = [parse(row, "on_street_name") for index, row in df.iterrows()]
df["on_street_name"] = street_list

# Dropping rows if no value was found.
df = df.drop(df[df.zip_code.isna()].index)
df = df.drop(df[df.borough.isna()].index)
df = df.drop(df[df.on_street_name.isna()].index)

# Change dtypes.
df["crash_date"] = pd.to_datetime(df["crash_date"])
df["zip_code"] = df["zip_code"].astype(int)

print(df.info())
