import streamlit as st
import matplotlib.pyplot as plt


def show_achievement(achievements):
    levels = list(achievements.keys())
    achievement_values_raw = list(achievements.values())
    achievement_values = []
    for item in achievement_values_raw:
        achievement_values.append(item*100)

    chart_type = st.selectbox('Select Chart Type', ['Bar Chart', 'Line Chart'])
    max_achievement = max(achievement_values)
    fig, ax = plt.subplots(figsize=(6, 4))

    if chart_type == 'Bar Chart':
        ax.bar(levels, achievement_values, color='skyblue')
        plt.xlabel('Levels')
        plt.ylabel('Achievement (%)')
        plt.title('Achievement by Level')
        ax.set_ylim(0, max_achievement*1.2)  # Set y-axis to show scale from 0 to 1
    elif chart_type == 'Line Chart':
        ax.plot(levels, achievement_values, marker='o', linestyle='-', color='deepskyblue')
        plt.xlabel('Levels')
        plt.ylabel('Achievement (%)')
        plt.title('Achievement by Level')
        ax.set_ylim(0, max_achievement*1.2)  # Set y-axis to show scale from 0 to 1
        plt.grid(True)

    # Use Streamlit to render the figure
    st.pyplot(fig)

def show_rank(ranking_list):
    # Create a figure for the histogram
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(ranking_list, bins=range(1, 101, 10), edgecolor='black')  # Bins represent intervals of 10

    ax.set_title('Distribution of Rankings')
    ax.set_xlabel('Rankings (1-100)')
    ax.set_ylabel('Frequency')
    ax.set_xticks(range(0, 101, 10))  # Adjust the x-ticks for better visualization

    # Display the plot in Streamlit
    st.pyplot(fig)

def show_scatterplot(ranks_by_level):
    # Create a figure for the scatter plot
    fig, ax = plt.subplots(figsize=(6, 4))
    noise_strength = 0.2
    for category, values in ranks_by_level.items():
        categories = []
        for i in range(len(values)):
            categories.append(category + rd.uniform(-noise_strength, noise_strength))
        ax.scatter(categories, values, label=category, s=20)

    ax.set_title('Ranking by Level')
    ax.set_xlabel('Level')
    ax.set_ylabel('Rank')
    ax.legend(title='Levels', loc='upper right', bbox_to_anchor=(1.3, 1))
    # Display the plot in Streamlit
    st.pyplot(fig)

