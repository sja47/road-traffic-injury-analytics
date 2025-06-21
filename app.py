import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Road Traffic Injury Analytics Dashboard")

# Load data
df = pd.read_csv("road_traffic_injuries_sample.csv")

# Overview
st.header("1. Dataset Overview")
st.write(df.head())

# Gender analysis
st.header("2. Average Death & Injury Rates by Gender")
gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean()
st.bar_chart(gender_avg)

# Yearly trend
st.header("3. Yearly Trends in Death & Injury Rates")
yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=yearly_avg, x="Year", y="Death_Rate_per_100k", marker="o", label="Death Rate", ax=ax)
sns.lineplot(data=yearly_avg, x="Year", y="Injury_Rate_per_100k", marker="o", label="Injury Rate", ax=ax)
ax.set_ylabel("Rate per 100,000")
ax.set_title("Average Death & Injury Rates Over Years")
ax.legend()
st.pyplot(fig)

# Vehicle type pie chart
st.header("4. Distribution by Vehicle Type")
vehicle_counts = df["Vehicle_Type"].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(vehicle_counts, labels=vehicle_counts.index, autopct="%1.1f%%", startangle=90)
ax2.axis("equal")
st.pyplot(fig2)

# Age group + Gender analysis
st.header("5. Age Group and Gender Analysis")
group_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=group_avg,
    x="Age_Group",
    y="Death_Rate_per_100k",
    hue="Gender",
    ax=ax3
)
ax3.set_title("Death Rate by Age Group and Gender")
ax3.set_ylabel("Rate per 100,000")
st.pyplot(fig3)

# Footer
st.markdown("---")
st.markdown("Developed by **sja47** – Healthcare Analytics Project (MSBA)")
