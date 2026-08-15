from google.genai import types
import joblib
from pathlib  import Path
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from  google import genai
import os
from datetime import datetime



script = Path(__file__).resolve().parent


root = script.parent


pipeline = joblib.load(root/"models"/"churn_prediction_pipeline.pkl")
FEATURE_NAMES = pipeline.named_steps['preprocessor'].get_feature_names_out()
rf_model = pipeline.named_steps['model']
GLOBAL_IMPORTANCE = dict(zip(FEATURE_NAMES, rf_model.feature_importances_))



cluster_df = pd.read_csv(root/"data"/"cleaned_data"/"cluster_churn_summary.csv")



def get_cluster_churn_data(cluster_id: int = None) -> dict:
    """
    If cluster_id is given, return that one cluster.
    If cluster_id is None, return ALL clusters (for comparison questions).
    """
    if cluster_id is not None:
        row = cluster_df[cluster_df["cluster"] == cluster_id]
        if row.empty:
            return {"error": f"Cluster {cluster_id} not found."}
        return row.to_dict(orient="records")[0]
    else:
        return cluster_df.to_dict(orient="records")




# Tool 1
cluster_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_cluster_churn_data",
            description="Returns churn statistics for customer segments/clusters, including"
                "total customers, churned customers, churn rate %, stay rate %, and risk category."
                "Call with no cluster_id to get ALL clusters (for comparisons or overview questions)."
                "Call with a specific cluster_id to get just that one segment.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "cluster_id": types.Schema(
                        type="INTEGER",
                        description="Optional. The specific cluster number (0, 1, 2, or 3) to look up. Omit to get all clusters."
                    )
                },
                required=[]
            )
        )
    ]
)


numeric_cols = ['age','days_since_last_login','avg_time_spent','avg_transaction_value',
                'avg_frequency_login_days','points_in_wallet','churn_risk_score']


categorical_cols = ['region_category','membership_category'
                    ,'joined_through_referral','preferred_offer_types',
                    'medium_of_operation','internet_option',
                    'used_special_discount','complaint_status','feedback']

df = pd.read_csv(root/"data"/"cleaned_data"/'clean_clustered.csv')

# predict the churn drivers
def get_churn_drivers_by_cluster(df: pd.DataFrame, numeric_cols: list,
                                categorical_cols: list, top_n: int = 5) -> dict:
    """
    For every cluster, finds the top features most associated with churn
    by comparing churned vs stayed customers WITHIN that cluster.

    df: full dataframe with 'cluster' and 'churn' columns
    Returns: dict keyed by cluster_id, each containing churn stats + top driving features
    """

    results = {}

    for cluster_id in sorted(df["cluster"].unique()):
        cluster_df = df[df["cluster"] == cluster_id]
        churned = cluster_df[cluster_df["churn_risk_score"] == 1]
        stayed = cluster_df[cluster_df["churn_risk_score"] == 0]

        total = len(cluster_df)
        churn_rate = round((len(churned) / total) * 100, 2) if total > 0 else 0

        feature_impact = []

        # --- Numeric features: compare mean(churned) vs mean(stayed) ---
        for col in numeric_cols:
            if churned[col].isnull().all() or stayed[col].isnull().all():
                continue
            churned_mean = churned[col].mean()
            stayed_mean = stayed[col].mean()
            pooled_std = cluster_df[col].std()

            if pooled_std == 0 or np.isnan(pooled_std):
                continue

            # effect size: how many std-devs apart are churners vs stayers on this feature
            effect_size = abs(churned_mean - stayed_mean) / pooled_std

            feature_impact.append({
                "feature": col,
                "type": "numeric",
                "churned_avg": round(churned_mean, 2),
                "stayed_avg": round(stayed_mean, 2),
                "effect_size": round(effect_size, 3),
                "direction": "higher in churners" if churned_mean > stayed_mean else "lower in churners"
            })

        # --- Categorical features: compare dominant value proportions ---
        for col in categorical_cols:
            if churned.empty or stayed.empty:
                continue
            churned_dist = churned[col].value_counts(normalize=True)
            stayed_dist = stayed[col].value_counts(normalize=True)

            # find the value with the biggest gap between churners and stayers
            all_values = set(churned_dist.index) | set(stayed_dist.index)
            biggest_gap = 0
            biggest_gap_value = None

            for val in all_values:
                churn_pct = churned_dist.get(val, 0) * 100
                stay_pct = stayed_dist.get(val, 0) * 100
                gap = abs(churn_pct - stay_pct)
                if gap > biggest_gap:
                    biggest_gap = gap
                    biggest_gap_value = val

            if biggest_gap_value is not None:
                feature_impact.append({
                    "feature": col,
                    "type": "categorical",
                    "dominant_value": biggest_gap_value,
                    "pct_among_churners": round(churned_dist.get(biggest_gap_value, 0) * 100, 2),
                    "pct_among_stayers": round(stayed_dist.get(biggest_gap_value, 0) * 100, 2),
                    "effect_size": round(biggest_gap / 100, 3)  # normalize to comparable scale
                })

        # --- Rank all features by effect size, take top N ---
        top_drivers = sorted(feature_impact, key=lambda x: x["effect_size"], reverse=True)[:top_n]

        results[int(cluster_id)] = {
            "cluster_id": int(cluster_id),
            "total_customers": total,
            "churned_customers": int(len(churned)),
            "churn_rate_pct": churn_rate,
            "top_churn_drivers": top_drivers
        }

    return results


churn_drivers = get_churn_drivers_by_cluster(df, numeric_cols, categorical_cols, top_n=5)
import json
with open(root/"data"/"cleaned_data"/"cluster_churn_drivers.json", "w") as f:
    json.dump(churn_drivers, f, indent=2)
print(f"Saved Churn_drivers per cluster successfully at {root/'data'/'cleaned_data'/'cluster_churn_drivers.json'} 💾")


with open(root/"data"/"cleaned_data"/"cluster_churn_drivers.json", "r") as f:
    CLUSTER_DRIVERS_DATA = json.load(f)


def get_cluster_churn_drivers(cluster_id: int = None) -> dict:
    """
    Returns churn statistics AND the top features driving churn for a specific cluster.
    If cluster_id is None, returns data for ALL clusters (for comparison questions).
    """
    if cluster_id is not None:
        data = CLUSTER_DRIVERS_DATA.get(str(cluster_id))
        if data is None:
            return {"error": f"Cluster {cluster_id} not found."}
        return data
    else:
        return list(CLUSTER_DRIVERS_DATA.values())


# Tool 2
churn_drivers_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_cluster_churn_drivers",
            description=(
                "Returns detailed churn statistics for customer segments/clusters, including "
                "total customers, churn rate, and the TOP FEATURES that specifically separate "
                "customers who churned from customers who stayed within that segment. "
                "Use this when the user asks WHY a segment churns, what drives churn in a "
                "segment, or wants root-cause analysis. "
                "Call with no cluster_id to compare ALL clusters. "
                "Call with a specific cluster_id (0, 1, 2, or 3) for just that segment."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "cluster_id": types.Schema(
                        type="INTEGER",
                        description="Optional. Specific cluster number to analyze. Omit for all clusters."
                    )
                },
                required=[]
            )
        )
    ]
)


def extract_features_from_prompt(text: str) -> dict:
    """Extract age and days since last login from user prompt using simple regex."""
    features = {}
    # Age patterns: "age 25", "age: 30", "25 years old", "I am 25"
    age_patterns = [
        r'age\s*[:\-]?\s*(\d+)',
        r'(\d+)\s*years?\s*old',
        r'I\s*am\s*(\d+)',
        r'I\s*\'?m\s*(\d+)'
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            features['age'] = int(match.group(1))
            break
    # Days since last login patterns: "logged in 5 days ago", "days since login: 3", "last login 2 days"
    login_patterns = [
        r'logged?\s*in\s*(\d+)\s*days?\s*ago',
        r'days?\s*since\s*last\s*login\s*[:\-]?\s*(\d+)',
        r'last\s*login\s*(\d+)\s*days?',
        r'(\d+)\s*days?\s*since\s*login'
    ]
    for pattern in login_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            features['days_since_last_login'] = int(match.group(1))
            break
    return features


def predict_churn_probability(customer_features: dict) -> float:
    """Predicts churn probability for a new customer using your trained model"""
    global pipeline  # Your loaded RandomForest pipeline
    features_df = pd.DataFrame([customer_features])
    return float(pipeline.predict_proba(features_df)[0][1])  # Returns probability [0,1]

churn_prediction_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="predict_churn_probability",
            description="Predicts churn probability for a NEW customer given their features (age, login frequency, transaction history, etc.)",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "age": types.Schema(type="INTEGER"),
                    "days_since_last_login": types.Schema(type="INTEGER"),
                    # Add other features your model expects
                },
                required=["age", "days_since_last_login"]  # List all required features
            )
        )
    ]
)


root_env = Path.cwd().resolve().parent/ ".env"
load_dotenv(dotenv_path=root_env)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_instruction = """You are a customer retention analyst. When answering questions about
customer segments, always ground your answer strictly in the tool data provided — never invent numbers.

When asked to analyze or predict for a segment, structure your answer as:

## Segment Overview(Explain the segmentation in 2-3 lines concrete and focused)
## Churn Probability(provide accurate numbers as per the tool provided)
## Risk Level(Highlight the most important risky churns and immediate actions to be taken for them)
## Suggested Retention Actions(Provided realistic optimistic at present suggestions to prevent churn!)
(10 concrete, specific actions appropriate to the risk level — more urgent/aggressive actions for
higher-risk segments, lighter-touch actions for lower-risk segments)

When asked for analysis and results for most important churn features or reasons per clusters

## When explaining WHY a segment churns, cite the specific features and their actual values
from the tool data (e.g., "customers who churned logged in far less often: 2.1 days vs 9.8 days
for those who stayed").

Structure segment analysis answers as:
## Segment Overview
## Churn Rate
## Root Causes (with real numbers)
Use BOTH tools together if the question needs stats AND causes.
1. get_cluster_churn_data - For questions about existing segments
2. get_cluster_churn_drivers - For root-cause analysis of segment churn
3. predict_churn_probability - For predicting churn risk for NEW customers
Use cluster tools for questions like: "What are the characteristics of high-risk segments?"
Use prediction tool for questions like: "What's the churn risk for a 35-year-old customer who logged in 2 days ago?"
"""
all_tools = [cluster_tool, churn_drivers_tool, churn_prediction_tool]

TOOL_FUNCTIONS = {
    "get_cluster_churn_data": get_cluster_churn_data,
    "get_cluster_churn_drivers": get_cluster_churn_drivers,
    "predict_churn_probability": predict_churn_probability
}

def ask_cluster_agent(user_question: str):
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=user_question)])
    ]

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(tools=all_tools, system_instruction=system_instruction)
    )

    part = response.candidates[0].content.parts[0]

    while part.function_call:
        contents.append(response.candidates[0].content)

        fn_name = part.function_call.name
        args = dict(part.function_call.args)
        cluster_id = args.get("cluster_id")
        print(f"[Tool call] {fn_name}({args})")

        # Explicit dispatch by name, as you wanted                      
        if fn_name == "get_cluster_churn_data":
            tool_result = get_cluster_churn_data(cluster_id)
        elif fn_name == "get_cluster_churn_drivers":
            tool_result = get_cluster_churn_drivers(cluster_id)
        elif fn_name == "predict_churn_probability":
            # Extract features from the user prompt and call the prediction tool
            features = extract_features_from_prompt(user_question)
            # If we couldn't extract required features, return an error
            if not features.get('age') is not None or not features.get('days_since_last_login') is not None:
                tool_result = {"error": "Could not extract age and/or days since last login from your question. Please phrase like: 'What is the churn risk for a 35-year-old customer who logged in 2 days ago?'"}
            else:
                tool_result = predict_churn_probability(features)
        else:
            tool_result = {"error": f"Unknown tool: {fn_name}"}

        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_function_response(name=fn_name, response={"result": tool_result})]
            )
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(tools=all_tools, system_instruction=system_instruction)
        )
        part = response.candidates[0].content.parts[0]

    return response.text


message  = input("Enter prompt : ")

answer = ask_cluster_agent(message)
print(answer)

SAVE_FOLDER = root / "models" / "gemini-response"
SAVE_FOLDER.mkdir(parents=True, exist_ok=True)

def save_response_to_file(response_text: str) -> str:
    """Saves the generated report to a markdown file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = uuid.uuid4().hex[:6]
    filename = f"churn_report_{timestamp}_{random_suffix}.md"
    filepath = SAVE_FOLDER / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response_text)

    return str(filepath)





file_path = save_response_to_file(answer)