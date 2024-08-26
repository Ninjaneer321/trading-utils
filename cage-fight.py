#!/usr/bin/env python3
"""
Stock performance comparison tool that allows users to compare the historical performance of multiple stocks.

Example:
    python3 cage-fight.py --tickers META,TSLA --start-date 2023-06-20 --end-date 2024-04-20

To install required packages:
    pip install pandas yfinance
"""
import colorsys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime, timedelta

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.dates import DateFormatter

from common.market import download_ticker_data


def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock_data = download_ticker_data(ticker, start_date, end_date)
        return stock_data["Adj Close"]
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def calculate_percent_change(stock_data):
    return stock_data.pct_change().fillna(0).add(1).cumprod().sub(1).mul(100)


def calculate_summary_stats(stock_data, ticker):
    total_change = stock_data.iloc[-1] - stock_data.iloc[0]
    total_pct_change = (stock_data.iloc[-1] / stock_data.iloc[0] - 1) * 100
    avg_daily_change = stock_data.pct_change().mean() * 100
    std_daily_change = stock_data.pct_change().std() * 100

    return {
        "Ticker": ticker,
        "Total Change": total_change,
        "Total Percent Change (%)": total_pct_change,
        "Average Daily Change (%)": avg_daily_change,
        "Standard Deviation of Daily Change (%)": std_daily_change,
    }


def plot_stock_performance(
    stock_data_list,
    ticker_list,
    start_date,
    end_date,
    show_plot=False,
    animation_duration=10,
    fps=60,
    font_name="Verdana",
):
    plt.rcParams["font.family"] = font_name
    sns.set_style("dark")
    plt.rcParams["axes.facecolor"] = "#1c1c1c"
    plt.rcParams["figure.facecolor"] = "#1c1c1c"
    plt.rcParams["text.color"] = "#e0e0e0"
    plt.rcParams["axes.labelcolor"] = "#e0e0e0"
    plt.rcParams["xtick.color"] = "#e0e0e0"
    plt.rcParams["ytick.color"] = "#e0e0e0"

    fig, ax = plt.subplots(figsize=(12, 6))

    min_length = min(len(data) for data in stock_data_list if data is not None)

    percent_changes = []
    for stock_data in stock_data_list:
        if stock_data is not None:
            pc = calculate_percent_change(stock_data)
            percent_changes.append(pc[:min_length])

    def generate_colors(n):
        hue_start = 0
        hue_end = 1
        hues = np.linspace(hue_start, hue_end, n, endpoint=False)
        colors = [colorsys.hsv_to_rgb(h, 0.8, 0.8) for h in hues]
        return colors

    contrasting_colors = generate_colors(len(ticker_list))

    lines = [
        ax.plot([], [], label=ticker, color=color, linewidth=1)[0]
        for ticker, color in zip(ticker_list, contrasting_colors)
    ]

    ax.set_xlim(percent_changes[0].index[0], percent_changes[0].index[-1])
    ax.set_ylim(
        min(pc.min() for pc in percent_changes), max(pc.max() for pc in percent_changes)
    )

    ax.set_title(
        f"Stock Performance Comparison ({start_date} to {end_date})",
        fontname=font_name,
        fontsize=14,
        color="#e0e0e0",
    )
    ax.set_ylabel(
        "% Change", fontname=font_name, fontsize=10, color="#e0e0e0"
    )
    ax.legend(
        loc="upper left",
        prop={"family": font_name, "size": 10},
        facecolor="#1c1c1c",
        edgecolor="#e0e0e0",
    )

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontname(font_name)
        label.set_fontsize(10)

    date_formatter = DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_formatter)
    fig.autofmt_xdate()

    annotation_boxes = []
    for ticker, line, color in zip(ticker_list, lines, contrasting_colors):
        ab = ax.annotate(
            ticker,
            xy=(0, 0),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=10,
            color="white",
            bbox=dict(boxstyle="round,pad=0.5", fc=color, ec="#e0e0e0", alpha=0.8),
            animated=True,
            fontname=font_name,
        )
        annotation_boxes.append(ab)
        ax.add_artist(ab)

    total_frames = int(animation_duration * fps)

    def animate(frame):
        index = int((frame / total_frames) * min_length)

        for line, pc, ab in zip(lines, percent_changes, annotation_boxes):
            line.set_data(pc.index[:index], pc.values[:index])
            if index > 0:
                ab.xy = (pc.index[index - 1], pc.values[index - 1])
                ab.set_visible(True)
            else:
                ab.set_visible(False)
        return lines + annotation_boxes

    anim = animation.FuncAnimation(
        fig, animate, frames=total_frames, interval=1000 / fps, blit=True
    )

    ticker_list_for_file_name = "-".join(ticker_list)
    anim.save(
        f"output/stock_performance_comparison-{ticker_list_for_file_name}-{start_date}-{end_date}.mp4",
        writer="ffmpeg",
        fps=fps,
    )

    if show_plot:
        plt.show()
    else:
        plt.close(fig)


def main():
    parser = ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--tickers",
        type=str,
        required=True,
        help="Comma-separated list of stock ticker symbols",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        required=False,
        default=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        help="Start date in the format YYYY-MM-DD",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        required=False,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date in the format YYYY-MM-DD",
    )
    parser.add_argument(
        "--show-plot",
        action="store_true",
        default=False,
        help="Show plot",
    )
    args = parser.parse_args()
    tickers = args.tickers.split(",")

    start_date = args.start_date
    end_date = args.end_date

    # Convert user input to lists
    ticker_list = [ticker.strip().upper() for ticker in tickers]

    # Fetch stock data for each ticker
    stock_data_list = []
    for ticker in ticker_list:
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        stock_data_list.append(stock_data)

    # Plot the stock performance comparison
    plot_stock_performance(
        stock_data_list,
        ticker_list,
        start_date,
        end_date,
        show_plot=args.show_plot,
        animation_duration=20,
        fps=30,
        font_name="Verdana",
    )

    # Print summary statistics for each stock
    print("\nSummary Statistics:")
    for stock_data, ticker in zip(stock_data_list, ticker_list):
        if stock_data is not None:
            summary_stats = calculate_summary_stats(stock_data, ticker)
            for key, value in summary_stats.items():
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()
