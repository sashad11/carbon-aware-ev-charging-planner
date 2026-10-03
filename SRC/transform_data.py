import json
from datetime import datetime
import duckdb

with open("Data/Raw Data/carbon_intensity.json", "r") as file:
    carbon_raw = json.load(file)

carbon_records = carbon_raw["data"]

print(carbon_records[0])

clean_carbon = []

for record in carbon_records:
    clean_carbon.append({
        "start_time": datetime.fromisoformat(record["from"].replace("Z", "+00:00")),
        "end_time": datetime.fromisoformat(record["to"].replace("Z", "+00:00")),
        "carbon_forecast": record["intensity"]["forecast"],
        "carbon_actual": record["intensity"]["actual"],
        "carbon_index": record["intensity"]["index"]
    })

print(clean_carbon[0])

print("Number of carbon records:", len(clean_carbon))

missing_values = 0

for record in clean_carbon:
    if None in record.values():
        missing_values += 1

print("Records with missing values:", missing_values)

start_times = [record["start_time"] for record in clean_carbon]

duplicates = len(start_times) - len(set(start_times))

print("Duplicate start times:", duplicates)

for column in clean_carbon[0].keys():
    missing_count = sum(
        record[column] is None
        for record in clean_carbon
    )
    print(column, "missing:", missing_count)

with open("Data/Raw Data/electricity_prices.json", "r") as file:
    price_raw = json.load(file)

price_records = price_raw["results"]

print(price_records[0])

clean_prices = []

for record in price_records:
    clean_prices.append({
        "start_time": datetime.fromisoformat(record["valid_from"].replace("Z", "+00:00")),
        "end_time": datetime.fromisoformat(record["valid_to"].replace("Z", "+00:00")),
        "price_p_per_kwh": record["value_inc_vat"]
    })

print(clean_prices[0]) 

print("Number of price records:", len(clean_prices))

for column in clean_prices[0].keys():
    missing_count = sum(
        record[column] is None
        for record in clean_prices
    )
    print(column, "missing:", missing_count)

price_start_times = [record["start_time"] for record in clean_prices]

price_duplicates = len(price_start_times) - len(set(price_start_times))

print("Duplicate price start times:", price_duplicates)

carbon_times = set(record["start_time"] for record in clean_carbon)
price_times = set(record["start_time"] for record in clean_prices)

carbon_only = sorted(carbon_times - price_times)
price_only = sorted(price_times - carbon_times)

print("Carbon times without a matching price:")
print(carbon_only)

print("Price times without matching carbon data:")
print(price_only)

con = duckdb.connect("carbon_energy.duckdb")
con.execute("""
    CREATE OR REPLACE TABLE carbon_intensity (
        start_time TIMESTAMPTZ,
        end_time TIMESTAMPTZ,
        carbon_forecast INTEGER,
        carbon_actual INTEGER,
        carbon_index VARCHAR
    )
""")
for record in clean_carbon:
    con.execute("""
        INSERT INTO carbon_intensity
        VALUES (?, ?, ?, ?, ?)
    """, [
        record["start_time"],
        record["end_time"],
        record["carbon_forecast"],
        record["carbon_actual"],
        record["carbon_index"]
    ])
    result = con.execute("""
    SELECT COUNT(*)
    FROM carbon_intensity
""").fetchone()

print("Rows in carbon table:", result[0])
con.execute("""
    CREATE OR REPLACE TABLE electricity_prices (
        start_time TIMESTAMPTZ,
        end_time TIMESTAMPTZ,
        price_p_per_kwh DOUBLE
    )
""")
for record in clean_prices:
    con.execute("""
        INSERT INTO electricity_prices
        VALUES (?, ?, ?)
    """, [
        record["start_time"],
        record["end_time"],
        record["price_p_per_kwh"]
    ])
    result = con.execute("""
    SELECT COUNT(*)
    FROM electricity_prices
""").fetchone()

print("Rows in price table:", result[0])

with open("SQL/create_charging_data.sql", "r") as file:
    charging_sql = file.read()

con.execute(charging_sql)

result = con.execute("""
    SELECT COUNT(*)
    FROM charging_data
""").fetchone()

print("Rows in charging table:", result[0])

con.close()
