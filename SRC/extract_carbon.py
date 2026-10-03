import requests
import json

url = "https://api.carbonintensity.org.uk/intensity/2026-10-03T00:00Z/2026-10-04T00:00Z"

response = requests.get(url)

print(response.status_code)

with open("Data/Raw Data/carbon_intensity.json", "w") as file:
    json.dump(response.json(), file, indent=4)