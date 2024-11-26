import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the dashboard
st.title("Financial Insights Dashboard")

# Upload dataset
uploaded_file = st.file_uploader("Upload family financial and transaction data", type="xlsx")

if uploaded_file:
    # Load data
    data = pd.read_excel(uploaded_file)
    st.subheader("Uploaded Dataset")
    st.dataframe(data.head())

    # Process data
    family_data = data.groupby('Family ID').agg({
        'Income': 'sum',
        'Monthly Expenses': 'sum',
        'Savings': 'sum',
        'Loan Payments': 'sum',
        'Credit Card Spending': 'sum',
        'Financial Goals Met (%)': 'mean'
    }).reset_index()

    # Add derived metrics
    family_data['Savings-to-Income Ratio'] = family_data['Savings'] / family_data['Income']
    family_data['Expenses-to-Income Ratio'] = family_data['Monthly Expenses'] / family_data['Income']
    family_data['Loan-to-Income Ratio'] = family_data['Loan Payments'] / family_data['Income']

    # Scoring function
    def calculate_financial_score(row):
        weights = {
            'savings_to_income_ratio': 0.4,
            'expenses_to_income_ratio': 0.2,
            'loan_to_income_ratio': 0.15,
            'credit_card_spending': 0.1,
            'goals_met': 0.15
        }

        score = (
            weights['savings_to_income_ratio'] * min(row['Savings-to-Income Ratio'] * 100, 100) +
            weights['expenses_to_income_ratio'] * max(0, 100 - row['Expenses-to-Income Ratio'] * 100) +
            weights['loan_to_income_ratio'] * max(0, 100 - row['Loan-to-Income Ratio'] * 100) +
            weights['credit_card_spending'] * max(0, 100 - row['Credit Card Spending'] / 1000) +  # Adjust as needed
            weights['goals_met'] * row['Financial Goals Met (%)']
        )
        return min(100, max(0, score))  # Ensure score is within 0-100

    # Apply the scoring function
    family_data['Financial Score'] = family_data.apply(calculate_financial_score, axis=1)

    # Display processed data and scores
    st.subheader("Processed Family Data with Financial Scores")
    st.dataframe(family_data)

    # Visualization 1: Financial Score Distribution
    st.subheader("Financial Score Distribution")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Family ID', y='Financial Score', data=family_data, palette="viridis")
    plt.title("Financial Scores by Family")
    plt.xlabel("Family ID")
    plt.ylabel("Financial Score")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Visualization 2: Monthly Expenses by Family
    st.subheader("Monthly Expenses by Family")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Family ID', y='Monthly Expenses', data=family_data, palette="coolwarm")
    plt.title("Monthly Expenses by Family")
    plt.xlabel("Family ID")
    plt.ylabel("Monthly Expenses")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Visualization 3: Savings-to-Income Ratio Distribution
    st.subheader("Savings-to-Income Ratio by Family")
    plt.figure(figsize=(15, 8))
    sns.barplot(x='Family ID', y='Savings-to-Income Ratio', data=family_data, palette="Blues")
    plt.title("Savings-to-Income Ratio by Family")
    plt.xlabel("Family ID")
    plt.ylabel("Savings-to-Income Ratio")
    plt.xticks(rotation=45)
    st.pyplot(plt)

else:
    st.write("Please upload a dataset to begin.")
