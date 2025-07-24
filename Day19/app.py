import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Sales Dashboard")
st.write("Upload your sales CSV to generate report and chart.")

uploaded_file = st.file_uploader("Upload sales_data.csv", type="csv")

if uploaded_file:
    # Save uploaded file
    with open("sales_data.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read and analyze
    df = pd.read_csv("sales_data.csv")
    df["Total"] = df["Quantity"] * df["Price"]
    total_sales = df["Total"].sum()
    best = df.loc[df["Total"].idxmax()]

    # Generate report.txt
    report_text = f"Total Sales = ${total_sales}\nBest Selling Product = {best['Product']} (${best['Total']})"
    with open("report.txt", "w") as f:
        f.write(report_text)

    # Create bar chart
    plt.figure(figsize=(8,5))
    plt.bar(df["Product"], df["Total"], color="skyblue")
    plt.xlabel("Product")
    plt.ylabel("Total Sales ($)")
    plt.title("Product-wise Total Sales")
    plt.tight_layout()
    plt.savefig("bar_chart.png")

    # Display in app
    st.write("### Data Preview", df)
    st.image("bar_chart.png", caption="Bar chart of Total Sales")
    st.text_area("📝 Report", report_text, height=100)
    st.download_button("📥 Download Report", report_text, file_name="report.txt")
