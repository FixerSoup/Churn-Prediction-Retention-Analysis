"""
The dataset for this project is used from HuggingFace Churn Dataset
Source : https://huggingface.co/datasets/d0r1h/customer_churn
"""
import os
from datasets import load_dataset
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from huggingface_hub import login
load_dotenv()

token_id = os.getenv("HF_TOKEN")

if token_id:
    login(token=token_id)
    print("Successfully Logged In ✅")
else:
    print("❌ HF_TOKEN not Found!")

dataset = load_dataset("d0r1h/customer_churn")
df = pd.DataFrame(dataset['train'])
print('-------------------------------------------------------------------------------------------')
print("Dataset Loaded Successfully ✅")
print('-------------------------------------------------------------------------------------------')
print(df.head())
print('-------------------------------------------------------------------------------------------')
print("Column Info : ")
print('-------------------------------------------------------------------------------------------')
print(df.info())
print('-------------------------------------------------------------------------------------------')
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")
print('-------------------------------------------------------------------------------------------')
print("Statistical Info : ")
print('-------------------------------------------------------------------------------------------')
print(df.describe())

script = Path(__file__).resolve().parent
root = script.parent
df.to_csv(root/"data"/"raw_data"/'data.csv')
print('-------------------------------------------------------------------------------------------')
print(f"Data Successfully Saved to {root/"data"/"raw_data"/'data.csv'} ✅")
print('-------------------------------------------------------------------------------------------')