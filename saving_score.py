def calculate_savings_score(income, expenses, analysis):
    total = sum(expenses.values())
    savings = income - total
    ratio = savings / income

    score = 100
    if ratio < 0.1:
        score -= 40
    elif ratio < 0.2:
        score -= 20

    for v in analysis.values():
        if v == "Overspending":
            score -= 10

    return max(score, 0)
