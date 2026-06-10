import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Smart Study Planner",
    layout="wide"
)

st.title("📚 Smart Study Planner Dashboard")
st.markdown("Plan your studies efficiently!")

st.sidebar.header("Student Profile")

name = st.sidebar.text_input("Student Name")

hours = st.sidebar.slider(
    "Available Study Hours",
    1,
    12,
    6
)

st.header("Enter Subjects")

num_subjects = st.number_input(
    "Number of Subjects",
    min_value=1,
    max_value=10,
    value=4
)

subjects = []
priorities = []

for i in range(num_subjects):

    col1, col2 = st.columns(2)

    with col1:
        subject = st.text_input(
            f"Subject {i+1}",
            key=f"sub{i}"
        )

    with col2:
        priority = st.selectbox(
            f"Priority {i+1}",
            ["High", "Medium", "Low"],
            key=f"pri{i}"
        )

    subjects.append(subject)
    priorities.append(priority)

if st.button("Generate Study Plan"):

    weights = []

    for p in priorities:
        if p == "High":
            weights.append(3)
        elif p == "Medium":
            weights.append(2)
        else:
            weights.append(1)

    total_weight = sum(weights)

    allocated_hours = []

    for w in weights:
        allocated_hours.append(
            round((w / total_weight) * hours, 2)
        )

    plan = pd.DataFrame({
        "Subject": subjects,
        "Priority": priorities,
        "Allocated Hours": allocated_hours
    })

    st.subheader("Generated Timetable")
    st.dataframe(plan)

    productivity = min(
        100,
        int((hours / len(subjects)) * 20)
    )

    st.metric(
        "Productivity Score",
        f"{productivity}%"
    )

    st.subheader("Study Hours Distribution")

    fig, ax = plt.subplots()

    ax.pie(
        allocated_hours,
        labels=subjects,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    st.subheader("Study Tips")

    st.success(
        "Study High Priority subjects first."
    )

    st.success(
        "Take short breaks every 30 minutes."
    )

    st.success(
        "Revise before sleeping."
    )

    csv = plan.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Timetable",
        csv,
        "study_plan.csv",
        "text/csv"
    )

    st.balloons()