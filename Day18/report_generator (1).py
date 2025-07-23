import pandas as pd

df = pd.read_csv('sales_data.csv')
df['Revenue'] = df['Units Sold'] * df['Unit Price']
grouped = df.groupby('Product').agg({'Revenue': 'sum'}).reset_index()
total_revenue = grouped['Revenue'].sum()
top_product = grouped.loc[grouped['Revenue'].idxmax()]

report_lines = ['📊 Sales Summary']
for _, row in grouped.iterrows():
    report_lines.append(f"Product: {row['Product']} – Revenue: {int(row['Revenue'])}")
report_lines.append('')
report_lines.append(f"🔸 Total Revenue: {int(total_revenue)}")
report_lines.append(f"🔸 Top Product: {top_product['Product']}")

with open('report.txt', 'w') as report_file:
    report_file.write('\n'.join(report_lines))