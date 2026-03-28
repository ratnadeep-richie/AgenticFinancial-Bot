import numpy as np

def detect_category_anomalies(history, current_expenses):
    anomalies = []
    if len(history) < 2:
        return anomalies

    for k in current_expenses:
        past = [h["expenses"].get(k, 0) for h in history[:-1]]
        if len(past) < 2:
            continue

        mean = np.mean(past)
        std = np.std(past)
        if std == 0:
            continue

        z = (current_expenses[k] - mean) / std
        if abs(z) > 2:
            anomalies.append(f"Unusual spike in {k}")

    return anomalies
