import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PASSWORD PROTECTION
# ---------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "MSBA":
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
# LOAD DATA DIRECTLY FROM GITHUB
# ---------------------------
CSV_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"

try:
    df = pd.read_csv(CSV_URL)
except Exception as e:
    st.error(f"❌ Failed to load data. Please check the CSV URL.\n\n{e}")
    st.stop()

# ---------------------------
# TITLE BELOW SOURCE
# ---------------------------
st.markdown("<h1 style='text-align: center;'>🚦 Road Traffic Injury Analytics Dashboard</h1>", unsafe_allow_html=True)

# ---------------------------
# DATA PREP
# ---------------------------
gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = df["Vehicle_Type"].value_counts()
age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# ------------------ ROW 1 -------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("### 1. Avg Death & Injury Rates by Gender")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["#A6CEE3", "#1F78B4"], legend=False)
    ax1.set_ylabel("Rate per 100k")
    ax1.set_xlabel("")
    st.pyplot(fig1, use_container_width=True)

with row1_col2:
    st.markdown("### 2. Yearly Trends in Death & Injury Rates")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', label="Death Rate", color="#FF9999")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', label="Injury Rate", color="#66B3FF")
    ax2.set_ylabel("Rate per 100k")
    ax2.set_xlabel("Year")
    ax2.legend(loc="upper right", frameon=False)
    st.pyplot(fig2, use_container_width=True)

# ------------------ ROW 2 -------------------
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("### 3. Vehicle Type Distribution")
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    colors = ["#FDBF6F", "#CAB2D6", "#B2DF8A", "#FB9A99", "#FFED6F"]
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax3.axis('equal')
    st.pyplot(fig3, use_container_width=True)

with row2_col2:
    st.markdown("### 4. Death & Injury Rates by Age Group and Gender")
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.75, rot=0, colormap="Set1", legend=False)
    ax4.set_ylabel("Rate per 100k")
    ax4.set_xlabel("Age Group")
    st.pyplot(fig4, use_container_width=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("© 2025 | Road Safety Analytics | MSBA Healthcare Analytics")
