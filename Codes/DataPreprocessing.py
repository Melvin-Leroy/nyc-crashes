import pandas as pd


from geopy.geocoders import Nominatim


def parse(latitude_list, longitude_list, street_list):
    new_zip_code = []
    new_borough = []
    new_street = []
    for index in range(len(latitude_list)):
        geolocator = Nominatim(user_agent="Melvin")
        location = geolocator.reverse((latitude_list[index], longitude_list[index]))
        if "postcode" in location.raw["address"].keys() and \
                "suburb" in location.raw["address"].keys() and \
                "road" in location.raw["address"].keys():
            loc = location.raw["address"]["postcode"]
            if ":" in loc:
                loc = loc.split(":")
                new_zip_code += [loc[0]]
            elif "-" in loc:
                loc = loc.split("-")
                new_zip_code += [loc[0]]
            else:
                new_zip_code += [loc]
            new_borough += [location.raw["address"]["suburb"]]
            if pd.isnull(street_list[index]):
                new_street += [location.raw["address"]["road"]]
            else:
                new_street += [street_list[index]]
        else:
            new_zip_code += [None]
            new_street += [None]
            new_borough += [None]
        print(index)

    return new_street, new_borough, new_zip_code


def round5(number: float) -> float:
    number = round(number, 5)
    return number


pd.options.display.max_columns = None

df = pd.read_csv("data_100000.csv")

# Drop some columns
columns_names_to_drop = ["off_street_name", "cross_street_name", "contributing_factor_vehicle_3",
                         "contributing_factor_vehicle_4", "contributing_factor_vehicle_5", "vehicle_type_code_3",
                         "vehicle_type_code_4", "vehicle_type_code_5", "collision_id"]
df = df.drop(columns_names_to_drop, axis=1)

# Drop lines without lat and long
df = df.drop(df[df.latitude.isna()].index)
df = df.drop(df[df.longitude.isna()].index)
df = df.drop(df[df.longitude < -100].index)

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

# Change dtypes.
df["crash_date"] = pd.to_datetime(df["crash_date"])
df["zip_code"] = df["zip_code"].astype(int)

# Save the data in a csv
df.to_csv("Results.csv", index=False)
