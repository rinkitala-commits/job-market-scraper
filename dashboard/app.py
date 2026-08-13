import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Job Market Analytics",
    page_icon="💼",
    layout="wide"
)


# -----------------------------
# Load Data
# -----------------------------

df = pd.read_csv(
    "data/cleaned_jobs.csv"
)
# Convert job posting date
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

skill_df = pd.read_csv(
    "data/skill_counts.csv"
)
# -----------------------------
# Filters
# -----------------------------

st.sidebar.header("🔎 Filters")

work_modes = ["All"] + sorted(
    df["work_mode"].dropna().unique().tolist()
)

selected_work_mode = st.sidebar.selectbox(
    "Work Mode",
    work_modes
)
locations = ["All"] + sorted(
    df["location"]
    .fillna("Unknown")
    .unique()
    .tolist()
)

selected_location = st.sidebar.selectbox(
    "Location",
    locations
)

salary_categories = ["All"] + sorted(
    df["salary_category"].dropna().unique().tolist()
)

selected_salary_category = st.sidebar.selectbox(
    "Salary Category",
    salary_categories
)
salary_min_value = int(
    df["salary_min"].fillna(0).max()
)

salary_range = st.sidebar.slider(
    "Minimum Salary",
    min_value=0,
    max_value=salary_min_value,
    value=0,
    step=5000
)

filtered_df = df.copy()

if selected_work_mode != "All":
    filtered_df = filtered_df[
        filtered_df["work_mode"] == selected_work_mode
    ]
if selected_location != "All":
    filtered_df = filtered_df[
        filtered_df["location"]
        .fillna("Unknown")
        == selected_location
    ]

if selected_salary_category != "All":
    filtered_df = filtered_df[
        filtered_df["salary_category"]
        == selected_salary_category
    ]
if salary_range > 0:
    filtered_df = filtered_df[
        filtered_df["salary_min"].fillna(0)
        >= salary_range
    ]

# -----------------------------
# Title
# -----------------------------

st.title("💼 Job Market Analytics Dashboard")

st.markdown(
    """
    **Explore real-world job market data using Python and Data Science.**

    Analyze job listings, salary trends, skills, locations, companies,
    and work modes through an interactive dashboard.
    """
)
st.divider()


# -----------------------------
# KPIs
# -----------------------------

total_jobs = len(filtered_df)

jobs_with_salary = filtered_df[
    filtered_df["salary_min"].notna()
    & filtered_df["salary_max"].notna()
]

salary_disclosure_rate = (
    len(jobs_with_salary) / total_jobs * 100
    if total_jobs > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Jobs",
        total_jobs
    )

with col2:
    st.metric(
        "Jobs With Salary",
        len(jobs_with_salary)
    )

with col3:
    st.metric(
        "Salary Disclosure",
        f"{salary_disclosure_rate:.1f}%"
    )
with col4:
    if not jobs_with_salary.empty:
        average_salary = jobs_with_salary[
            "salary_midpoint"
        ].mean()
        st.metric(
            "Average Salary",
            f"${average_salary:,.0f}"
        )
    else:
        st.metric(
            "Average Salary",
            "N/A"
        )

# -----------------------------
# Dataset Summary
# -----------------------------

st.header("📊 Dataset Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric(
        "Companies",
        filtered_df["company"].nunique()
    )

with summary_col2:
    st.metric(
        "Locations",
        filtered_df["location"].nunique()
    )

with summary_col3:
    st.metric(
        "Skills Tracked",
        skill_df["skill"].nunique()
    )

# -----------------------------
# Job Market Overview
# -----------------------------

st.header("📊 Job Market Overview")

overview_col1, overview_col2 = st.columns(2)

with overview_col1:

    st.subheader("🏢 Jobs by Work Mode")

    work_mode_overview = (
        filtered_df["work_mode"]
        .fillna("Not Specified")
        .value_counts()
    )

    st.bar_chart(work_mode_overview)

with overview_col2:

    st.subheader("📍 Jobs by Location")

    location_overview = (
        filtered_df["location"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
    )

    st.bar_chart(location_overview)


# -----------------------------
# Job Listings
# -----------------------------

st.header("📋 Job Listings")

search = st.text_input(
    "🔍 Search Jobs",
    placeholder="Search by job title or company..."
)


if search:
    filtered_df = filtered_df[
        filtered_df["job_title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
        |
        filtered_df["company"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

st.caption(
    f"Showing {len(filtered_df)} matching job(s)"
)


if filtered_df.empty:

    st.warning(
        "No jobs match the selected filters."
    )

else:

    display_df = filtered_df[
        [
            "job_title",
            "company",
            "location",
            "salary_min",
            "salary_max",
            "salary_category",
            "work_mode",
            "url"
        ]
    ].copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "url": st.column_config.LinkColumn(
                "Apply / Job Link",
                display_text="Open Job"
            ),
            "salary_min": st.column_config.NumberColumn(
                "Minimum Salary",
                format="%d"
            ),
            "salary_max": st.column_config.NumberColumn(
                "Maximum Salary",
                format="%d"
            )
        },
        hide_index=True
    )
# -----------------------------
# Latest Jobs
# -----------------------------

st.header("🆕 Latest Job Listings")

latest_jobs = filtered_df.sort_values(
    "date",
    ascending=False
).head(10)

st.dataframe(
    latest_jobs[
        [
            "date",
            "job_title",
            "company",
            "location",
            "work_mode",
            "url"
        ]
    ],
    use_container_width=True,
    column_config={
        "url": st.column_config.LinkColumn(
            "Job Link",
            display_text="Open Job"
        ),
        "date": st.column_config.DatetimeColumn(
            "Posted Date",
            format="YYYY-MM-DD"
        )
    },
    hide_index=True
)
# -----------------------------
# Automated Insights
# -----------------------------

st.header("💡 Key Insights")

if not filtered_df.empty:

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        top_location = (
            filtered_df["location"]
            .fillna("Unknown")
            .value_counts()
            .idxmax()
        )

        top_company = (
            filtered_df["company"]
            .value_counts()
            .idxmax()
        )

        st.info(
            f"📍 Most common location: **{top_location}**"
        )

        st.info(
            f"🏢 Company with most listings: **{top_company}**"
        )

    with insight_col2:

        remote_count = (
            filtered_df["work_mode"]
            .eq("Remote")
            .sum()
        )

        salary_count = (
            filtered_df["salary_midpoint"]
            .notna()
            .sum()
        )

        st.info(
            f"🌍 Remote jobs detected: **{remote_count}**"
        )

        st.info(
            f"💰 Jobs with salary data: **{salary_count}**"
        )

else:

    st.warning(
        "No data available for generating insights."
    )
# -----------------------------
# Top Skills
# -----------------------------
st.header("🔥 Most Demanded Skills")

top_skills = skill_df.head(10).copy()

st.bar_chart(
    top_skills.set_index("skill")[
        "job_count"
    ]
)

st.write(
    f"Based on {total_jobs} jobs in the current dataset."
)
# -----------------------------
# Skill Category Analysis
# -----------------------------

st.header("🧠 Skill Demand Analysis")

skill_data = skill_df.copy()

if not skill_data.empty:

    total_skill_mentions = skill_data["job_count"].sum()

    skill_data["percentage"] = (
        skill_data["job_count"]
        / total_skill_mentions
        * 100
    )

    skill_data["percentage"] = (
        skill_data["percentage"]
        .round(2)
    )

    st.dataframe(
        skill_data.head(15),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No skill data is available."
    )
# -----------------------------
# Top Locations
# -----------------------------

st.header("🌍 Top Job Locations")

location_counts = (
    df["location"]
    .fillna("Unknown")
    .value_counts()
    .head(10)
)

st.bar_chart(location_counts)

# -----------------------------
# Work Mode Analysis
# -----------------------------

st.header("🏢 Work Mode Distribution")

work_mode_counts = (
    filtered_df["work_mode"]
    .fillna("Unknown")
    .value_counts()
)

st.bar_chart(
    work_mode_counts
)

# -----------------------------
# Salary Category Analysis
# -----------------------------

st.header("💵 Salary Category Distribution")

salary_category_counts = (
    filtered_df["salary_category"]
    .fillna("Not Disclosed")
    .value_counts()
)

st.bar_chart(salary_category_counts)
# -----------------------------
# Salary Analysis
# -----------------------------

st.header("💰 Salary Analysis")

salary_data = filtered_df.dropna(
    subset=[
        "salary_min",
        "salary_max",
        "salary_midpoint"
    ]
)

if salary_data.empty:

    st.info(
        "No salary information is available "
        "for the selected jobs."
    )

else:

    avg_min = salary_data["salary_min"].mean()
    avg_max = salary_data["salary_max"].mean()
    avg_midpoint = salary_data["salary_midpoint"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Minimum Salary",
            f"{avg_min:,.0f}"
        )

    with col2:
        st.metric(
            "Average Maximum Salary",
            f"{avg_max:,.0f}"
        )

    with col3:
        st.metric(
            "Average Salary Midpoint",
            f"{avg_midpoint:,.0f}"
        )

    st.dataframe(
        salary_data[
            [
                "job_title",
                "company",
                "salary_min",
                "salary_max",
                "salary_midpoint"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# Salary Distribution
# -----------------------------
st.subheader("📊 Salary Distribution")

salary_chart = salary_data[
    [
        "job_title",
        "salary_midpoint"
    ]
].copy()

salary_chart = salary_chart.sort_values(
    "salary_midpoint",
    ascending=False
)

st.bar_chart(
    salary_chart.set_index("job_title")[
        "salary_midpoint"
    ]
)

# -----------------------------
# Footer
# -----------------------------

st.divider()

st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <p>💼 <strong>Job Market Analytics Dashboard</strong></p>
        <p>Built with Python, Pandas, Matplotlib & Streamlit</p>
        <p>👩‍💻 Jhumarani Tala | B.Tech Data Science Student</p>
    </div>
    """,
    unsafe_allow_html=True
)