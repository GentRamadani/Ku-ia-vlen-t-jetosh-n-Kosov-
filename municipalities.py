MUNICIPALITY_COORDINATES = {
    "Deçan": (42.5402, 20.2879),
    "Gjakovë": (42.3803, 20.4308),
    "Gllogoc": (42.6283, 20.8939),
    "Gjilan": (42.4605, 21.4694),
    "Dragash": (42.0265, 20.6533),
    "Istog": (42.7808, 20.4875),
    "Kaçanik": (42.2317, 21.2594),
    "Klinë": (42.6217, 20.5778),
    "Fushë Kosovë": (42.6394, 21.0961),
    "Kamenicë": (42.5781, 21.5803),
    "Mitrovicë": (42.8833, 20.8667),
    "Leposaviq": (43.1039, 20.8028),
    "Lipjan": (42.5217, 21.1258),
    "Novobërdë": (42.6159, 21.4340),
    "Obiliq": (42.6869, 21.0703),
    "Rahovec": (42.3994, 20.6547),
    "Pejë": (42.6591, 20.2883),
    "Podujevë": (42.9106, 21.1931),
    "Prishtinë": (42.6629, 21.1655),
    "Prizren": (42.2139, 20.7397),
    "Skënderaj": (42.7467, 20.7886),
    "Shtime": (42.4331, 21.0397),
    "Shtërpcë": (42.2390, 21.0276),
    "Suharekë": (42.3583, 20.8250),
    "Ferizaj": (42.3702, 21.1483),
    "Viti": (42.3214, 21.3583),
    "Vushtrri": (42.8231, 20.9675),
    "Zubin Potok": (42.9144, 20.6897),
    "Zveçan": (42.9075, 20.8403),
    "Malishevë": (42.4822, 20.7458),
    "Junik": (42.4758, 20.2772),
    "Mamushë": (42.3308, 20.7269),
    "Hani i Elezit": (42.1507, 21.2969),
    "Graçanicë": (42.6011, 21.1958),
    "Ranillug": (42.4922, 21.5989),
    "Partesh": (42.4014, 21.4336),
    "Kllokot": (42.3714, 21.3744),
    "Mitrovicë Veriore": (42.8950, 20.8650),
}


# ============================================================
# Municipality name normalization
# ============================================================

MUNICIPALITY_ALIASES = {
    # Gllogoc
    "Gllogovc": "Gllogoc",

    # Skenderaj
    "Sknderaj": "Skënderaj",
    "Skenderaj": "Skënderaj",

    # Zvecan
    "Zveqan": "Zveçan",

    # Ranillug
    "Ranilug": "Ranillug",

    # North Mitrovica
    "Mitrovica e V.": "Mitrovicë Veriore",
    "Mitrovica Veriore": "Mitrovicë Veriore",
    "Mitrovica e Veriut": "Mitrovicë Veriore",

    # National totals - these are not municipalities
    "Kosova": None,
    "Kosovë": None,
    "Gjithsej": None,
    "Total": None,
}


def normalize_municipality_name(name):
    """
    Converts different ASKdata municipality spellings
    into one canonical municipality name.
    """

    if name is None:
        return None

    name = str(name).strip()

    return MUNICIPALITY_ALIASES.get(
        name,
        name
    )