import pandas as pd
import matplotlib.pyplot as plt


def plot_top_locations(df, top_n=10):
    """Plot the most common job locations."""

    locations = (
        df["location"]
        .fillna("Unknown")
        .value_counts()
        .head(top_n)
    )

    plt.figure(figsize=(10, 6))

    locations.sort_values().plot(
        kind="barh"
    )

    plt.title("Top Job Locations")
    plt.xlabel("Number of Jobs")
    plt.ylabel("Location")

    plt.tight_layout()

    plt.savefig(
        "data/top_job_locations.png",
        dpi=300
    )

    plt.show()


def plot_top_companies(df, top_n=10):
    """Plot companies with the most listings."""

    companies = (
        df["company"]
        .value_counts()
        .head(top_n)
    )

    plt.figure(figsize=(10, 6))

    companies.sort_values().plot(
        kind="barh"
    )

    plt.title("Companies with Most Job Listings")
    plt.xlabel("Number of Jobs")
    plt.ylabel("Company")

    plt.tight_layout()

    plt.savefig(
        "data/top_companies.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":

    df = pd.read_csv(
        "data/cleaned_jobs.csv"
    )

    plot_top_locations(df)
    plot_top_companies(df)