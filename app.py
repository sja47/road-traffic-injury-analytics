import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PASSWORD PROTECTION
# ---------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "msba":
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
# LOAD DATA FROM GITHUB
# ---------------------------
csv_url = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"

try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"❌ Failed to load data. Error: {e}")
    st.stop()

# ---------------------------
# HEADER
# ---------------------------
st.markdown("---")
st.markdown("<h1 style='text-align: center;'>🚦 Road Traffic Injury Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------------
# DATA AGGREGATION
# ---------------------------
gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = df["Vehicle_Type"].value_counts()
age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# ---------------------------
# VISUALIZATIONS (2x2 layout with tighter figures)
# ---------------------------
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Chart 1: Avg by Gender
with row1_col1:
    st.subheader("1. Death & Injury Rates by Gender")
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["#91c4f2", "#4169e1"])
    ax1.set_ylabel("Rate per 100k")
    ax1.set_xlabel("")
    ax1.legend(loc="upper right", bbox_to_anchor=(1.2, 1))
    st.pyplot(fig1)

# Chart 2: Yearly Trends
with row1_col2:
    st.subheader("2. Yearly Death & Injury Trends")
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', color='crimson', label="Death Rate")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', color='navy', label="Injury Rate")
    ax2.set_ylabel("Rate per 100k")
    ax2.set_xlabel("Year")
    ax2.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig2)

# Chart 3: Vehicle Type Distribution
with row2_col1:
    st.subheader("3. Vehicle Type Distribution")
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 8})
    ax3.axis("equal")
    st.pyplot(fig3)

# Chart 4: Age × Gender Rates
with row2_col2:
    st.subheader("4. Age & Gender-based Rates")
    fig4, ax4 = plt.subplots(figsize=(4, 3))
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.8)
    ax4.set_ylabel("Rate per 100k")
    ax4.set_xlabel("Age Group")
    ax4.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig4)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("<div style='text-align: center;'>© 2025 | Road Safety Analytics | MSBA Healthcare Analytics</div>", unsafe_allow_html=True)
