from rules import get_city_rules

def analyze_expenses(data):
    income = data["income"]
    city = data["city"]
    rules = get_city_rules(city)

    ideal = {
        "rent": income * rules["rent"],
        "food": income * rules["food"],
        "travel": income * rules["travel"],
        "entertainment": income * rules["entertainment"]
    }

    analysis = {}
    for k in ideal:
        analysis[k] = "OK" if data.get(k, 0) <= ideal[k] else "Overspending"

    return ideal, analysis
