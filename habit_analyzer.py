from collections import Counter

def detect_spending_habits(transactions, threshold=5):
    counter = Counter()

    for tx in transactions:
        if tx["amount"] < 0:
            merchant = str(tx.get("transaction_details", ""))
            counter[merchant] += 1

    return [f"Habit detected at {m} ({c} times)" for m, c in counter.items() if c >= threshold]
