import os
import pandas as pd


def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """Loads raw online retail transaction data and performs baseline cleaning,

    feature engineering (Month, DayOfWeek, discount_percent, Revenue), and filtering.
    """
    # Load dataset with original encoding
    df = pd.read_csv(file_path, encoding="ISO-8859-1")

    # 1. Filter out non-positive quantities and prices (returns & adjustments)
    clean_df = df[(df["Quantity"] > 0) & (df["Price"] > 0)].copy()

    # 2. Parse timestamps and extract calendar features
    clean_df["InvoiceDate"] = pd.to_datetime(clean_df["InvoiceDate"])
    clean_df["Month"] = clean_df["InvoiceDate"].dt.month
    clean_df["DayOfWeek"] = clean_df["InvoiceDate"].dt.dayofweek

    # 3. Calculate item peak price and derive discount percentages
    clean_df["peak_price"] = clean_df.groupby("StockCode")["Price"].transform(
        "max"
    )
    clean_df["discount_percent"] = (
        (clean_df["peak_price"] - clean_df["Price"])
        / clean_df["peak_price"]
        * 100
    )
    clean_df = clean_df.drop(columns=["peak_price"])

    # 4. Compute total transaction revenue
    clean_df["Revenue"] = clean_df["Quantity"] * clean_df["Price"]

    return clean_df


if __name__ == "__main__":
    # Relative default path for running locally from project root
    default_path = os.path.join("data", "online_retail_II.csv")

    if os.path.exists(default_path):
        data = load_and_clean_data(default_path)
        print(
            f"Successfully cleaned dataset. Final Shape: {data.shape}"
        )
    else:
        print(f"Data file not found at {default_path}. Function ready for import.")
