import pandas as pd


def load_cleaned_data(file_path):
    """Load the cleaned job dataset."""
    return pd.read_csv(file_path)


def salary_analysis(df):
    """Analyze jobs that contain salary information."""

    salary_df = df.dropna(
        subset=["salary_min", "salary_max"]
    ).copy()

    if salary_df.empty:
        return None

    return {
        "jobs_with_salary": len(salary_df),
        "average_min_salary": salary_df["salary_min"].mean(),
        "average_max_salary": salary_df["salary_max"].mean(),
        "average_salary_midpoint": salary_df["salary_midpoint"].mean(),
    }


def location_analysis(df):
    """Count jobs by location."""

    return (
        df["location"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
    )


def company_analysis(df):
    """Count jobs by company."""

    return (
        df["company"]
        .value_counts()
        .head(10)
    )


if __name__ == "__main__":

    df = load_cleaned_data(
        "data/cleaned_jobs.csv"
    )

    print("Total jobs:", len(df))

    print("\nSalary Analysis:")
    print(salary_analysis(df))

    print("\nTop Locations:")
    print(location_analysis(df))

    print("\nTop Companies:")
    print(company_analysis(df))