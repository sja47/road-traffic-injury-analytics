import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# 1. PASSWORD PROTECTION
# --------------------------
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

# --------------------------
# 2. LOAD DATA FROM GITHUB
# --------------------------
csv_url = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"
try:
    df = pd.read_csv(csv_url)
except Exception:
    st.error("❌ Failed to load data. Please check the CSV URL.")
    st.stop()

# --------------------------
# 3. PAGE CONFIG + HEADER
# --------------------------
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🚦 Road Traffic Injury Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --------------------------
# 4. DATA PREP
# --------------------------
gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = df["Vehicle_Type"].value_counts()
age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# --------------------------
# 5. COMPACT 2x2 DASHBOARD
# --------------------------
figsize = (3, 2.2)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Avg Death & Injury Rates by Gender")
    fig1, ax1 = plt.subplots(figsize=figsize)
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["skyblue", "navy"], legend=False)
    ax1.set_ylabel("Rate per 100k", fontsize=8)
    ax1.tick_params(axis='both', labelsize=6)
    st.pyplot(fig1, use_container_width=True)
    st.caption("Legend: Death (navy), Injury (skyblue)")

with col2:
    st.subheader("2. Yearly Trends in Death & Injury Rates")
    fig2, ax2 = plt.subplots(figsize=figsize)
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', color='red', label="Death Rate")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', color='blue', label="Injury Rate")
    ax2.set_ylabel("Rate per 100k", fontsize=8)
    ax2.set_xlabel("Year", fontsize=8)
    ax2.tick_params(axis='both', labelsize=6)
    ax2.legend(fontsize=6, loc='center left', bbox_to_anchor=(1, 0.5))
    st.pyplot(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Vehicle Type Distribution")
    fig3, ax3 = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax3.pie(vehicle_counts, labels=None, autopct='%1.1f%%', startangle=90,
                                       colors=plt.cm.Paired.colors, textprops={'fontsize': 6})
    ax3.axis('equal')
    ax3.legend(vehicle_counts.index, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=6)
    st.pyplot(fig3, use_container_width=True)

with col4:
    st.subheader("4. Death & Injury Rates by Age × Gender")
    fig4, ax4 = plt.subplots(figsize=figsize)
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.7, legend=False)
    ax4.set_ylabel("Rate per 100k", fontsize=8)
    ax4.set_xlabel("Age Group", fontsize=8)
    ax4.tick_params(axis='both', labelsize=6)
    st.pyplot(fig4, use_container_width=True)
    st.caption("Legend shown separately")

# --------------------------
# 6. FOOTER
# --------------------------
st.markdown("---")
st.markdown("<div style='text-align: center;'>© 2025 | Road Safety Analytics | MSBA Healthcare Analytics</div>", unsafe_allow_html=True)
