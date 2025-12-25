import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page config
st.set_page_config(page_title="Digital Payment Analytics", layout="wide", page_icon="💳")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('User Perception of Digital Payment Platforms .csv')
    df.columns = ['Timestamp', 'Username', 'Platforms_Used', 'Primary_Wallet', 'Usage_Frequency', 
                  'Most_Reliable', 'Best_Issue_Handler', 'Satisfaction', 'Data_Protection_Confidence',
                  'Most_Trusted_Security', 'Most_Innovative', 'Ease_of_Use', 'Adapts_Quickly',
                  'Would_Recommend', 'Prefer_PayPal', 'PayPal_Reason', 'Not_Switch_Reason',
                  'PayPal_Features_to_Adopt', 'Should_Adopt_PayPal_Practices']
    return df

df = load_data()

# Title
st.title("💳 Digital Payment Platforms Dashboard")
st.markdown("### User Perception Analysis")

# Filters
col1, col2 = st.columns(2)
with col1:
    platforms = ['All'] + list(df['Primary_Wallet'].unique())
    selected_platform = st.selectbox("Filter by Platform", platforms)
with col2:
    frequencies = ['All'] + list(df['Usage_Frequency'].unique())
    selected_frequency = st.selectbox("Filter by Usage Frequency", frequencies)

# Apply filters
filtered_df = df.copy()
if selected_platform != 'All':
    filtered_df = filtered_df[filtered_df['Primary_Wallet'] == selected_platform]
if selected_frequency != 'All':
    filtered_df = filtered_df[filtered_df['Usage_Frequency'] == selected_frequency]

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Responses", len(filtered_df))
with col2:
    st.metric("Platforms", df['Primary_Wallet'].nunique())
with col3:
    satisfied = len(filtered_df[filtered_df['Satisfaction'].isin(['Satisfied', 'Very satisfied'])])
    st.metric("Satisfaction Rate", f"{satisfied/len(filtered_df)*100:.1f}%")
with col4:
    daily = len(filtered_df[filtered_df['Usage_Frequency'] == 'Daily'])
    st.metric("Daily Users", daily)

# Charts
col1, col2 = st.columns(2)

with col1:
    # Primary Wallet Distribution
    st.subheader("Primary Wallet Distribution")
    wallet_counts = filtered_df['Primary_Wallet'].value_counts()
    fig1 = px.bar(x=wallet_counts.index, y=wallet_counts.values, 
                  color=wallet_counts.values,
                  color_continuous_scale='Purples')
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Satisfaction Levels
    st.subheader("Satisfaction Levels")
    sat_counts = filtered_df['Satisfaction'].value_counts()
    fig2 = px.pie(values=sat_counts.values, names=sat_counts.index, 
                  hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Usage Frequency
    st.subheader("Usage Frequency")
    freq_counts = filtered_df['Usage_Frequency'].value_counts()
    fig3 = px.bar(x=freq_counts.index, y=freq_counts.values,
                  color=freq_counts.values, color_continuous_scale='Viridis')
    fig3.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Most Trusted Security
    st.subheader("Most Trusted Security")
    trust_counts = filtered_df['Most_Trusted_Security'].value_counts().head(5)
    fig4 = px.bar(x=trust_counts.values, y=trust_counts.index, 
                  orientation='h', color=trust_counts.values,
                  color_continuous_scale='Blues')
    fig4.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig4, use_container_width=True)

# Ease of Use
st.subheader("Ease of Use by Platform")
ease_by_platform = filtered_df.groupby(['Primary_Wallet', 'Ease_of_Use']).size().reset_index(name='count')
fig5 = px.bar(ease_by_platform, x='Primary_Wallet', y='count', color='Ease_of_Use',
              barmode='group', color_discrete_sequence=px.colors.qualitative.Set2)
fig5.update_layout(height=400)
st.plotly_chart(fig5, use_container_width=True)

# PayPal Preference
col1, col2 = st.columns(2)
with col1:
    st.subheader("Would Prefer PayPal?")
    paypal_counts = filtered_df['Prefer_PayPal'].value_counts()
    fig6 = px.pie(values=paypal_counts.values, names=paypal_counts.index,
                  color_discrete_sequence=['#00B8D4', '#6C5CE7'])
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    st.subheader("Would Recommend?")
    rec_counts = filtered_df['Would_Recommend'].value_counts()
    fig7 = px.pie(values=rec_counts.values, names=rec_counts.index,
                  color_discrete_sequence=['#00E676', '#FFD600', '#FF1744'])
    st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.markdown("**Data Source:** User Perception of Digital Payment Platforms Survey")
