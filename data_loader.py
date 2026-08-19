import requests
import pandas as pd

from municipalities import (
    MUNICIPALITY_COORDINATES,
    normalize_municipality_name
)


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

    metadata = get_population_metadata()

    municipality_variable = metadata["variables"][0]
    year_variable = metadata["variables"][1]

    municipality_codes = municipality_variable["values"]
    year_codes = year_variable["values"]

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

    response = requests.post(
        POPULATION_URL,
        json=query,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    municipality_labels = (
        data["dimension"][municipality_variable["code"]]
        ["category"]["label"]
    )

    year_labels = (
        data["dimension"][year_variable["code"]]
        ["category"]["label"]
    )

    population_values = data["value"]

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

    df = pd.DataFrame(rows)

    return df


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

    municipality_codes = municipality_variable["values"]

    economic_activity_codes = economic_variable["values"]

    total_employment_status = (
        employment_status_variable["values"][0]
    )

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

    response = requests.post(
        EMPLOYMENT_URL,
        json=query,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    municipality_labels = (
        data["dimension"][municipality_variable["code"]]
        ["category"]["label"]
    )

    economic_labels = (
        data["dimension"][economic_variable["code"]]
        ["category"]["label"]
    )

    values = data["value"]

    municipalities = list(
        municipality_labels.values()
    )

    economic_activities = list(
        economic_labels.values()
    )

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

    df = (
        df.groupby(
            "Municipality",
            as_index=False
        )["Employed"]
        .sum()
    )

    df = df[
        df["Municipality"] != "Kosovë"
    ].reset_index(drop=True)

    return df


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
            HigherEducation
            Total15Plus
            HigherEducationRate
    """

    metadata = get_education_metadata()

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

    municipality_codes = (
        municipality_variable["values"]
    )

    total_sex = (
        sex_variable["values"][0]
    )

    total_ethnicity = (
        ethnicity_variable["values"][0]
    )

    education_codes = (
        education_variable["values"]
    )

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

    response = requests.post(
        EDUCATION_URL,
        json=query,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    municipality_labels = (
        data["dimension"]["Municipality"]
        ["category"]["label"]
    )

    education_labels = (
        data[
            "dimension"
        ][
            "Highest level of education completed"
        ][
            "category"
        ][
            "label"
        ]
    )

    values = data["value"]

    municipalities = list(
        municipality_labels.values()
    )

    education_levels = list(
        education_labels.values()
    )

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
        .groupby(
            "Municipality"
        )["Population"]
        .sum()
    )

    total_population = (
        df[
            df["EducationLevel"] == "Total"
        ]
        .set_index(
            "Municipality"
        )["Population"]
    )

    result = pd.DataFrame({
        "HigherEducation": higher_education,
        "Total15Plus": total_population
    }).reset_index()

    result["HigherEducationRate"] = (
        result["HigherEducation"]
        / result["Total15Plus"]
        * 100
    )

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


# ============================================================
# ASKdata - Settlements
# ============================================================

SETTLEMENTS_URL = (
    "https://askdata.rks-gov.net/api/v1/en/ASKdata/"
    "Geographical%20data/"
    "geo02.px"
)


def get_settlements_metadata():
    """
    Gets metadata for the settlements dataset from ASKdata.
    """

    response = requests.get(
        SETTLEMENTS_URL,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def load_settlements_data():
    """
    Loads the number of settlements by municipality
    from ASKdata.

    Returns:
        pd.DataFrame:
            Municipality
            Settlements
    """

    metadata = get_settlements_metadata()

    municipality_variable = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Municipality"
    )

    variable_dimension = next(
        variable
        for variable in metadata["variables"]
        if variable["code"] == "Variable"
    )

    municipality_codes = (
        municipality_variable["values"]
    )

    number_of_settlements_code = (
        variable_dimension["values"][0]
    )

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
                "code": variable_dimension["code"],
                "selection": {
                    "filter": "item",
                    "values": [
                        number_of_settlements_code
                    ]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    response = requests.post(
        SETTLEMENTS_URL,
        json=query,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    municipality_labels = (
        data["dimension"]["Municipality"]
        ["category"]["label"]
    )

    settlements_values = data["value"]

    municipalities = list(
        municipality_labels.values()
    )

    rows = []

    for municipality, settlements in zip(
        municipalities,
        settlements_values
    ):

        rows.append({
            "Municipality": municipality,
            "Settlements": settlements
        })

    df = pd.DataFrame(rows)

    df = df[
        df["Municipality"] != "Total"
    ].reset_index(drop=True)

    return df


# ============================================================
# Open-Meteo - Air Quality
# ============================================================

AIR_QUALITY_URL = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
)


def load_air_quality_data():
    """
    Loads current air quality and the average AQI
    for the previous 24 hours for all Kosovo municipalities.

    Returns:
        pd.DataFrame:
            Municipality
            Latitude
            Longitude
            CurrentAQI
            AQI24h
            PM2_5_24h
            PM10_24h
            NO2_24h
            O3_24h
    """

    municipalities = list(
        MUNICIPALITY_COORDINATES.keys()
    )

    latitudes = [
        MUNICIPALITY_COORDINATES[
            municipality
        ][0]
        for municipality in municipalities
    ]

    longitudes = [
        MUNICIPALITY_COORDINATES[
            municipality
        ][1]
        for municipality in municipalities
    ]

    params = {
        "latitude": ",".join(
            str(latitude)
            for latitude in latitudes
        ),

        "longitude": ",".join(
            str(longitude)
            for longitude in longitudes
        ),

        "current": (
            "european_aqi,"
            "pm2_5,"
            "pm10,"
            "nitrogen_dioxide,"
            "ozone"
        ),

        "hourly": (
            "european_aqi,"
            "pm2_5,"
            "pm10,"
            "nitrogen_dioxide,"
            "ozone"
        ),

        "past_hours": 24,
        "forecast_hours": 0,
        "timezone": "Europe/Belgrade"
    }

    response = requests.get(
        AIR_QUALITY_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        data = [data]

    rows = []

    for municipality, location in zip(
        municipalities,
        data
    ):

        current = location.get(
            "current",
            {}
        )

        hourly = location.get(
            "hourly",
            {}
        )

        def average(values):

            clean_values = [
                value
                for value in values
                if value is not None
            ]

            if not clean_values:
                return None

            return (
                sum(clean_values)
                / len(clean_values)
            )

        rows.append({
            "Municipality":
                municipality,

            "Latitude":
                MUNICIPALITY_COORDINATES[
                    municipality
                ][0],

            "Longitude":
                MUNICIPALITY_COORDINATES[
                    municipality
                ][1],

            "CurrentAQI":
                current.get(
                    "european_aqi"
                ),

            "AQI24h":
                average(
                    hourly.get(
                        "european_aqi",
                        []
                    )
                ),

            "PM2_5_24h":
                average(
                    hourly.get(
                        "pm2_5",
                        []
                    )
                ),

            "PM10_24h":
                average(
                    hourly.get(
                        "pm10",
                        []
                    )
                ),

            "NO2_24h":
                average(
                    hourly.get(
                        "nitrogen_dioxide",
                        []
                    )
                ),

            "O3_24h":
                average(
                    hourly.get(
                        "ozone",
                        []
                    )
                )
        })

    df = pd.DataFrame(rows)

    return df


# ============================================================
# Municipality normalization
# ============================================================

def normalize_municipalities(df):
    """
    Normalizes municipality names across all datasets.
    Removes national totals.
    """

    df = df.copy()

    df["Municipality"] = (
        df["Municipality"]
        .apply(
            normalize_municipality_name
        )
    )

    df = df[
        df["Municipality"].notna()
    ]

    return df.reset_index(drop=True)


# ============================================================
# Master Municipality Dataset
# ============================================================

def load_master_data():
    """
    Loads and merges all five project data sources.

    Sources:
    1. Population
    2. Employment
    3. Education
    4. Settlements
    5. Air Quality

    Returns:
        pd.DataFrame
    """

    # --------------------------------------------------------
    # 1. Population
    # --------------------------------------------------------

    population = load_population_data()

    population = normalize_municipalities(
        population
    )

    population = population[
        population["Year"] == 2024
    ][
        [
            "Municipality",
            "Population"
        ]
    ].copy()

    population = population.rename(
        columns={
            "Population": "Population2024"
        }
    )

    # --------------------------------------------------------
    # 2. Employment
    # --------------------------------------------------------

    employment = load_employment_data()

    employment = normalize_municipalities(
        employment
    )

    # --------------------------------------------------------
    # 3. Education
    # --------------------------------------------------------

    education = load_education_data()

    education = normalize_municipalities(
        education
    )

    # --------------------------------------------------------
    # 4. Settlements
    # --------------------------------------------------------

    settlements = load_settlements_data()

    settlements = normalize_municipalities(
        settlements
    )

    # --------------------------------------------------------
    # 5. Air Quality
    # --------------------------------------------------------

    air_quality = load_air_quality_data()

    air_quality = normalize_municipalities(
        air_quality
    )

    # --------------------------------------------------------
    # Merge
    # --------------------------------------------------------

    master = population.merge(
        employment,
        on="Municipality",
        how="outer",
        validate="one_to_one"
    )

    master = master.merge(
        education,
        on="Municipality",
        how="outer",
        validate="one_to_one"
    )

    master = master.merge(
        settlements,
        on="Municipality",
        how="outer",
        validate="one_to_one"
    )

    master = master.merge(
        air_quality,
        on="Municipality",
        how="outer",
        validate="one_to_one"
    )

    # --------------------------------------------------------
    # Derived indicators
    # --------------------------------------------------------

    master["EmployedPer1000"] = (
        master["Employed"]
        / master["Population2024"]
        * 1000
    )

    master["PopulationPerSettlement"] = (
        master["Population2024"]
        / master["Settlements"]
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    master = master.sort_values(
        "Municipality"
    ).reset_index(drop=True)

    return master