import requests


WASTE_URL = (
    "https://askdata.rks-gov.net/api/v1/en/ASKdata/"
    "Environment/"
    "Mbeturinat/"
    "Anketa e Mbeturinave Komunale/"
    "env02.px"
)


response = requests.get(
    WASTE_URL,
    timeout=30
)

print("Status:", response.status_code)

response.raise_for_status()

metadata = response.json()


print("\nDataset:")
print(metadata.get("title"))


print("\nVariables:")

for variable in metadata["variables"]:

    print("\n================================")
    print("Code:", variable["code"])
    print("Text:", variable["text"])
    print("Number of values:", len(variable["values"]))

    for code, label in zip(
        variable["values"],
        variable["valueTexts"]
    ):
        print(code, "->", label)