import pandas as pd
import ast


def load_data(file_path):
    """Load raw job data from CSV."""
    df = pd.read_csv(file_path)
    return df


def basic_cleaning(df):
    """Perform basic data cleaning."""

    # Remove duplicate jobs
    df = df.drop_duplicates()

    # Convert empty strings to missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Clean text columns
    text_columns = [
        "job_title",
        "company",
        "location"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # Convert salary columns to numeric
    df["salary_min"] = pd.to_numeric(
        df["salary_min"],
        errors="coerce"
    )

    df["salary_max"] = pd.to_numeric(
        df["salary_max"],
        errors="coerce"
    )

    # Convert date to datetime
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )
    # Treat zero salaries as missing salary information
    df["salary_min"] = df["salary_min"].replace(0, pd.NA)
    df["salary_max"] = df["salary_max"].replace(0, pd.NA)

    # Remove rows without a job title
    df = df.dropna(subset=["job_title"])

    # Remove duplicate job URLs
    df = df.drop_duplicates(subset=["url"])
    # Calculate salary midpoint
    df["salary_midpoint"] = (
        df["salary_min"] + df["salary_max"]
    ) / 2
    # Create salary categories
    def salary_category(salary):
        if pd.isna(salary):
            return "Not Disclosed"
        elif salary < 50000:
            return "Below 50K"
        elif salary < 100000:
            return "50K - 100K"
        elif salary < 150000:
            return "100K - 150K"
        else:
            return "150K+"

    df["salary_category"] = df["salary_midpoint"].apply(
        salary_category
    )
    # Convert skills from string representation to Python lists
    def parse_skills(value):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError, TypeError):
            return []

    df["skills"] = df["skills"].apply(parse_skills)

    # Convert scraping timestamp to datetime
    df["scraped_at"] = pd.to_datetime(
        df["scraped_at"],
        errors="coerce"
    )

    # Detect work mode from job description
    def detect_work_mode(text):
        if pd.isna(text):
            return "Unknown"

        text = str(text).lower()

        if "in-office" in text or "in office" in text:
            return "In-Office"
        elif "hybrid" in text:
            return "Hybrid"
        elif "remote" in text:
            return "Remote"
        else:
            return "Not Specified"

    df["work_mode"] = df["description"].apply(
        detect_work_mode
    )
    return df


if __name__ == "__main__":

    file_path = "data/raw_jobs.csv"

    df = load_data(file_path)

    print("Before cleaning:", len(df), "rows")

    df = basic_cleaning(df)
    # Save cleaned dataset
    df.to_csv(
        "data/cleaned_jobs.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nCleaned data saved successfully!")
    print("File: data/cleaned_jobs.csv")

    print("After cleaning:", len(df), "rows")

    print("\nMissing values:")
    print(df.isnull().sum())

    # Analyze salary availability
    salary_missing = (
        df["salary_min"].isna() &
        df["salary_max"].isna()
    )

    print("\nSalary statistics:")
    print(df[["salary_min", "salary_max"]].describe())
    print("Jobs with salary information:", (~salary_missing).sum())
    print("Jobs without salary information:", salary_missing.sum())

    print("\nSalary statistics:")
    print(df[["salary_min", "salary_max"]].describe())

    print("\nSalary midpoint:")
    print(
        df[
            ["job_title", "salary_min", "salary_max", "salary_midpoint"]
        ].dropna(subset=["salary_midpoint"])
    )

    print("\nDataset columns:")
    print(df.columns.tolist())

    print("\nScraping timestamp:")
    print(df["scraped_at"].head())

    print("\nMissing salary values:")
    print(df["salary_midpoint"].isna().sum())
    print("\nSample skills:")
    print(df["skills"].head(10).to_list())

    # Extract all individual skills
    all_skills = []

    for skill_list in df["skills"]:
        all_skills.extend(skill_list)

    skill_counts = pd.Series(all_skills).value_counts()
    # Save skill frequency data
    skill_counts_df = skill_counts.reset_index()
    skill_counts_df.columns = ["skill", "job_count"]

    skill_counts_df.to_csv(
        "data/skill_counts.csv",
        index=False
    )

    print("\nSkill analysis saved successfully!")
    print("File: data/skill_counts.csv")

    print("\nTop 15 skills:")
    print(skill_counts.head(15))

    print("\nSalary categories:")   
    print(df["salary_category"].value_counts())

    print("\nWork mode distribution:")
    print(df["work_mode"].value_counts())