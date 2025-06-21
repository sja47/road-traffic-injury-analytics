import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# --- Password Protection ---
st.markdown("<h2 style='text-align: center;'>🔐 Secure Access</h2>", unsafe_allow_html=True)
password = st.text_input("Enter password to access the dashboard:", type="password")
if password != "msba":
    st.warning("🔒 Please enter the correct password to continue.")
    st.stop()

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🚦 Road Traffic Injury Analytics Dashboard</h1>", unsafe_allow_html=True)

# --- Load Data ---
CSV_URL = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"
try:
    df = pd.read_csv(CSV_URL)
except Exception as e:
    st.error(f"❌ Failed to load data. Please check the CSV URL.\n\n{e}")
    st.stop()

# --- Layout Grid 2x2 ---
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# --- 1. Avg by Gender ---
with row1_col1:
    st.subheader("1. Avg Death & Injury Rates by Gender")
    gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean()
    fig1, ax1 = plt.subplots(figsize=(3, 2))
    gender_avg.plot(kind="bar", stacked=True, ax=ax1, color=["skyblue", "navy"], legend=False)
    ax1.set_ylabel("Rate per 100k", fontsize=8)
    ax1.set_xlabel("Gender", fontsize=8)
    ax1.tick_params(axis='both', labelsize=7)
    fig1.tight_layout()
    st.pyplot(fig1, use_container_width=True)

# --- 2. Yearly Trends ---
with row1_col2:
    st.subheader("2. Yearly Trends in Death & Injury Rates")
    yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(3, 2))
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', color='red', label="Death Rate")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', color='blue', label="Injury Rate")
    ax2.set_ylabel("Rate per 100k", fontsize=8)
    ax2.set_xlabel("Year", fontsize=8)
    ax2.tick_params(axis='both', labelsize=7)
    ax2.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False, fontsize=7)
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)

# --- 3. Vehicle Types ---
with row2_col1:
    st.subheader("3. Vehicle Type Distribution")
    vehicle_counts = df["Vehicle_Type"].value_counts()
    fig3, ax3 = plt.subplots(figsize=(3, 2))
    vehicle_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax3, colors=sns.color_palette("pastel"), textprops={'fontsize': 7})
    ax3.set_ylabel("")
    fig3.tight_layout()
    st.pyplot(fig3, use_container_width=True)

# --- 4. Age × Gender ---
with row2_col2:
    st.subheader("4. Death & Injury Rates by Age × Gender")
    age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()
    fig4, ax4 = plt.subplots(figsize=(3, 2))
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.8, color=["red", "green", "skyblue", "orange"])
    ax4.set_ylabel("Rate per 100k", fontsize=8)
    ax4.set_xlabel("Age Group", fontsize=8)
    ax4.tick_params(axis='both', labelsize=7)
    ax4.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False, fontsize=7)
    fig4.tight_layout()
    st.pyplot(fig4, use_container_width=True)
