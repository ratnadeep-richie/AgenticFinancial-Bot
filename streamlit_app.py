import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

from auth import authenticate_user, register_user
from validators import valid_name, valid_username, valid_email, valid_phone
from excel_parser import excel_to_json
from agent import ExpenseAgent
from simulator import simulate_sip
from rules import get_city_rules
from data_store import (
    save_profile,
    load_profile,
    save_month,
    load_history,
    save_alert,
    load_alerts
)
from report_generator import generate_financial_report


st.set_page_config(page_title="Agentic Financial AI", layout="wide")


# ================= SESSION INIT =================
if "auth" not in st.session_state:
    st.session_state.auth = False


# ================= AUTH SECTION =================
if not st.session_state.auth:

    st.title("🔐 Agentic Financial AI")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN
    with tab1:
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_btn"):
            ok, name = authenticate_user(login_user, login_pass)
            if ok:
                st.session_state.auth = True
                st.session_state.user = login_user
                st.session_state.name = name
                st.rerun()
            else:
                st.error("Invalid credentials")

    # REGISTER
    with tab2:
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_user = st.text_input("Username (Ex: Deva@1)", key="reg_user")
        reg_email = st.text_input("Email", key="reg_email")
        reg_phone = st.text_input("Phone", key="reg_phone")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register", key="reg_btn"):
            if valid_name(reg_name) and valid_username(reg_user) and valid_email(reg_email) and valid_phone(reg_phone):
                ok, msg = register_user(reg_name, reg_user, reg_email, reg_phone, reg_pass)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.error("Invalid input")

    st.stop()


# ================= SIDEBAR =================
with st.sidebar:
    section = st.selectbox(
        "Navigate",
        ["Dashboard", "Bills", "Notifications", "Simulator"]
    )

    st.write(f"👤 {st.session_state.name}")

    if st.button("Logout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ================= DASHBOARD =================
if section == "Dashboard":

    st.header("📊 Financial Dashboard")

    profile = load_profile(st.session_state.user)

    INDIAN_STATES = sorted([
        "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
        "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand",
        "Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur",
        "Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan",
        "Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh",
        "Uttarakhand","West Bengal","Delhi (NCT)"
    ])

    CITY_OPTIONS = sorted([
        "Mumbai","Delhi","Bangalore","Chennai","Hyderabad",
        "Kolkata","Pune","Ahmedabad","Jaipur","Lucknow",
        "Chandigarh","Indore","Nagpur","Bhopal","Ranchi","Guwahati"
    ])

    # -------- Create Profile --------
    if not profile:
        st.subheader("Create Profile")

        state = st.selectbox("State", INDIAN_STATES)
        city = st.selectbox("City", CITY_OPTIONS)
        occupation = st.selectbox("Occupation", ["Student","Salaried","Freelancer"])
        salary = st.number_input("Monthly Salary (₹)", min_value=1000)

        if st.button("Save Profile"):
            save_profile(st.session_state.user, {
                "state": state,
                "city": city,
                "occupation": occupation,
                "salary": salary
            })
            st.success("Profile Saved")
            st.rerun()

        st.stop()

    # -------- Display Profile --------
    st.subheader("👤 Profile")
    st.json(profile)

    # -------- Edit Profile --------
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    if st.button("✏ Edit Profile"):
        st.session_state.edit_mode = not st.session_state.edit_mode

    if st.session_state.edit_mode:

        state_index = INDIAN_STATES.index(profile["state"]) if profile["state"] in INDIAN_STATES else 0
        city_index = CITY_OPTIONS.index(profile["city"]) if profile["city"] in CITY_OPTIONS else 0
        occ_list = ["Student","Salaried","Freelancer"]
        occ_index = occ_list.index(profile["occupation"]) if profile["occupation"] in occ_list else 0

        edit_state = st.selectbox("State", INDIAN_STATES, index=state_index)
        edit_city = st.selectbox("City", CITY_OPTIONS, index=city_index)
        edit_occ = st.selectbox("Occupation", occ_list, index=occ_index)
        edit_salary = st.number_input("Monthly Salary (₹)", min_value=1000, value=int(profile["salary"]))

        if st.button("Save Changes"):
            save_profile(st.session_state.user, {
                "state": edit_state,
                "city": edit_city,
                "occupation": edit_occ,
                "salary": edit_salary
            })
            st.success("Profile Updated")
            st.session_state.edit_mode = False
            st.rerun()

    st.divider()

    # -------- Expense Upload --------
    file = st.file_uploader("Upload Expense Excel", type=["xlsx"])

    if file:

        parsed = excel_to_json(file)
        expenses = parsed.get("expenses", {})
        transactions = parsed.get("transactions", [])

        agent = ExpenseAgent()

        ideal, analysis, advice = agent.run({
            "city": profile["city"],
            "income": profile["salary"],
            **expenses
        })

        save_month(st.session_state.user, expenses)

        st.subheader("📊 Expense Analysis")
        st.json(analysis)

        fig, ax = plt.subplots(figsize=(6,3))

        categories = list(expenses.keys())
        actual_vals = list(expenses.values())
        ideal_vals = [ideal[k] for k in categories]

        colors = ["red" if actual_vals[i] > ideal_vals[i] else "blue" for i in range(len(categories))]

        ax.bar(categories, actual_vals, color=colors)
        ax.plot(categories, ideal_vals, color="green", marker="o")
        st.pyplot(fig)

        total_spent = sum(actual_vals)
        salary = profile["salary"]
        savings = salary - total_spent
        savings_rate = savings / salary if salary else 0
        score = int((savings_rate * 60) + 40)
        score = max(0, min(score, 100))

        st.metric("💳 Financial Score", f"{score}/100")

        st.subheader("🤖 Advice")
        for a in advice:
            st.success(a)

        st.subheader("📄 Transactions")
        st.dataframe(pd.DataFrame(transactions))


# ================= BILLS =================
if section == "Bills":

    st.header("📅 Recurring Bills")

    os.makedirs("user_data", exist_ok=True)
    path = f"user_data/{st.session_state.user}_bills.json"

    if os.path.exists(path):
        with open(path, "r") as f:
            bills = json.load(f)
    else:
        bills = []

    name = st.text_input("Bill Name")
    amount = st.number_input("Amount (₹)", min_value=0.0)
    due = st.number_input("Due Day (1–31)", min_value=1, max_value=31)

    if st.button("Add Bill"):
        bills.append({"name": name, "amount": amount, "due_day": due})
        with open(path, "w") as f:
            json.dump(bills, f, indent=4)
        st.success("Bill Added")
        st.rerun()

    if bills:
        st.dataframe(bills)
        
        
# ================= NOTIFICATIONS =================
if section == "Notifications":

    st.header("🔔 Notification Center")

    profile = load_profile(st.session_state.user)
    history = load_history(st.session_state.user)

    alerts = []

    if profile and history:

        salary = profile["salary"]
        latest_expenses = history[-1]["expenses"]

        total_spent = sum(latest_expenses.values())
        savings = salary - total_spent if salary else 0
        savings_rate = (savings / salary) if salary else 0

        # 🚨 Low Savings Alert
        if savings_rate < 0.2:
            alerts.append("📉 Savings rate below 20%. Consider reducing discretionary spending.")

        # 🚨 Overspending Alert (City Rules)
        rules = get_city_rules(profile["city"])

        for category, value in latest_expenses.items():
            if category in rules:
                if value > salary * rules[category]:
                    alerts.append(f"🚨 Overspending detected in {category} category.")

    # 📅 Bill Due Reminder
    bill_path = f"user_data/{st.session_state.user}_bills.json"

    if os.path.exists(bill_path):
        with open(bill_path, "r") as f:
            bills = json.load(f)

        today = datetime.now().day

        for bill in bills:
            if bill["due_day"] - today == 2:
                alerts.append(f"📅 Bill '{bill['name']}' due in 2 days.")

    # ========== DISPLAY ALERTS ==========
    if alerts:
        for alert in alerts:
            st.warning(alert)
            save_alert(st.session_state.user, alert, "alert")
    else:
        st.success("✅ No active financial alerts.")

    # ========== ALERT HISTORY ==========
    st.subheader("📜 Alert History")

    past_alerts = load_alerts(st.session_state.user)

    if past_alerts:
        st.dataframe(pd.DataFrame(past_alerts), use_container_width=True)
    else:
        st.info("No past alerts found.")


# ================= SIMULATOR =================
if section == "Simulator":

    st.header("📈 SIP What-If Simulator")

    current = st.number_input("Current SIP", min_value=0)
    extra = st.number_input("Increase SIP By", min_value=0)
    annual = st.slider("Annual Return %", 5, 15, 12)
    years = st.slider("Years", 1, 30, 10)
    inflation = st.slider("Inflation %", 2, 10, 6)

    if st.button("Simulate"):
        nominal, real = simulate_sip(current, extra, annual, years, inflation)
        st.success(f"Nominal Wealth: ₹ {nominal:,}")
        st.info(f"Inflation Adjusted Wealth: ₹ {real:,}")