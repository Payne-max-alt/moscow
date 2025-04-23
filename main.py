import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")
st.title("📊 MoSCoW Backlog Visualizer")

# --- Inicjalizacja session_state dla zadań ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []  # lista słowników: {"name": ..., "points": ...}

# --- Sidebar do konfiguracji ---
st.sidebar.header("⚙️ Ustawienia")
velocity = st.sidebar.number_input("Velocity zespołu", min_value=10, value=100, step=10)
must_threshold = st.sidebar.number_input("Granica 'Must have'", min_value=0, max_value=velocity, value=50)
should_threshold = st.sidebar.number_input("Granica 'Should have'", min_value=must_threshold, max_value=velocity, value=75)

# --- Formularz dodawania zadania ---
st.subheader("➕ Dodaj nowe zadanie")
with st.form("add_task_form"):
    task_name = st.text_input("Nazwa zadania")
    task_points = st.number_input("Punkty story", min_value=1, max_value=100, value=10)
    submitted = st.form_submit_button("Dodaj")
    if submitted and task_name:
        st.session_state.tasks.append({"name": task_name, "points": task_points})
        st.success(f"Dodano zadanie: {task_name} ({task_points} pkt)")

# --- Edycja i usuwanie ---
st.subheader("📝 Lista zadań")
to_delete = []
for i, task in enumerate(st.session_state.tasks):
    col1, col2, col3, col4 = st.columns([5, 2, 2, 1])
    col1.write(task["name"])
    new_points = col2.number_input("Pkt", key=f"points_{i}", value=task["points"], min_value=1)
    if new_points != task["points"]:
        task["points"] = new_points
    if col3.button("Usuń", key=f"delete_{i}"):
        to_delete.append(i)

for i in reversed(to_delete):
    st.session_state.tasks.pop(i)

# --- Rysowanie wykresu ---
st.subheader("📈 Wizualizacja Backlogu")
if st.session_state.tasks:
    task_positions = []
    task_widths = []
    task_labels = []
    task_colors = []
    task_categories = []

    current_pos = 0
    for task in st.session_state.tasks:
        name = task["name"]
        points = task["points"]

        if current_pos < must_threshold:
            category = "Must have"
            color = "#66BB6A"
        elif current_pos < should_threshold:
            category = "Should have"
            color = "#FFA726"
        elif current_pos < velocity:
            category = "Could have"
            color = "#FFEB3B"
        else:
            category = "Won't have"
            color = "#FF5252"

        task_positions.append(current_pos)
        task_widths.append(points)
        task_labels.append(f"{name}<br>{points} pkt")
        task_colors.append(color)
        task_categories.append(category)

        current_pos += points

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=task_widths,
        y=["Backlog"] * len(task_widths),
        base=task_positions,
        orientation='h',
        marker_color=task_colors,
        text=task_labels,
        hoverinfo='text',
        showlegend=False
    ))

    # Linie graniczne
    for boundary, label in zip([must_threshold, should_threshold, velocity],
                               ["Must/Could", "Could/Should", "Should/Won't"]):
        fig.add_shape(
            type="line",
            x0=boundary,
            y0=-1,
            x1=boundary,
            y1=1,
            line=dict(color="red", width=2, dash="dot")
        )
        fig.add_annotation(
            x=boundary,
            y=1.2,
            text=label,
            showarrow=False,
            font=dict(color="red", size=12)
        )

    fig.update_layout(
        title="Backlog w kontekście MoSCoW i velocity",
        xaxis=dict(title="Story Points", range=[0, max(current_pos + 10, velocity + 20)]),
        yaxis=dict(showticklabels=False),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Brak zadań do wyświetlenia.")
