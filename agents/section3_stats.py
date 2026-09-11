import pandas as pd

SECTION_3_AGENTS = [
    {"name": "Stats Analyst", "job": "compute descriptive statistics on tabular biological data"},
    {"name": "Anomaly Spotter", "job": "flag unusual or outlier values in biological data"}
]

def analyze_statistics(filepath, column):
    df = pd.read_csv(filepath)
    stats = {
    "mean": float(df[column].mean()),
    "median": float(df[column].median()),
    "std_dev": float(df[column].std()),
    "min": float(df[column].min()),
    "max": float(df[column].max())
}
    return stats

def find_outliers(filepath, column):
    df = pd.read_csv(filepath)
    mean = df[column].mean()
    std = df[column].std()

    outliers = df[(df[column] - mean).abs() > 3 * std]
    return outliers[[column]].to_dict(orient="records")

if __name__ == "__main__":
    print(analyze_statistics("sample_data.csv", "value"))
    print(find_outliers("sample_data.csv", "value"))