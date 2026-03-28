def generate_advice(analysis):
    advice = []
    for k, v in analysis.items():
        if v == "Overspending":
            advice.append(f"Reduce spending in {k}")
    if not advice:
        advice.append("Excellent financial discipline!")
    return advice
