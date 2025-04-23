# --- v1.5.0 - PUBLIC RELEASE ---
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
import io

st.set_page_config(layout="wide")
st.title("📊 MoSCoW Backlog Visualizer")

# --- Sidebar do konfiguracji ---
st.sidebar.header("⚙️ Ustawienia")
velocity = st.sidebar.number_input("Velocity zespołu", min_value=10, value=100, step=10)
must_threshold = st.sidebar.number_input("Granica 'Must have'", min_value=0, max_value=velocity, value=50)
should_threshold = st.sidebar.number_input("Granica 'Should have'", min_value=must_threshold, max_value=velocity,
                                           value=75)

# --- Inicjalizacja session_state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Rysowanie wykresu ---
st.subheader("📈 Wizualizacja Backlogu")
if st.session_state.tasks:
    export_data = []
    export_chart_data = []

    bar_x = []
    bar_base = []
    bar_color = []
    bar_text = []

    current_pos = 0
    for task in st.session_state.tasks:
        name = task["name"]
        points = task["points"]
        start = current_pos
        end = current_pos + points

        thresholds = [must_threshold, should_threshold, velocity]
        colors = ["#66BB6A", "#FFA726", "#FFEB3B", "#FF5252"]
        categories = ["Must have", "Should have", "Could have", "Won't have"]

        segments = []
        seg_start = start
        for i, threshold in enumerate(thresholds):
            if seg_start >= end:
                break
            seg_end = min(end, threshold)
            if seg_end > seg_start:
                segments.append({
                    "start": seg_start,
                    "width": seg_end - seg_start,
                    "color": colors[i],
                    "category": categories[i]
                })
                seg_start = seg_end
        if seg_start < end:
            segments.append({
                "start": seg_start,
                "width": end - seg_start,
                "color": colors[-1],
                "category": categories[-1]
            })

        for segment in segments:
            bar_x.append(segment["width"])
            bar_base.append(segment["start"])
            bar_color.append(segment["color"])
            bar_text.append(f"{name}<br>{segment['width']} pkt")

            chart_row = {"Name": name, "Must have": 0, "Should have": 0, "Could have": 0, "Won't have": 0}
            chart_row[segment["category"]] = segment["width"]
            export_chart_data.append(chart_row)

        export_data.append({
            "Name": name,
            "Points": points,
            "Category": segments[0]["category"],
            "Start Position": start
        })

        current_pos = end

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bar_x,
        y=["Backlog"] * len(bar_x),
        base=bar_base,
        orientation='h',
        marker=dict(
            color=bar_color,
            line=dict(color='rgba(0,0,0,0.6)', width=1)
        ),
        text=bar_text,
        hoverinfo='text',
        showlegend=False
    ))

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

    # --- Eksport CSV ---
    csv_buffer = io.StringIO()
    pd.DataFrame(export_data).to_csv(csv_buffer, index=False)
    st.download_button("📥 Pobierz CSV", data=csv_buffer.getvalue(), file_name="moscow_backlog.csv", mime="text/csv")

    # --- Eksport Excel z wykresem ---
    excel_buffer = io.BytesIO()
    df_export = pd.DataFrame(export_data)
    df_chart = pd.DataFrame(export_chart_data)
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df_export.to_excel(writer, sheet_name='Backlog', index=False)
        df_chart.to_excel(writer, sheet_name='Chart', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Chart']
        chart = workbook.add_chart({'type': 'column'})
        categories_range = f'=Chart!$A$2:$A${len(df_chart) + 1}'
        for i, cat in enumerate(["Must have", "Should have", "Could have", "Won't have"]):
            col = chr(66 + i)
            chart.add_series({
                'name': cat,
                'categories': categories_range,
                'values': f'=Chart!${col}$2:${col}${len(df_chart) + 1}'
            })
        chart.set_title({'name': 'Task Distribution by MoSCoW Category'})
        chart.set_x_axis({'name': 'Tasks'})
        chart.set_y_axis({'name': 'Points'})
        chart.set_style(11)
        worksheet.insert_chart('G2', chart)
    st.download_button("📥 Pobierz Excel", data=excel_buffer.getvalue(), file_name="moscow_backlog.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# --- Formularz dodawania zadania ---
st.subheader("➕ Dodaj nowe zadanie")
with st.form("add_task_form"):
    task_name = st.text_input("Nazwa zadania")
    task_points = st.number_input("Punkty story", min_value=1, max_value=100, value=10)
    submitted = st.form_submit_button("Dodaj")
    if submitted and task_name:
        if any(task_name == task["name"] for task in st.session_state.tasks):
            st.error(f"Zadanie o nazwie '{task_name}' już istnieje!")
        else:
            st.session_state.tasks.append({"name": task_name, "points": task_points})
            st.success(f"Dodano zadanie: {task_name} ({task_points} pkt)")
            st.rerun()

# --- Lista i edycja zadań z opcją przesuwania ---

st.subheader("📝 Lista zadań")
st.markdown("""
<style>
    .task-header {
        display: flex;
        font-weight: bold;
        padding: 4px 10px;
        margin-bottom: 4px;
    }
    .task-header > div {
        flex: 1;
    }
    .task-row {
        margin-bottom: 4px;
        padding: 6px;
        border-bottom: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

header_cols = st.columns([2, 5, 1, 1])
header_cols[0].markdown("**Priorytet**")
header_cols[1].markdown("**Nazwa**")
header_cols[2].markdown("**Pkt**")
header_cols[3].markdown("**Usuń**")
to_delete = []

for i, task in enumerate(st.session_state.tasks):
    with st.container():
        col_arrows, col_name, col_points, col_delete = st.columns([2, 5, 1, 1])

        col_up, col_down = col_arrows.columns([1, 1])
        if i > 0:
            if col_up.button("⬆️", key=f"up_{i}", use_container_width=True):
                st.session_state.tasks[i - 1], st.session_state.tasks[i] = st.session_state.tasks[i], \
                                                                           st.session_state.tasks[i - 1]
                st.rerun()
        else:
            col_up.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

        if i < len(st.session_state.tasks) - 1:
            if col_down.button("⬇️", key=f"down_{i}", use_container_width=True):
                st.session_state.tasks[i + 1], st.session_state.tasks[i] = st.session_state.tasks[i], \
                                                                           st.session_state.tasks[i + 1]
                st.rerun()
        else:
            col_down.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

        col_name.markdown(
            f"<div style='display:flex; align-items:center; height:38px; padding-left:10px'>{task['name']}</div>",
            unsafe_allow_html=True)

    new_points = col_points.number_input("Pkt", value=task["points"], key=f"edit_{i}", min_value=1,
                                         label_visibility="collapsed", step=1, format="%d")
    if new_points != task["points"]:
        task["points"] = new_points
        st.rerun()
    if col_delete.button("Usuń", key=f"delete_{i}"):
        to_delete.append(i)

for i in reversed(to_delete):
    st.session_state.tasks.pop(i)
    st.rerun()
