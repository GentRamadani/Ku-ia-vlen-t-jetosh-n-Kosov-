import requests
import pandas as pd


# ============================================================
# ASKdata - Population
# ============================================================

POPULATION_URL = (
    "https://askdata.rks-gov.net/api/v1/sq/ASKdata/"
    "Population/Estimate%2C%20projection%20and%20structure%20of%20population/"
    "Population%20estimate/tab001.px"
)


def get_population_metadata():
    """
    Gets metadata for the population dataset from ASKdata.
    """

    response = requests.get(
        POPULATION_URL,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def load_population_data():
    """
    Loads population data from ASKdata
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame:
            Municipality
            Year
            Population
    """

    # Get dataset metadata
    metadata = get_population_metadata()

    # Get the two variables from the dataset
    municipality_variable = metadata["variables"][0]
    year_variable = metadata["variables"][1]

    # Get the codes used by the API
    municipality_codes = municipality_variable["values"]
    year_codes = year_variable["values"]

    # Create the API query
    query = {
        "query": [
            {
                "code": municipality_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": municipality_codes
                }
            },
            {
                "code": year_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": year_codes
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    # Send query to ASKdata
    response = requests.post(
        POPULATION_URL,
        json=query,
        timeout=30
    )

    response.raise_for_status()

    # Convert response to JSON
    data = response.json()

    # Get municipality labels
    municipality_labels = (
        data["dimension"][municipality_variable["code"]]
        ["category"]["label"]
    )

    # Get year labels
    year_labels = (
        data["dimension"][year_variable["code"]]
        ["category"]["label"]
    )

    # Get population values
    population_values = data["value"]

    # Create rows
    rows = []

    index = 0

    for municipality in municipality_labels.values():

        for year in year_labels.values():

            rows.append({
                "Municipality": municipality,
                "Year": int(year),
                "Population": population_values[index]
            })

            index += 1

    # Convert to DataFrame
    df = pd.DataFrame(rows)

# ============================================================
# ASKdata - Employment
# ============================================================

EMPLOYMENT_URL = (
    "https://askdata.rks-gov.net/api/v1/en/ASKdata/"
    "Census%20population/"
    "4_Labour%20market/"
    "lc13ensus.px"
)


def get_employment_metadata():
    """
    Gets metadata for the employment dataset from ASKdata.
    """

    response = requests.get(
        EMPLOYMENT_URL,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def load_employment_data():
    """
    Loads total employed persons aged 15-64
    by municipality from ASKdata.

    All economic activities are included and summed
    to calculate total employment.

    Returns:
        pd.DataFrame:
            Municipality
            Employed
    """

    metadata = get_employment_metadata()

    # Find variables
    municipality_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Komuna"
    )

    economic_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Aktivitetet ekonomike - NACE Rev.2"
    )

    employment_status_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Statusi i punësimit"
    )

    sex_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Gjinia"
    )

    # All municipalities
    municipality_codes = municipality_variable["values"]

    # All economic activities
    economic_activity_codes = economic_variable["values"]

    # Total employment status
    total_employment_status = employment_status_variable["values"][0]

    # Total sex
    total_sex = sex_variable["values"][0]

    query = {
        "query": [
            {
                "code": municipality_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": municipality_codes
                }
            },
            {
                "code": economic_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": economic_activity_codes
                }
            },
            {
                "code": employment_status_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": [total_employment_status]
                }
            },
            {
                "code": sex_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": [total_sex]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    # Request data
    response = requests.post(
        EMPLOYMENT_URL,
        json=query,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # Get labels
    municipality_labels = (
        data["dimension"][municipality_variable["code"]]
        ["category"]["label"]
    )

    economic_labels = (
        data["dimension"][economic_variable["code"]]
        ["category"]["label"]
    )

    # Values returned by the API
    values = data["value"]

    municipalities = list(municipality_labels.values())
    economic_activities = list(economic_labels.values())

    # Create rows
    rows = []

    index = 0

    for municipality in municipalities:

        for economic_activity in economic_activities:

            rows.append({
                "Municipality": municipality,
                "EconomicActivity": economic_activity,
                "Employed": values[index]
            })

            index += 1

    df = pd.DataFrame(rows)

    # Sum all economic activities for each municipality
    df = (
        df.groupby("Municipality", as_index=False)["Employed"]
        .sum()
    )

    # Remove Kosovo total
    df = df[
        df["Municipality"] != "Kosovë"
    ].reset_index(drop=True)

# ============================================================
# ASKdata - Education
# ============================================================

EDUCATION_URL = (
    "https://askdata.rks-gov.net/api/v1/en/ASKdata/"
    "Census%20population/"
    "2_Education/"
    "tabcensusedu3.px"
)


def get_education_metadata():
    """
    Gets metadata for the education dataset from ASKdata.
    """

    response = requests.get(
        EDUCATION_URL,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def load_education_data():
    """
    Loads education data by municipality.

    Calculates the percentage of population aged 15+
    with higher education.

    Higher education includes:
    - Higher school
    - College / Bachelor's degree
    - Postgraduate degree
    - Doctorate degree

    Returns:
        pd.DataFrame:
            Municipality
            HigherEducationRate
    """

    metadata = get_education_metadata()

    # Find variables
    sex_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Sex"
    )

    municipality_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Municipality"
    )

    education_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Highest level of education completed"
    )

    ethnicity_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Ethnicity"
    )

    # --------------------------------------------------------
    # Select values
    # --------------------------------------------------------

    municipality_codes = municipality_variable["values"]

    # Total sex
    total_sex = sex_variable["values"][0]

    # Total ethnicity
    total_ethnicity = ethnicity_variable["values"][0]

    # All education levels
    education_codes = education_variable["values"]

    query = {
        "query": [
            {
                "code": sex_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": [total_sex]
                }
            },
            {
                "code": municipality_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": municipality_codes
                }
            },
            {
                "code": education_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": education_codes
                }
            },
            {
                "code": ethnicity_variable["code"],
                "selection": {
                    "filter": "item",
                    "values": [total_ethnicity]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    # --------------------------------------------------------
    # Request data
    # --------------------------------------------------------

    response = requests.post(
        EDUCATION_URL,
        json=query,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # --------------------------------------------------------
    # Get labels
    # --------------------------------------------------------

    municipality_labels = (
        data["dimension"]["Municipality"]
        ["category"]["label"]
    )

    education_labels = (
        data["dimension"]["Highest level of education completed"]
        ["category"]["label"]
    )

    values = data["value"]

    municipalities = list(municipality_labels.values())
    education_levels = list(education_labels.values())

    # --------------------------------------------------------
    # Build rows
    # --------------------------------------------------------

    rows = []

    index = 0

    for municipality in municipalities:

        for education_level in education_levels:

            rows.append({
                "Municipality": municipality,
                "EducationLevel": education_level,
                "Population": values[index]
            })

            index += 1

    df = pd.DataFrame(rows)

    # --------------------------------------------------------
    # Calculate higher education
    # --------------------------------------------------------

    higher_education_levels = [
        "Higher school",
        "College, Bachelor's degree",
        "Postgraduate degree",
        "Doctorate degree"
    ]

    higher_education = (
        df[
            df["EducationLevel"].isin(
                higher_education_levels
            )
        ]
        .groupby("Municipality")["Population"]
        .sum()
    )

    total_population = (
        df[
            df["EducationLevel"] == "Total"
        ]
        .set_index("Municipality")["Population"]
    )

    result = pd.DataFrame({
        "HigherEducation": higher_education,
        "Total15Plus": total_population
    }).reset_index()

    # Calculate percentage
    result["HigherEducationRate"] = (
        result["HigherEducation"]
        / result["Total15Plus"]
        * 100
    )

    # Remove Kosovo total
    result = result[
        result["Municipality"] != "Gjithsej"
    ].reset_index(drop=True)

    return result[
        [
            "Municipality",
            "HigherEducation",
            "Total15Plus",
            "HigherEducationRate"
        ]
    ]

    return df