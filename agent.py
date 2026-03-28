from analyzer import analyze_expenses
from recommender import generate_advice

class ExpenseAgent:
    def run(self, user_data):
        ideal, analysis = analyze_expenses(user_data)
        advice = generate_advice(analysis)
        return ideal, analysis, advice
