import pandas as pd

def excel_to_json(file):
    df = pd.read_excel(file)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.strip()
    )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    transactions = df.to_dict(orient="records")

    expenses = {"rent": 0, "food": 0, "travel": 0, "entertainment": 0}

    for tx in transactions:
        if tx["amount"] >= 0:
            continue
        tag = str(tx.get("tags", "")).lower()
        value = abs(tx["amount"])

        if "rent" in tag:
            expenses["rent"] += value
        elif "food" in tag:
            expenses["food"] += value
        elif "travel" in tag:
            expenses["travel"] += value
        elif "entertainment" in tag:
            expenses["entertainment"] += value

    return {"transactions": transactions, "expenses": expenses}
