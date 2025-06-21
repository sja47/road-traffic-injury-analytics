import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------
# PASSWORD PROTECTION
# ------------------------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "MSBA":  # ← CHANGE THIS
            st.session_state["authenticated"] = True
        else:
            st.error("❌ Incorrect password")
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        st.stop()

check_password()

# ------------------------------------------
# APP TITLE
# ------------------------------------------
st.title("🚦 Road Traffic Injury Analytics Dashboard")

# ------------------------------------------
# CSV UPLOAD
# ------------------------------------------
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])
if uploaded_file is None:
    st.warning("Please upload a CSV file to proceed.")
    st.stop()

df = pd.read_csv(uploaded_file)

# ------------------------------------------
# DATA OVERVIEW
# ------------------------------------------
st.header("1. Dataset Overview")
st.dataframe(df.head())

# ------------------------------------------
# VISUALS LAYOUT
# ------------------------------------------
col1, col2 = st.columns(2)

# -- 1. Average Death & Injury Rates by Gender
with col1:
    st.subheader("2. Avg Death & Injury by Gender")
    gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()

    fig1, ax1 = plt.subplots()
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["skyblue", "blue"])
    ax1.set_ylabel("Rate per 100,000")
    ax1.set_title("Avg Death & Injury Rates by Gender")
    st.pyplot(fig1)

# -- 2. Yearly Trends in Death & Injury Rates
with col2:
    st.subheader("3. Yearly Trends in Death & Injury")
    yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()

    fig2, ax2 = plt.subplots()
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', label='Death Rate')
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', label='Injury Rate')
    ax2.set_ylabel("Rate per 100,000")
    ax2.set_title("Yearly Death & Injury Trends")
    ax2.legend()
    st.pyplot(fig2)

# -- 3. Distribution by Vehicle Type
with col1:
    st.subheader("4. Distribution by Vehicle Type")
    vehicle_counts = df["Vehicle_Type"].value_counts()

    fig3, ax3 = plt.subplots()
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct="%1.1f%%", startangle=140)
    ax3.set_title("Vehicle Type Distribution")
    st.pyplot(fig3)

# -- 4. Avg Rates by Age Group & Gender
with col2:
    st.subheader("5. Avg Death & Injury by Age Group & Gender")
    age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

    fig4, ax4 = plt.subplots()
    age_gender_avg.plot(kind="bar", ax=ax4)
    ax4.set_ylabel("Rate per 100,000")
    ax4.set_title("Death & Injury Rates by Age & Gender")
    st.pyplot(fig4)

# ------------------------------------------
# END OF APP
# ------------------------------------------
st.markdown("© 2025 | Road Safety Analytics | MSBA Project")
