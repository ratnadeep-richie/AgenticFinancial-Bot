def validate_profile(state, city, occupation, salary):
    return all([state, city, occupation]) and salary > 0
