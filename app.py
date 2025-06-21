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
    st.error("❌ Failed to load data. Please check the CSV URL.")
    st.stop()

# ---------------------------
# HEADER
# ---------------------------
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
# 2x2 VISUAL LAYOUT
# ---------------------------
col1, col2 = st.columns(2)

# --- Chart 1 ---
with col1:
    st.markdown("**1. Avg Death & Injury Rates by Gender**")
    fig1, ax1 = plt.subplots(figsize=(2.8, 2.4), dpi=120)
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["skyblue", "navy"])
    ax1.set_ylabel("Rate per 100k", fontsize=8)
    ax1.set_xlabel("")
    ax1.tick_params(axis='x', labelsize=7)
    ax1.tick_params(axis='y', labelsize=7)
    ax1.legend(["Injury", "Death"], fontsize=6, loc='upper right', bbox_to_anchor=(1.0, 1.0))
    fig1.tight_layout()
    st.pyplot(fig1, clear_figure=True)

# --- Chart 2 ---
with col2:
    st.markdown("**2. Yearly Death & Injury Trends**")
    fig2, ax2 = plt.subplots(figsize=(2.8, 2.4), dpi=120)
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', color='red', label="Death Rate")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', color='blue', label="Injury Rate")
    ax2.set_ylabel("Rate per 100k", fontsize=8)
    ax2.set_xlabel("Year", fontsize=8)
    ax2.tick_params(axis='x', labelsize=7)
    ax2.tick_params(axis='y', labelsize=7)
    ax2.legend(fontsize=6, loc='upper right')
    fig2.tight_layout()
    st.pyplot(fig2, clear_figure=True)

col3, col4 = st.columns(2)

# --- Chart 3 ---
with col3:
    st.markdown("**3. Vehicle Type Distribution**")
    fig3, ax3 = plt.subplots(figsize=(2.8, 2.4), dpi=120)
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 6})
    ax3.axis('equal')
    fig3.tight_layout()
    st.pyplot(fig3, clear_figure=True)

# --- Chart 4 ---
with col4:
    st.markdown("**4. Death & Injury Rates by Age × Gender**")
    fig4, ax4 = plt.subplots(figsize=(2.8, 2.4), dpi=120)
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.7)
    ax4.set_ylabel("Rate per 100k", fontsize=8)
    ax4.set_xlabel("Age Group", fontsize=8)
    ax4.tick_params(axis='x', labelsize=7)
    ax4.tick_params(axis='y', labelsize=7)
    ax4.legend(fontsize=6, loc="upper right", bbox_to_anchor=(1.2, 1))
    fig4.tight_layout()
    st.pyplot(fig4, clear_figure=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("<div style='text-align: center; font-size: small;'>© 2025 | Road Safety Analytics | MSBA Healthcare Analytics</div>", unsafe_allow_html=True)
