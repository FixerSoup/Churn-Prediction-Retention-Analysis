"""
This script trains the model on the cleaned dataset
"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split as tts
from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt 
import seaborn as sns

script = Path(__file__).resolve().parent
root = script.parent

# load data
data = pd.read_csv(root/"data"/"cleaned_data"/'clean_clustered.csv')

# features used for training
x = data.drop(columns = ['churn_risk_score'])

# label /target 
y = data['churn_risk_score']

# split the data into training and test set
x_train,x_test,y_train,y_test = tts(x,y,test_size = 0.4,random_state = 42,stratify = y)

# take all the numbers
numerical_cols = x_train.select_dtypes(exclude = 'object').columns.tolist()
# take all the categoricals 
categorical_cols = x_train.select_dtypes(include = 'object').columns.to_list()

#use a encoder
encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

# Make a copy
x_train_encoded = x_train.copy()
x_test_encoded = x_test.copy()

#Encoder it
x_train_encoded[categorical_cols] = encoder.fit_transform(x_train[categorical_cols])
x_test_encoded[categorical_cols] = encoder.transform(x_test[categorical_cols])


# Make the model object
rf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')

# Train the model 
rf.fit(x_train_encoded, y_train)

# Test it 
rf_predictions = rf.predict(x_test_encoded)
rf_probabilities = rf.predict_proba(x_test_encoded)

print("Predictions : ")
print(rf_predictions[:10])

print("Probabilities")
print(rf_probabilities[:10])

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
print("\n------------------ RandomForest ------------------------")
print("Accuracy:", accuracy_score(y_test, rf_predictions))
print(classification_report(y_test, rf_predictions))

preview = pd.DataFrame({
    'actual': y_test.values[:15],
    'predicted': rf_predictions[:15],
    'prob_stay': rf_probabilities[:15, 0],
    'prob_churn': rf_probabilities[:15, 1]
})
preview['correct'] = preview['actual'] == preview['predicted']

print(preview)

preprocessor = ColumnTransformer(transformers=[
    ('cat',OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1),categorical_cols),
    ('num',StandardScaler(),numerical_cols)
])

full_pipeline = Pipeline(
    steps=[
        ('preprocessor',preprocessor),
        ('model',RandomForestClassifier(n_estimators=200,random_state = 42,class_weight = 'balanced'))
    ]
)

full_pipeline.fit(x_train,y_train)

joblib.dump(full_pipeline,root/"models"/'churn_prediction_pipeline.pkl')
print(f"Successfully saved the model to {root/"models"/'churn_model_pipeline.pkl'} ✅")

def model_performance_report(model,x_test,y_test):
    prediction = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:,1]
    print("=" * 50)
    print("HEADLINE NUMBERS")
    print("=" * 50)
    print(f"Accuracy : {accuracy_score(y_test,prediction):.3f}")
    print(f"Precision : {precision_score(y_test,prediction):.3f}")
    print(f"Recall : {recall_score(y_test,prediction):.3f}")

    print("\n" + "=" * 50)
    print("FULL BREAKDOWN BY CLASS")
    print("=" * 50)
    print(classification_report(y_test, prediction, target_names=['Stayed', 'Churned']))
    cm = confusion_matrix(y_test,prediction)
    plt.figure(figsize = (6,5))
    sns.heatmap(cm,annot = False,fmt = 'd',cmap = 'Reds',
    xticklabels  = ['Predicted : stay','Predicted : churn'],
    yticklabels = ['Actual :stay','Actual : churn']
    )
    plt.title('Confusion Matrix')
    plt.show()
    fpr, tpr, _ = roc_curve(y_test, probabilities)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc_score(y_test, probabilities):.3f}", color='steelblue')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random guessing')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend()
    plt.show()

model_performance_report(full_pipeline, x_test, y_test)

# Checking model performance by % of churns

total_customers = len(y_test)

predicted_churn_count =  (rf_predictions==1).sum()
actual_churn_count = (y_test==1).sum()

predicted_churn_pct = (predicted_churn_count/total_customers) *100
actual_churn_pct = (actual_churn_count/total_customers) *100

print("=" * 50)
print("CHURN SUMMARY (Business View)")
print("=" * 50)
print(f"Total customers analyzed     : {total_customers}")
print(f"Actual churn rate            : {actual_churn_pct:.2f}%  ({actual_churn_count} customers)")
print(f"Model-predicted churn rate   : {predicted_churn_pct:.2f}%  ({predicted_churn_count} customers)")
print("=" * 50)


# Feature importance
importances = rf.feature_importances_
rf_model = full_pipeline.named_steps['model']
preprocessor_fitted = full_pipeline.named_steps['preprocessor']
# Find the feature names
feature_names = preprocessor_fitted.get_feature_names_out()
feature_importance_df = pd.DataFrame(
{ "Feature": feature_names,
    "Importance" : importances  
}).sort_values(by="Importance",ascending = False)

print(feature_importance_df.head(10).to_string(index=False))
print(feature_importance_df.shape)
feature_importance_df.to_csv(root/"data"/"cleaned_data"/"feature_importance.csv",index = False)
print(f"Successfully saved feature_importance to {root/"data"/"cleaned_data"/"feature_importance.csv"} ✅")