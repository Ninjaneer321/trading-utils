#!/usr/bin/env python3
"""
Stock Data Analysis Script

This script allows the user to download and analyze stock data.

Example:
    python3 max-consecutive-days.py --symbol TQQQ --from_date 2012-01-01 --to_date 2023-01-01

To install required packages:
    pip install pandas yfinance
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from common.market import download_ticker_data

OUTPUT_FOLDER = Path.cwd() / "output"
OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download and analyze stock data.")
    parser.add_argument(
        "--symbol", type=str, default="TSLA", help="Stock symbol (default: TSLA)"
    )
    parser.add_argument(
        "--from_date",
        type=str,
        default=(datetime.now() - timedelta(days=10 * 365)).strftime("%Y-%m-%d"),
        help="Start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--to_date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date in YYYY-MM-DD format",
    )
    return parser.parse_args()


def save_to_file(symbol, data, start_date, end_date):
    file_name = OUTPUT_FOLDER.joinpath(f"{symbol}_{start_date}_{end_date}.csv")
    if not file_name.exists():
        data.to_csv(file_name)
    return file_name


def load_data_frame(file_path):
    return pd.read_csv(file_path)


def find_max_consecutive(df, consecutive):
    if isinstance(consecutive, pd.DataFrame):
        if len(consecutive.columns) == 1:
            consecutive = consecutive.iloc[:, 0]
        else:
            raise ValueError(
                "The 'consecutive' DataFrame must have only one column for grouping."
            )

    max_consecutive = consecutive * (
        consecutive.groupby((consecutive != consecutive.shift()).cumsum()).cumcount()
        + 1
    )
    max_increase_days = max_consecutive.max()
    max_period = max_consecutive.idxmax()
    # Use iloc with index to find the start and end dates
    start_date_index = df.index.get_loc(max_period) - max_increase_days + 1
    end_date_index = df.index.get_loc(max_period)

    # Ensure the index does not go out of bounds
    start_date_index = max(0, start_date_index)
    end_date_index = min(len(df) - 1, end_date_index)

    start_date = df.index[start_date_index]
    end_date = df.index[end_date_index]
    return max_increase_days, start_date, end_date


def main():
    args = parse_arguments()
    df = download_ticker_data(args.symbol, start=args.from_date, end=args.to_date)
    max_increase_days, start_date, end_date = find_max_consecutive(
        df, (df["Adj Close"] > df["Adj Close"].shift()).astype(int)
    )
    print(
        f"✅ {start_date} to {end_date} closing price increase: {max_increase_days} days"
    )
    max_decrease_days, start_date, end_date = find_max_consecutive(
        df, (df["Adj Close"] < df["Adj Close"].shift()).astype(int)
    )
    print(
        f"❌ {start_date} to {end_date} closing price decrease: {max_decrease_days} days"
    )


if __name__ == "__main__":
    main()
