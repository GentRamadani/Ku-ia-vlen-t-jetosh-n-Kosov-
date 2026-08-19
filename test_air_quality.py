import requests


ENVIRONMENT_URL = (
    "https://askdata.rks-gov.net/api/v1/en/ASKdata/"
    "Environment"
)


response = requests.get(
    ENVIRONMENT_URL,
    timeout=30
)

print("Status:", response.status_code)

response.raise_for_status()

data = response.json()


print("\nEnvironment categories:\n")

for item in data:
    print(
        f"{item['id']} -> {item['text']}"
    )