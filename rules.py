TIER_RULES = {
    "Tier 1": {"rent": 0.45, "food": 0.25, "travel": 0.15, "entertainment": 0.10},
    "Tier 2": {"rent": 0.35, "food": 0.22, "travel": 0.15, "entertainment": 0.10},
    "Tier 3": {"rent": 0.25, "food": 0.20, "travel": 0.12, "entertainment": 0.08},
}

CITY_TIER_MAP = {
    "Mumbai": "Tier 1",
    "Delhi": "Tier 1",
    "Bangalore": "Tier 1",
    "Chennai": "Tier 1",
    "Hyderabad": "Tier 1",
    "Kolkata": "Tier 1",
    "Pune": "Tier 1",
    "Ahmedabad": "Tier 2",
}

def get_city_rules(city):
    tier = CITY_TIER_MAP.get(city, "Tier 3")
    return TIER_RULES[tier]
