from datetime import datetime, timedelta

def run_proactive_checks(income, expenses, ideal, bills):
    alerts = []

    for k in expenses:
        if expenses[k] > ideal[k]:
            alerts.append(f"Budget exceeded in {k}")

    savings = income - sum(expenses.values())
    if savings / income < 0.2:
        alerts.append("Savings below 20% threshold")

    today = datetime.today().date()

    for bill in bills:
        reminder = bill["due_date"] - timedelta(days=2)
        if today == reminder:
            alerts.append(f"{bill['name']} due in 2 days")

    return alerts
