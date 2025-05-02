import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import os


project_root = "/root/DSCI510-Final-Project"
processed_dir = os.path.join(project_root, "data", "processed")
figures_dir = os.path.join(project_root, "figures")
os.makedirs(figures_dir, exist_ok=True)


final_df = pd.read_csv(os.path.join(processed_dir, "final_merged_data_complete.csv"))
qs_df = pd.read_csv(os.path.join(processed_dir, "qs_top100_cleaned.csv"))


avg_edu_spending = final_df.groupby("Country Name")["Education Expenditure (% of GDP)"].mean().reset_index()
avg_edu_spending.rename(columns={"Education Expenditure (% of GDP)": "Avg Education Expenditure (% of GDP)"}, inplace=True)


qs_count = qs_df["Country Name"].value_counts().reset_index()
qs_count.columns = ["Country Name", "QS Top 100 Count"]


data = avg_edu_spending.merge(qs_count, on="Country Name", how="left")


latest_gdp = final_df[final_df["Year"] == 2022][["Country Name", "GDP (current US$)"]]
data = data.merge(latest_gdp, on="Country Name", how="left")


plt.figure(figsize=(14, 10))
qs_sorted = qs_count.sort_values("QS Top 100 Count", ascending=False)
sns.barplot(x="QS Top 100 Count", y="Country Name", data=qs_sorted, palette="Blues_r")
plt.title("QS Top 100 University Distribution by Country", fontsize=16)
plt.xlabel("QS Top 100 Count", fontsize=14)
plt.ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "qs_distribution.png"))
plt.close()


plt.figure(figsize=(10, 8))
sns.regplot(x="Avg Education Expenditure (% of GDP)", y="QS Top 100 Count", data=data, scatter=True)
texts = []
for _, row in data.iterrows():
    texts.append(plt.text(row["Avg Education Expenditure (% of GDP)"], row["QS Top 100 Count"], row["Country Name"], fontsize=8))
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
plt.title("Education Spending (Avg 2018-2022) vs QS Top 100 Universities", fontsize=16)
plt.xlabel("Average Education Expenditure (% of GDP)", fontsize=14)
plt.ylabel("QS Top 100 Count", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "spending_vs_qs.png"))
plt.close()


plt.figure(figsize=(16, 8))
sns.lineplot(data=final_df, x="Year", y="Education Expenditure (% of GDP)", hue="Country Name", marker="o")
plt.title("Education Expenditure (% of GDP) Trend (2018–2022)", fontsize=16)
plt.ylabel("Education Expenditure (% of GDP)", fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "education_trend.png"))
plt.close()


plt.figure(figsize=(12, 8))
sns.scatterplot(
    x="Avg Education Expenditure (% of GDP)",
    y="QS Top 100 Count",
    size="GDP (current US$)",
    hue="Country Name",
    data=data,
    sizes=(50, 2000),
    alpha=0.7,
    legend=False
)
texts = []
for _, row in data.iterrows():
    texts.append(plt.text(row["Avg Education Expenditure (% of GDP)"], row["QS Top 100 Count"], row["Country Name"], fontsize=8))
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
plt.title("Education Spending vs QS Top 100 vs GDP Size (Bubble Chart)", fontsize=16)
plt.xlabel("Average Education Expenditure (% of GDP)", fontsize=14)
plt.ylabel("QS Top 100 Count", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "bubble_qs_gdp.png"))
plt.close()

print(" All visualizations have been regenerated and saved to /figures/")


