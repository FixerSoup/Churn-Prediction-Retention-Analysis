# Customer Segmentation & Churn Prediction

![Churn Workflow Banner](churn_workflow_banner.svg)

![Churn Prediction Animation](churn_prediction_animation.svg)

![Space README Banner](space_readme_banner.svg)

A focused project that segments customers, predicts churn, and lets you ask questions in plain English.

## What it does
- **Cleans & engineers features** from raw data (RFM, login, transaction stats).
- **Trains a churn prediction model** (RandomForest pipeline) saved as `models/churn_prediction_pipeline.pkl`.
- **Analyzes segments**: gives cluster‑level churn rates and the top features that drive churn in each segment.
- **Powers a Gemini agent** that answers:
  - *About segments*: “What are the traits of high‑risk clusters?”
  - *About a new customer*: “What’s the churn chance for a 35‑year‑old who logged in 2 days ago?”
- **Includes a Gradio demo** for quick interaction.

## Key features
- End‑to‑end pipeline: data → model → insights → natural‑language Q&A.
- Uses the trained model both for segment summaries and real‑time individual predictions.
- Simple, dependency‑light setup (see `requirements.txt`).

## Basic terms (short & precise)
- **Churn**: Customer leaves or stops using the service.
- **Segmentation**: Grouping customers with similar behavior.
- **Feature**: Measurable input for the model (e.g., age, days since last login).
- **Model**: Algorithm that learns patterns to predict churn.
- **Probability**: Estimated chance of churn (0 = never, 1 = certain).

## Prerequisites
- **Ollama** installed locally (to run local models if needed)
- A **GEMINI API KEY** set in a `.env` variable `GEMINI_API_KEY`
- Access to a free open cloud model such as **nemotron-3-super:cloud** (ensure it’s available in your model provider)

## Claude Code Subscription Note
If you already have a Claude Code subscription, you can use the agent directly without additional setup.  
If you do not have a subscription and want to use the agent for free, follow the prerequisites and steps above.

## How to run
1. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your Gemini key:  
   ```bash
   GEMINI_API_KEY=your_key_here
   ```
3. Launch the agent (or demo)  
   ```bash
   python scripts/tool_develop.py   # interactive console
   # or
   python gradio/app.py             # Gradio web UI
   ```

## Files you’ll see
- `data/raw_data/` – original CSV (untouched).
- `data/cleaned_data/` – cleaned, clustered data and feature importance.
- `models/` – trained model and Gemini‑generated reports.
- `scripts/` – training (`train_model.py`), agent (`tool_develop.py`), utilities.
- `notebooks/` – exploratory work (EDA, clustering, RFM).
- `gradio/` – simple web interface.

## Claude Code Skills
The project includes custom Claude Code skills to streamline common tasks:

- **`/generate-churn-report`** – Produces a full churn analysis report (executive summary, segmentation, drivers, model performance, recommendations) and saves it as Markdown/PDF.
- **`customer-segmentation-retention`** – Provides end‑to‑end project guidance and best‑practice explanations for every stage of the workflow.
- **`train model`** – Helper skill that walks you through model training, hyper‑parameter tuning, and evaluation.

### Using a skill in Claude Code CLI
1. Make sure your virtual environment is activated and you are in the project root.
2. In the Claude Code chat, type the skill name preceded by a slash, e.g.:
   ```
   /generate-churn-report
   ```
3. Claude will execute the skill’s defined steps (loading data, running scripts, generating the report) and return the output.
4. The resulting Markdown report appears in `models/gemini-response/`; a PDF version (if requested) is placed in `models/reports/`.

You can also invoke the skill manually via the agent:
```bash
python scripts/run_agent.py
```
Then, when prompted, ask for a churn report (e.g., “Generate a detailed churn report that includes an executive summary, segmentation analysis, churn drivers per cluster, model performance, feature importance, and retention recommendations.”).

That’s it—short, churn‑focused, and ready to use.