with col4:
    st.markdown("**4. Age × Gender Injury/Death Rates**")
    fig4, ax4 = plt.subplots(figsize=(6.0, 5.5), dpi=120)
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.6)

    ax4.set_ylabel("Rate per 100k", fontsize=12)
    ax4.set_xlabel("Age Group", fontsize=12)
    ax4.tick_params(axis='x', labelsize=10, rotation=30)
    ax4.tick_params(axis='y', labelsize=10)

    handles, labels = ax4.get_legend_handles_labels()
    simplified_labels = [
        label.replace("Death_Rate_per_100k", "Death").replace("Injury_Rate_per_100k", "Injury")
        for label in labels
    ]
    ax4.legend(handles, simplified_labels, fontsize=10, loc="center left", bbox_to_anchor=(1, 0.5))
    fig4.tight_layout(pad=0.8)
    st.pyplot(fig4)
