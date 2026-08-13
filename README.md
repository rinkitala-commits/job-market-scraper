# 💼 Job Market Scraper & Data Science Dashboard

A Python and Data Science project that collects job listings from a publicly accessible job-data API, cleans and analyzes the data, performs salary and skill analysis, and presents insights through an interactive Streamlit dashboard.

## 🚀 Project Overview

This project demonstrates an end-to-end Data Science workflow:

**API Data Collection → Data Cleaning → Feature Engineering → EDA → Visualization → Interactive Dashboard**

## 🎯 Project Goals

- Collect job listing data automatically
- Clean and preprocess real-world job data
- Analyze salary information
- Identify frequently requested skills
- Analyze job locations and companies
- Detect work modes such as Remote, Hybrid, and In-Office
- Build an interactive dashboard
- Create a portfolio-ready Data Science project

## 🛠️ Technologies Used

- Python
- Requests
- Pandas
- Matplotlib
- Streamlit
- REST API
- CSV
- Data Analysis
- Data Visualization

## 📂 Project Structure

```text
job_market_scraper/
│
├── data/
│   ├── raw_jobs.csv
│   ├── cleaned_jobs.csv
│   ├── skill_counts.csv
│   ├── top_job_locations.png
│   └── top_companies.png
│
├── src/
│   ├── scraper.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── visualization.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md

## 📊 Features

### 🔎 Data Collection

Collects job information including:

- Job title
- Company
- Location
- Salary range
- Skills
- Job posting date
- Job description
- Job URL
- Scraping timestamp

### 🧹 Data Cleaning

The pipeline handles:

- Missing values
- Salary data
- Skill parsing
- Datetime conversion
- Text encoding
- Salary midpoint calculation

### ⚙️ Feature Engineering

Additional features include:

- Salary midpoint
- Salary category
- Work mode
- Skill frequency

### 📈 Data Analysis

The project analyzes:

- Salary disclosure
- Salary ranges
- Popular skills
- Job locations
- Companies with multiple listings
- Work-mode distribution

### 📊 Interactive Dashboard

The Streamlit dashboard provides:

- Job search
- Work-mode filtering
- Location filtering
- Salary-category filtering
- Minimum salary filtering
- Job listing table
- Direct job links
- Salary analysis
- Skill-demand analysis
- Work-mode visualization
- Automated insights
- Latest job listings

## 💰 Salary Data Limitation

Salary information is not available for every job listing.

The analysis therefore uses only jobs with disclosed salary information when calculating salary statistics.

Jobs without salary information are categorized as:

`Not Disclosed`


## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/rinkitala-commits/job_market_scraper.git
```

Go to the project

```bash
cd personal-finance-dashboard
```
Create a virtual environment

```bash
python -m venv .venv
```
Activate the environment

```bash
.venv\Scripts\Activate.ps1
```
Install dependencies

```bash
pip install -r requirements.txt
```

Run the scraper

```bash
python src/scraper.py
```
Run the data

```bash
python src/data_cleaning.py
```
Run analysis
```bash
python src/analysis.py
```
Launch the dashboard
```bash
streamlit run dashboard/app.py
```

---
## 📈 Data Science Workflow
                Job Data API
                    ↓
                Data Collection
                    ↓
                Raw Dataset
                    ↓
                Data Cleaning
                    ↓
                Feature Engineering
                    ↓
                Exploratory Data Analysis
                    ↓
                Visualization
                    ↓
                Streamlit Dashboard
---
---

## 📈 Future Improvements

-Collect jobs from multiple sources
-Schedule automatic scraping
-Store historical job data
-Add more salary records
-Add NLP-based skill extraction
-Add job-category classification
-Add salary prediction
-Add interactive Plotly visualizations
-Deploy the dashboard online

---

## 👩‍💻 Author

**Jhumarani Tala**

B.Tech Data Science Student | Python | Data Science | Data Analysis | AI & Machine Learning

GitHub:
https://github.com/rinkitala-commits