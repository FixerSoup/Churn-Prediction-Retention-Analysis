import pandas as pd
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from pathlib import Path
import matplotlib.pyplot as plt
script = Path(__file__).resolve().parent
root = script.parent

# Load your clustered dataset
df = pd.read_csv(root/"data"/"cleaned_data"/'clean_clustered.csv')
cluster_churn_summary = df.groupby('cluster')['churn_risk_score'].agg(
    total_customers = 'count',
    churned_customers = 'sum'
)

cluster_churn_summary["churn_rate_%"] = (
    cluster_churn_summary["churned_customers"] / cluster_churn_summary["total_customers"] * 100
).round(2)

cluster_churn_summary["stay_rate_%"] = (100 - cluster_churn_summary["churn_rate_%"]).round(2)

cluster_churn_summary = cluster_churn_summary.sort_values(by="churn_rate_%", ascending=False)

cluster_churn_summary['risk_category'] = pd.cut(
    cluster_churn_summary['churn_rate_%'],
    bins=[0, 20, 40, 60, 80, 100],
    labels=[
        'Least Risk',
        'Lower Risk',
        'Medium Risk',
        'Risky',
        'High Risk'
    ],
    include_lowest=True
)

print(cluster_churn_summary)
cluster_churn_summary.to_csv(root/"data"/"cleaned_data"/"cluster_churn_summary.csv")
print(f"Successfully saved cluster churn summary to {root/"data"/"cleaned_data"/"cluster_churn_summary.csv"} ✅")

plt.figure(figsize=(9, 5))
bars = plt.bar(cluster_churn_summary.index.astype(str), cluster_churn_summary['churn_rate_%'],
                color=['#e34948' if x >= 60 else '#eda100' if x >= 40 else '#2a78d6' for x in cluster_churn_summary['churn_rate_%']])
plt.xlabel('Cluster')
plt.ylabel('Churn rate (%)')
plt.title('Churn rate by cluster, with risk category')

for bar, category in zip(bars, cluster_churn_summary['risk_category']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, category,
            ha='center', fontsize=8, rotation=0)

plt.tight_layout()
plt.savefig(root/"charts"/'cluster_churn_summary.png')
print(f"Successfully Saved chart to {root/"charts"/'cluster_churn_summary.png'} ✅")
plt.show()