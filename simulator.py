def simulate_sip(current_sip, extra_sip, annual_return, years, inflation):
    total = current_sip + extra_sip
    r = annual_return / 12 / 100
    n = years * 12

    fv = total * (((1 + r) ** n - 1) / r) * (1 + r)
    real = fv / ((1 + inflation / 100) ** years)

    return round(fv, 2), round(real, 2)
