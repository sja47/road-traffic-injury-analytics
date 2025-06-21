import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PASSWORD PROTECTION
# ---------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "YourSecurePassword":
            st.session_state["authenticated"] = True
        else:
            st.error("❌ Wrong password")
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.text_input("🔐 Enter password to access the dashboard:", type="password", on_change=password_entered, key="password")
        st.stop()

check_password()

# ---------------------------
# AUTO-LOAD DATA FROM GITHUB (Raw URL)
# ---------------------------
CSV_URL = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"

try:
    df = pd.read_csv(CSV_URL)
except Exception as e:
    st.error("❌ Failed to load data from GitHub. Please check the URL.")
    st.stop()

# ---------------------------
# OPTIONAL UPLOAD (disabled view only)
# ---------------------------
st.file_uploader("📂 Upload your CSV file (optional, already loaded)", type="csv", disabled=True)

# ---------------------------
# TITLE
# ---------------------------
st.title("🚦 Road Traffic Injury Analytics Dashboard")

# ---------------------------
# DATA PREPARATION
# ---------------------------
gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = df["Vehicle_Type"].value_counts()
age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# ---------------------------
# VISUALS IN 2x2 LAYOUT
# ---------------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("**1. Avg Death & Injury Rates by Gender**")
    fig1, ax1 = plt.subplots()
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["#add8e6", "#1f77b4"], legend=False)
    ax1.set_ylabel("Rate per 100k")
    ax1.set_xlabel("")
    st.pyplot(fig1, use_container_width=True)

with row1_col2:
    st.markdown("**2. Yearly Trends in Death & Injury Rates**")
    fig2, ax2 = plt.subplots()
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], label="Death Rate", color="crimson", marker='o')
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], label="Injury Rate", color="navy", marker='o')
    ax2.set_ylabel("Rate per 100k")
    ax2.legend(loc="upper right", frameon=False)
    st.pyplot(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("**3. Vehicle Type Distribution**")
    fig3, ax3 = plt.subplots()
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
    ax3.axis('equal')
    st.pyplot(fig3, use_container_width=True)

with row2_col2:
    st.markdown("**4. Death & Injury Rates by Age × Gender**")
    fig4, ax4 = plt.subplots()
    age_gender_avg.plot(kind="bar", ax=ax4)
    ax4.set_ylabel("Rate per 100k")
    ax4.set_xlabel("Age Group")
    ax4.legend(loc="upper right", frameon=False)
    st.pyplot(fig4, use_container_width=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("© 2025 | Road Safety Analytics | MSBA Healthcare Analytics")
