# Smart Study Schedule Generator
# Streamlit app: with colorful subjects 🎨

import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.cm as cm
import matplotlib.colors as mcolors

st.set_page_config(page_title="Smart Study Schedule Generator", page_icon="📚", layout="wide")

st.title("📚 Smart Study Schedule Generator")
st.write(
    "Enter your subjects and their difficulty, choose how many hours you can study this week, "
    "and get an automatically balanced, colorful weekly schedule."
)

with st.sidebar:
    st.header("How this works")
    st.markdown(
        """
        **Steps**
        1. Edit the table to list your subjects and pick a difficulty.
        2. Set your total weekly study hours.
        3. (Optional) Open **Advanced Options** to tweak daily hours or session length.
        4. Click **Generate Schedule**.
        
        **Tip**: Difficulty weights are used to split your weekly hours:
        - Easy = 1x
        - Medium = 2x
        - Hard = 3x
        """
    )

    # 🎨 Color palette choice
    palette_name = st.selectbox(
        "🎨 Choose Color Palette",
        ["tab10", "tab20", "Set3", "Pastel1", "Dark2"],
        index=0
    )

# Default subjects
default_df = pd.DataFrame({
    "Subject": ["Math", "English", "Science"],
    "Difficulty": ["Hard", "Medium", "Easy"]
})

st.subheader("1) Subjects & Difficulty")
edited_df = st.data_editor(
    default_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Difficulty": st.column_config.SelectboxColumn(
            "Difficulty",
            options=["Easy", "Medium", "Hard"],
            required=True
        )
    }
)

st.subheader("2) Weekly Study Hours")
total_hours = st.number_input("Total hours you can study this week", min_value=1.0, value=14.0, step=1.0)

with st.expander("Advanced Options (optional)"):
    st.caption("Tweak daily hours and session length if you want more control.")
    session_len = st.selectbox("Session length (hours per study block)", [0.5, 1.0, 1.5, 2.0], index=1)
    equal_per_day = total_hours / 7.0
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_df = pd.DataFrame({"Day": days, "Hours": [round(equal_per_day, 2)] * 7})
    custom = st.checkbox("Customize hours per day")
    if custom:
        day_df = st.data_editor(day_df, use_container_width=True, num_rows=7, disabled=["Day"], key="day_editor")
    else:
        st.dataframe(day_df, use_container_width=True)

generate = st.button("✨ Generate Schedule", type="primary")

# --- Helpers ---
def _difficulty_weight(d):
    return {"Easy": 1, "Medium": 2, "Hard": 3}.get(d, 1)

def _normalize_daily_hours(df, total):
    s = float(df["Hours"].sum())
    if s <= 0:
        return pd.Series([total/7.0]*7, index=df.index), True
    if abs(s - total) < 1e-6:
        return df["Hours"], False
    scaled = df["Hours"] * (total / s)
    return scaled, True

def get_subject_colors(subjects, palette="tab10"):
    n = max(1, len(subjects))
    cmap = cm.get_cmap(palette, n)
    return {subj: mcolors.to_hex(cmap(i)) for i, subj in enumerate(subjects)}

def build_schedule(subjects_df, total_hours, day_hours_series, session_len):
    subjects_df = subjects_df.copy()
    subjects_df["Weight"] = subjects_df["Difficulty"].map(_difficulty_weight)
    subjects_df = subjects_df[subjects_df["Subject"].astype(str).str.strip() != ""]
    if subjects_df.empty:
        return pd.DataFrame(columns=["Day", "Start Time", "Subject", "Duration (hrs)"]), pd.DataFrame()

    total_weight = subjects_df["Weight"].sum()
    if total_weight == 0:
        subjects_df["Weight"] = 1
        total_weight = subjects_df["Weight"].sum()

    subjects_df["TargetHours"] = subjects_df["Weight"] * (total_hours / total_weight)
    remaining = {row["Subject"]: float(row["TargetHours"]) for _, row in subjects_df.iterrows()}

    schedule_rows = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def pick_subject(remaining_dict):
        if not remaining_dict:
            return None
        filtered = {k: v for k, v in remaining_dict.items() if v > 1e-6}
        if not filtered:
            return None
        return max(filtered, key=lambda k: filtered[k])

    for i, day in enumerate(days):
        day_remaining = float(day_hours_series.iloc[i])
        current_time = 8.0  # start at 08:00
        safety = 0
        while day_remaining > 1e-6:
            subj = pick_subject(remaining)
            if subj is None:
                break
            block = min(session_len, day_remaining, remaining[subj])
            if block <= 1e-6:
                break

            start_hour = int(current_time)
            start_min = int(round((current_time - start_hour) * 60))
            start_str = f"{start_hour:02d}:{start_min:02d}"
            schedule_rows.append({
                "Day": day,
                "Start Time": start_str,
                "Subject": subj,
                "Duration (hrs)": round(float(block), 2)
            })

            remaining[subj] -= block
            day_remaining -= block
            current_time += block
            safety += 1
            if safety > 1000:
                break

    schedule_df = pd.DataFrame(schedule_rows)
    if schedule_df.empty:
        summary = pd.DataFrame()
    else:
        summary = schedule_df.pivot_table(
            index="Day", columns="Subject", values="Duration (hrs)", aggfunc="sum", fill_value=0.0
        ).reindex(days)

    return schedule_df, summary

# --- Main ---
if generate:
    if edited_df.empty or "Subject" not in edited_df.columns or "Difficulty" not in edited_df.columns:
        st.error("Please provide at least one subject with a difficulty.")
        st.stop()

    if 'day_editor' in st.session_state and isinstance(st.session_state['day_editor'], pd.DataFrame):
        dh = st.session_state['day_editor']
    else:
        equal_per_day = total_hours / 7.0
        dh = pd.DataFrame({"Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                           "Hours": [round(equal_per_day, 2)] * 7})

    day_hours, rescaled = _normalize_daily_hours(dh, total_hours)
    if rescaled:
        st.info("Daily hours were rescaled to match your total weekly hours.")

    sched_df, summary_df = build_schedule(edited_df, total_hours, day_hours, session_len)

    st.subheader("📆 Generated Weekly Schedule (Detailed)")
    if sched_df.empty:
        st.warning("No schedule could be generated. Please check your inputs.")
    else:
        # 🎨 Color setup
        subject_colors = get_subject_colors(sorted(sched_df["Subject"].unique()), palette=palette_name)

        # Legend
        st.caption("📌 Legend")
        for subj, color in subject_colors.items():
            st.markdown(
                f'<div style="display:flex;align-items:center;margin:4px 0">'
                f'<div style="width:16px;height:16px;background:{color};border:1px solid #555;margin-right:8px;"></div>'
                f'<span style="font-size:14px;">{subj}</span></div>',
                unsafe_allow_html=True
            )

        # Detailed schedule with colors
        def style_detailed(df):
            styles = pd.DataFrame("", index=df.index, columns=df.columns)
            for idx, row in df.iterrows():
                c = subject_colors.get(row["Subject"], "#FFFFFF")
                styles.loc[idx, "Subject"] = f"background-color: {c}; color: black; font-weight: 700;"
            return styles

        styled_detailed = sched_df.style.apply(style_detailed, axis=None)
        st.dataframe(styled_detailed, use_container_width=True)

        st.subheader("📊 Weekly Summary (hours per subject per day)")

        def style_summary(df):
            styles = pd.DataFrame("", index=df.index, columns=df.columns)
            for subj in df.columns:
                c = subject_colors.get(subj, "#FFFFFF")
                styles.loc[df[subj] > 0, subj] = f"background-color: {c}; color: black; font-weight: 600;"
            return styles

        styled_summary = summary_df.style.apply(style_summary, axis=None)
        st.dataframe(styled_summary, use_container_width=True)

        # Downloads
        csv1 = sched_df.to_csv(index=False).encode("utf-8")
        csv2 = summary_df.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button("Download Detailed Schedule CSV", data=csv1, file_name="schedule_detailed.csv", mime="text/csv")
        st.download_button("Download Weekly Summary CSV", data=csv2, file_name="schedule_summary.csv", mime="text/csv")

        st.success("✅ Schedule ready! You can tweak inputs and regenerate anytime.")
else:
    st.info("Fill in your subjects and hours, then click **Generate Schedule**.")

