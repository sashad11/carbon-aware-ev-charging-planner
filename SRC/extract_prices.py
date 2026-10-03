import requests
import json

url = "https://api.octopus.energy/v1/products/AGILE-24-10-01/electricity-tariffs/E-1R-AGILE-24-10-01-C/standard-unit-rates/"

params = {
    "period_from": "2026-10-03T00:00Z",
    "period_to": "2026-10-04T00:00Z"
}

response = requests.get(url, params=params)

print(response.status_code)

with open("Data/Raw Data/electricity_prices.json", "w") as file:
    json.dump(response.json(), file, indent=4)