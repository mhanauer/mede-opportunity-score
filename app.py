import pandas as pd
import numpy as np
import streamlit as st

# Set the random seed for reproducibility
np.random.seed(42)

# Generate the initial dataset
n = 1000  # Number of data points
data = {
    'Member ID': np.arange(1, n + 1),
    'Age': np.random.randint(18, 90, size=n),
    'Gender': np.random.choice(['Male', 'Female'], size=n),
    'Number of Chronic Conditions': np.random.randint(0, 6, size=n),
    'Generic Rate': np.random.randint(0, 101, size=n),
    'Total Claims': np.random.randint(1, 501, size=n),
    'Inpatient Percent': np.random.randint(0, 101, size=n)
}

df = pd.DataFrame(data)

# Generate predicted values by applying a random change
df['Generic Rate Predicted'] = df['Generic Rate'] + np.random.randint(-10, 11, size=n)
df['Total Claims Predicted'] = df['Total Claims'] + np.random.randint(-50, 51, size=n)
df['Inpatient Percent Predicted'] = df['Inpatient Percent'] + np.random.randint(-10, 11, size=n)

# Calculate adjusted values
df['Generic Rate Adjusted'] = df['Generic Rate'] - df['Generic Rate Predicted']
df['Total Claims Adjusted'] = df['Total Claims'] - df['Total Claims Predicted']
df['Inpatient Percent Adjusted'] = df['Inpatient Percent'] - df['Inpatient Percent Predicted']

# Calculate standardized adjusted values
df['Generic Rate Adjusted Standardized'] = (df['Generic Rate Adjusted'] - df['Generic Rate Adjusted'].mean()) / df['Generic Rate Adjusted'].std()
df['Total Claims Adjusted Standardized'] = (df['Total Claims Adjusted'] - df['Total Claims Adjusted'].mean()) / df['Total Claims Adjusted'].std()
df['Inpatient Percent Adjusted Standardized'] = (df['Inpatient Percent Adjusted'] - df['Inpatient Percent Adjusted'].mean()) / df['Inpatient Percent Adjusted'].std()

# Reverse the standardized scores for Total Claims and Inpatient Percent
df['Total Claims Adjusted Standardized'] *= -1
df['Inpatient Percent Adjusted Standardized'] *= -1

# Calculate the Mede Opportunity Score
df['Mede Opportunity Score'] = (
    df['Generic Rate Adjusted Standardized'] +
    df['Total Claims Adjusted Standardized'] +
    df['Inpatient Percent Adjusted Standardized']
)

# Round all numerical values to 2 decimal places
df = df.round(2)

# Streamlit app
st.title("Mede Opportunity Score Example")

# Add explanatory text
st.write("""
Below we show the Mede Opportunity Score. This score takes multiple quality and cost aspects of members, adjusts, normalizes, and sums them to create a composite score. Negative values mean members are below average, and positive values mean members are above average relative to other members.
""")

# Display the dataframe
st.dataframe(df)

