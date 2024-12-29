import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import zscore

st.set_page_config(page_title="Transaction Analysis Dashboard", layout="wide")

data = pd.read_excel('https://github.com/abdullah-naqvi/aiassignment/raw/refs/heads/main/Enhanced_Dummy_HBL_Data.xlsx')

st.sidebar.header("Filters")
region_filter = st.sidebar.multiselect("Select Region", options=data['Region'].unique(), default=data['Region'].unique())
filtered_data = data[data['Region'].isin(region_filter)]

st.title("Transaction Analysis Dashboard")

account_type_distribution = filtered_data['Account Type'].value_counts()
fig1 = px.pie(values=account_type_distribution, names=account_type_distribution.index, title="Account Type Distribution")
st.plotly_chart(fig1, use_container_width=True)

top_beneficiary_banks = (filtered_data.groupby(['Region', 'Transaction To'])['Credit']
                        .sum()
                        .reset_index()
                        .sort_values(['Region', 'Credit'], ascending=[True, False])
                        .groupby('Region').head(5))
fig2 = px.bar(top_beneficiary_banks, x='Transaction To', y='Credit', color='Region', title="Top Beneficiary Banks by Credit Transactions")
st.plotly_chart(fig2, use_container_width=True)

transaction_intensity = filtered_data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()
fig3 = px.density_heatmap(transaction_intensity, x='Region', y='Credit', z='Debit', title="Geographic Heatmap of Transactions")
st.plotly_chart(fig3, use_container_width=True)

filtered_data['Credit_Z'] = zscore(filtered_data['Credit'])
filtered_data['Debit_Z'] = zscore(filtered_data['Debit'])
anomalies = filtered_data[(filtered_data['Credit_Z'].abs() > 3) | (filtered_data['Debit_Z'].abs() > 3)]
fig4 = px.scatter(anomalies, x='Credit', y='Debit', color='Account Type', title="Anomalies in Transactions")
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.box(filtered_data, x='Account Type', y='Credit', color='Account Type', title="Distribution of Credit Transactions by Account Type")
st.plotly_chart(fig5, use_container_width=True)

if 'Time' in filtered_data.columns:
    time_series = filtered_data.groupby('Time')[['Credit', 'Debit']].sum().reset_index()
    fig6 = px.line(time_series, x='Time', y=['Credit', 'Debit'], title="Transaction Trends Over Time")
    st.plotly_chart(fig6, use_container_width=True)

if 'Customer Type Description' in filtered_data.columns:
    customer_insights = filtered_data.groupby('Customer Type Description')[['Credit', 'Debit']].sum().reset_index()
    fig7 = px.bar(customer_insights, x='Customer Type Description', y=['Credit', 'Debit'], title="Customer Insights: Total Credit and Debit")
    st.plotly_chart(fig7, use_container_width=True)
