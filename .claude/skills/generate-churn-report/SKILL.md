---
name: generate-churn-report
description: >
  Skill for generating a comprehensive churn report. This skill defines the
  standard structure, required analyses, and output artifacts for a churn
  report in the Customer Segmentation and Retention Analysis project.
  Use this skill whenever the user requests a churn report, summary, or
  executive overview of churn insights.
---

# Generate Churn Report — Skill

## 🎯 Skill Purpose

This skill ensures that every churn report produced for this project contains:

- **Executive summary** with key metrics and high‑risk segments  
- **Data overview** (size, time period, churn rate)  
- **Segmentation analysis** (cluster profiles, sizes, churn rates, risk categories)  
- **Churn drivers** (top features separating churners from stayers per segment)  
- **Model performance** (if a predictive model is trained: ROC‑AUC, precision/recall, confusion matrix)  
- **Feature importance** (global and per‑segment)  
- **Retention recommendations** (actionable, risk‑tiered)  
- **Visualizations** (charts saved as PNG and embedded in the report)  
- **Appendix** (raw tables, feature lists, etc.)

The report is generated as a Markdown file and optionally converted to PDF.

---

## 📋 Standard Report Structure

A complete churn report MUST contain the following sections (in this order):

1. **Title Page**  
   - Report title: `Customer Churn Analysis Report`  
   - Date of generation  
   - Project name: `Customer Segmentation and Retention Analysis`  
   - Analyst / model version (if applicable)

2. **Executive Summary** (½‑1 page)  
   - Overall churn rate (%)  
   - Number of customers analyzed  
   - Top‑risk segment (cluster ID, churn rate, size)  
   - One‑sentence insight on the biggest churn driver  
   - High‑level recommendation (e.g., “Focus retention efforts on Cluster 2”)

3. **Data Overview**  
   - Date range of data  
   - Total rows and columns  
   - Churn/distribution (count and %)  
   - Missing data summary  

4. **Segmentation Analysis**  
   - Description of clustering method used (e.g., K‑means on scaled RFM)  
   - Table showing per cluster:  
     * Cluster ID  
     * Size (customers and %)  
     * Churned customers  
     * Churn rate (%)  
     * Stay rate (%)  
     * Risk category (Least/Lower/Medium/Risky/High)  
   - Bar chart of churn rate by cluster (with risk‑category labels)  

5. **Churn Drivers per Segment**  
   - For each cluster (or for all clusters if comparing):  
     * Top 5 features that differentiate churners from stayers within the cluster  
     * For numeric features: average value for churned vs stayed, effect size, direction  
     * For categorical features: dominant value, % among churners vs stayers, effect size  
   - Table or bullet list per cluster  

6. **Predictive Model Performance** (if a model was trained)  
   - Model type (e.g., Random Forest, LightGBM)  
   - Hold‑out set size  
   - Metrics: ROC‑AUC, PR‑AUC, Accuracy, Precision, Recall, F1 at chosen threshold  
   - Confusion matrix (png)  
   - ROC curve (png)  
   - Feature importance table (top 10)  

7. **Feature Importance (Global)**  
   - Bar chart of top 15 features by importance  
   - Brief interpretation of what drives churn overall  

8. **Retention Recommendations**  
   - Prioritized by risk tier (High → Low)  
   - Specific, actionable tactics (e.g., “Send personalized win‑back offer to High‑risk cluster customers who have not logged in >7 days”)  
   - Estimated impact where possible  

9. **Visualizations Appendix**  
   - List of all generated charts with captions and file paths  
   - Ensure each chart is referenced in the relevant section  

10. **Appendix (Optional)**  
   - Full segmentation table  
   - Full feature importance list  
   - Hyperparameters used  
   - Data dictionary  

---

## 🛠️ How to Generate the Report

Follow these steps to produce a churn report. All scripts assume they are run from the project root with the virtual environment activated.

### 1. Prepare the Environment

```bash
# Windows
venv\Scripts\activate.bat
# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Load (or Reload) the Data

```bash
python scripts/load_data.py
```
*This saves the raw CSV to `data/raw_data/data.csv`.*

### 3. Train the Churn Prediction Model (if not already present)

```bash
python scripts/train_model.py
```
*This outputs:*  
- `models/churn_prediction_pipeline.pkl`  
- `data/cleaned_data/feature_importance.csv`  
- Various metric prints to console  

### 4. Run Segmentation and Cluster‑Level Churn Analysis

```bash
python scripts/segmentize_customers_by_clustering.py
```
*This outputs:*  
- `data/cleaned_data/cluster_churn_summary.csv`  
- `charts/cluster_churn_summary.png`  

### 5. Generate the Markdown Report

You can use the agent (`run_agent.py`) to compile a report by asking it to summarize the findings, or you can manually assemble a Markdown file using the outputs above.

**Example prompt to the agent:**  
> “Generate a detailed churn report that includes an executive summary, segmentation analysis, churn drivers per cluster, model performance, feature importance, and retention recommendations. Use all available output files.”

Run:

```bash
python scripts/run_agent.py
```
Then paste the prompt when prompted. The agent will produce a Markdown response and save it to `models/gemini-response/`.

### 6. Convert to PDF (Optional)

If you saved the Markdown report in `models/gemini-response/`, run:

```bash
python scripts/save_to_pdf.py
```
This converts every `.md` in `models/gemini-response/` to a PDF in `models/reports/` with a timestamped filename.

---

## 📂 Expected Output Artifacts

After completing the steps above, you should have:

| Artifact | Path | Description |
|----------|------|-------------|
| Raw data | `data/raw_data/data.csv` | Original dataset |
| Cleaned data (with clusters) | `data/cleaned_data/clean_clustered.csv` | Used for segmentation and training |
| Cluster churn summary | `data/cleaned_data/cluster_churn_summary.csv` | Table of size, churn rate, risk |
| Cluster chart | `charts/cluster_churn_summary.png` | Bar chart of churn % by cluster |
| Feature importance | `data/cleaned_data/feature_importance.csv` | Global feature importances |
| Trained model | `models/churn_prediction_pipeline.pkl` | Pickled pipeline for inference |
| Model metrics | (printed to console) | ROC‑AUC, etc. |
| Markdown report | `models/gemini-response/churn_report_<timestamp>_<suffix>.md` | Full report in Markdown |
| PDF report | `models/reports/churn_report_<timestamp>_<suffix>.pdf` | PDF version (if conversion run) |
| Additional charts | (as generated by agent or scripts) | e.g., confusion matrix, ROC curve |

---

## 📝 Quality Rules

When generating a report, always:

- **Explain before showing numbers** – give context for each metric.  
- **Reference visualizations** – every chart must be mentioned in the text.  
- **Use consistent naming** – cluster IDs start at 0; risk categories as defined in `segmentize_customers_by_clustering.py`.  
- **Highlight risk tiers** – use color‑coding (red for High, orange for Risky, etc.) in tables or text.  
- **State limitations** – e.g., “Model trained on 80% of data; performance may vary on unseen segments.”  
- **Provide actionable recommendations** – avoid vague statements; tie each recommendation to a specific driver or segment.  

---

## 🔄 Update History

- **2026‑08‑15**: Initial version of the skill – defines standard churn report contents and generation workflow.  

--- 

*Use this skill as a checklist whenever you or the user asks for a churn report. Following it ensures that all reports are comparable, complete, and decision‑ready.* 