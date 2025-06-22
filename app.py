import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Password protection
password = st.text_input("Enter Password:", type="password")
if password != "msba":
    st.warning("Please enter the correct password to view the dashboard.")
    st.stop()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("your_data.csv")  # Replace with your actual file
    return df

df = load_data()

# Dropdown filters
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    selected_gender = st.selectbox("Select Gender", ["All"] + sorted(df["Gender"].dropna().unique().tolist()))
with col_filter2:
    selected_year = st.selectbox("Select Year", ["All"] + sorted(df["Year"].dropna().unique().tolist()))

# Apply filters
filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]

# Pre-aggregate data
avg_gender = filtered_df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean()
yearly = filtered_df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean()
vehicle = filtered_df["Vehicle_Type"].value_counts(normalize=True)
age_gender_avg = filtered_df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# Row 1
col1, col2 = st.columns(2)
with col1:
    st.write("**1. Avg Death & Injury by Gender**")
    fig1, ax1 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    avg_gender.plot(kind="bar", stacked=True, color=["skyblue", "navy"], ax=ax1, width=0.6)
    ax1.set_ylabel("Rate per 100k", fontsize=6)
    ax1.tick_params(axis="x", labelsize=6)
    ax1.tick_params(axis="y", labelsize=6)
    ax1.legend(["Injury", "Death"], fontsize=5, loc="upper right")
    fig1.tight_layout(pad=0.5)
    st.pyplot(fig1)

with col2:
    st.write("**2. Yearly Death & Injury Trends**")
    fig2, ax2 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    ax2.plot(yearly.index, yearly["Death_Rate_per_100k"], marker="o", color="red", label="Death")
    ax2.plot(yearly.index, yearly["Injury_Rate_per_100k"], marker="o", color="blue", label="Injury")
    ax2.set_ylabel("Rate per 100k", fontsize=6)
    ax2.set_xlabel("Year", fontsize=6)
    ax2.tick_params(axis="x", labelsize=6)
    ax2.tick_params(axis="y", labelsize=6)
    ax2.legend(fontsize=5)
    fig2.tight_layout(pad=0.5)
    st.pyplot(fig2)

# Row 2
col3, col4 = st.columns(2)
with col3:
    st.write("**3. Vehicle Type Distribution**")
    fig3, ax3 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    ax3.pie(vehicle, labels=vehicle.index, autopct="%1.1f%%", textprops={"fontsize": 6})
    fig3.tight_layout()
    st.pyplot(fig3)

with col4:
    st.write("**4. Age × Gender Injury/Death Rates**")
    fig4, ax4 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.6)
    ax4.set_ylabel("Rate per 100k", fontsize=6)
    ax4.set_xlabel("Age Group", fontsize=6)
    ax4.tick_params(axis='x', labelsize=5, rotation=30)
    ax4.tick_params(axis='y', labelsize=5)
    ax4.legend(
        fontsize=5,
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        borderaxespad=0.
    )
    fig4.tight_layout(pad=0.5)
    st.pyplot(fig4)
