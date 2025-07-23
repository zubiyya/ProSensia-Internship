
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

try:
    df = pd.read_csv("sales_data.csv")
except Exception as e:
    logging.error(f"Error reading CSV: {e}")
    raise

try:
    df.groupby("Product")["Sales"].sum().plot(kind="bar", title="Sales by Product", color='skyblue')
    plt.tight_layout()
    plt.savefig("Bar Chart.png")
    plt.clf()
except Exception as e:
    logging.error(f"Bar chart error: {e}")
