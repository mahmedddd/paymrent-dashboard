import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page config
st.set_page_config(page_title="Digital Payment Analytics", layout="wide", page_icon="💳")

# Premium Dark Theme with Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1f3a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    h1 {
        color: #E8E9ED !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: #E8E9ED !important;
        font-weight: 600 !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #6C5CE7 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #A0A3BD !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] {
        background: rgba(30, 30, 47, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(108, 92, 231, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(108, 92, 231, 0.1);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background: rgba(30, 30, 47, 0.7);
        border: 1px solid rgba(108, 92, 231, 0.3);
        border-radius: 12px;
        color: #E8E9ED;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Chart containers */
    [data-testid="stPlotlyChart"] {
        background: rgba(30, 30, 47, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Subheader styling */
    .stMarkdown h3 {
        background: linear-gradient(90deg, rgba(108, 92, 231, 0.1) 0%, transparent 100%);
        padding: 0.8rem 1rem;
        border-left: 4px solid #6C5CE7;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

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
st.markdown("<h1>💳 Digital Payment Platforms Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #A0A3BD; margin-top: -1rem;'>User Perception Analysis</h3>", unsafe_allow_html=True)

# Survey Description
st.markdown("""
<div style='background: rgba(30, 30, 47, 0.7); backdrop-filter: blur(10px); 
            border: 1px solid rgba(108, 92, 231, 0.3); border-radius: 16px; 
            padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 8px 32px rgba(108, 92, 231, 0.1);'>
    <h4 style='color: #6C5CE7; margin-top: 0;'>📋 About This Survey</h4>
    <p style='color: #E8E9ED; line-height: 1.8; margin-bottom: 0.8rem;'>
        This comprehensive survey examines user perceptions of leading digital payment platforms in Pakistan, 
        including <b>Easypaisa</b>, <b>JazzCash</b>, and <b>NayaPay</b>. Conducted with <b>68 respondents</b>, 
        the study captures critical insights into user satisfaction, trust levels, security perceptions, 
        and platform preferences.
    </p>
    <h4 style='color: #00B8D4; margin-top: 1rem;'>🎯 Key Research Objectives</h4>
    <ul style='color: #E8E9ED; line-height: 1.8;'>
        <li><b>User Satisfaction:</b> Assess overall satisfaction levels with current digital payment solutions</li>
        <li><b>Security Trust:</b> Evaluate user confidence in data protection and transaction security</li>
        <li><b>Platform Comparison:</b> Compare ease of use, reliability, and innovation across platforms</li>
        <li><b>Market Insights:</b> Identify gaps and opportunities for platform improvements</li>
    </ul>
    <h4 style='color: #00E676; margin-top: 1rem;'>💡 Impact & Significance</h4>
    <p style='color: #E8E9ED; line-height: 1.8; margin-bottom: 0;'>
        These insights drive strategic decisions for digital payment providers, helping them enhance user experience, 
        build trust, and adapt to evolving consumer expectations in Pakistan's rapidly growing fintech ecosystem.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

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

st.markdown("<br>", unsafe_allow_html=True)

# Charts
col1, col2 = st.columns(2)

with col1:
    # Primary Wallet Distribution
    st.markdown("### 📊 Primary Wallet Distribution")
    wallet_counts = filtered_df['Primary_Wallet'].value_counts()
    fig1 = px.bar(x=wallet_counts.index, y=wallet_counts.values, 
                  color=wallet_counts.values,
                  color_continuous_scale=[[0, '#6C5CE7'], [0.5, '#A29BFE'], [1, '#00B8D4']])
    fig1.update_layout(
        showlegend=False, 
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8E9ED', size=14),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(108, 92, 231, 0.1)')
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(f"""
    <div style='background: rgba(108, 92, 231, 0.1); border-left: 3px solid #6C5CE7; 
                padding: 0.8rem; border-radius: 8px; margin-top: -1rem;'>
        <p style='color: #E8E9ED; font-size: 0.9rem; margin: 0;'>
            <b>Insight:</b> {wallet_counts.index[0]} dominates with {wallet_counts.values[0]} users 
            ({wallet_counts.values[0]/wallet_counts.sum()*100:.1f}%), indicating strong market leadership. 
            This suggests high brand trust and user retention in the primary platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Satisfaction Levels
    st.markdown("### 😊 Satisfaction Levels")
    sat_counts = filtered_df['Satisfaction'].value_counts()
    fig2 = px.pie(values=sat_counts.values, names=sat_counts.index, 
                  hole=0.4, 
                  color_discrete_sequence=['#6C5CE7', '#A29BFE', '#00B8D4', '#00E676', '#FD79A8'])
    fig2.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8E9ED', size=14)
    )
    st.plotly_chart(fig2, use_container_width=True)
    satisfied_pct = (len(filtered_df[filtered_df['Satisfaction'].isin(['Satisfied', 'Very satisfied'])])/len(filtered_df)*100)
    st.markdown(f"""
    <div style='background: rgba(108, 92, 231, 0.1); border-left: 3px solid #6C5CE7; 
                padding: 0.8rem; border-radius: 8px; margin-top: -1rem;'>
        <p style='color: #E8E9ED; font-size: 0.9rem; margin: 0;'>
            <b>Insight:</b> {satisfied_pct:.1f}% users report positive satisfaction (Satisfied/Very satisfied), 
            reflecting good platform performance. However, addressing the {100-satisfied_pct:.1f}% neutral/dissatisfied 
            segment presents growth opportunities.
        </p>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Usage Frequency
    st.markdown("### 📈 Usage Frequency")
    freq_counts = filtered_df['Usage_Frequency'].value_counts()
    fig3 = px.bar(x=freq_counts.index, y=freq_counts.values,
                  color=freq_counts.values, 
                  color_continuous_scale=[[0, '#00E676'], [0.5, '#00B8D4'], [1, '#6C5CE7']])
    fig3.update_layout(
        showlegend=False, 
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8E9ED', size=14),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(108, 92, 231, 0.1)')
    )
    st.plotly_chart(fig3, use_container_width=True)
    daily_pct = (len(filtered_df[filtered_df['Usage_Frequency'] == 'Daily'])/len(filtered_df)*100)
    st.markdown(f"""
    <div style='background: rgba(0, 184, 212, 0.1); border-left: 3px solid #00B8D4; 
                padding: 0.8rem; border-radius: 8px; margin-top: -1rem;'>
        <p style='color: #E8E9ED; font-size: 0.9rem; margin: 0;'>
            <b>Insight:</b> {daily_pct:.1f}% users engage daily, demonstrating strong platform stickiness 
            and integration into daily financial activities. Higher frequency correlates with increased 
            platform dependency and loyalty.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Most Trusted Security
    st.markdown("### 🔒 Most Trusted Security")
    trust_counts = filtered_df['Most_Trusted_Security'].value_counts().head(5)
    fig4 = px.bar(x=trust_counts.values, y=trust_counts.index, 
                  orientation='h', color=trust_counts.values,
                  color_continuous_scale=[[0, '#6C5CE7'], [1, '#00B8D4']])
    fig4.update_layout(
        showlegend=False, 
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8E9ED', size=14),
        xaxis=dict(showgrid=True, gridcolor='rgba(108, 92, 231, 0.1)'),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown(f"""
    <div style='background: rgba(0, 184, 212, 0.1); border-left: 3px solid #00B8D4; 
                padding: 0.8rem; border-radius: 8px; margin-top: -1rem;'>
        <p style='color: #E8E9ED; font-size: 0.9rem; margin: 0;'>
            <b>Insight:</b> {trust_counts.index[0]} leads in security trust with {trust_counts.values[0]} votes. 
            Security perception is critical for user retention—platforms must continuously strengthen 
            encryption, fraud detection, and transparency.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Ease of Use
st.markdown("### ⚡ Ease of Use by Platform")
ease_by_platform = filtered_df.groupby(['Primary_Wallet', 'Ease_of_Use']).size().reset_index(name='count')
fig5 = px.bar(ease_by_platform, x='Primary_Wallet', y='count', color='Ease_of_Use',
              barmode='group', 
              color_discrete_sequence=['#6C5CE7', '#A29BFE', '#00B8D4', '#00E676', '#FFD600'])
fig5.update_layout(
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E8E9ED', size=14),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(108, 92, 231, 0.1)'),
    legend=dict(bgcolor='rgba(30, 30, 47, 0.7)')
)
st.plotly_chart(fig5, use_container_width=True)
easy_users = len(filtered_df[filtered_df['Ease_of_Use'].isin(['Easy to use', 'Very easy to use'])])
st.markdown(f"""
<div style='background: rgba(0, 230, 118, 0.1); border-left: 3px solid #00E676; 
            padding: 0.8rem; border-radius: 8px; margin-top: -1rem;'>
    <p style='color: #E8E9ED; font-size: 0.9rem; margin: 0;'>
        <b>Insight:</b> {easy_users/len(filtered_df)*100:.1f}% users find their platform easy to use. 
        User-friendly interfaces directly impact adoption rates—platforms with intuitive design see 
        higher engagement and lower churn rates across demographics.
    </p>
</div>
""", unsafe_allow_html=True)

# PayPal Preference
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 💰 Would Prefer PayPal?")
    paypal_counts = filtered_df['Prefer_PayPal'].value_counts()
    fig6 = px.pie(values=paypal_counts.values, names=paypal_counts.index,
                  hole=0.4,
                  color_discrete_sequence=['#00B8D4', '#6C5CE7', '#FD79A8'])
    fig6.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8E9ED', size=14)
    )
    st.plotly_chart(fig6, use_container_width=True)
    if 'Yes' in paypal_counts.index:
        paypal_yes_pct = (paypal_counts['Yes']/paypal_counts.sum()*100)
    else:
        paypal_yes_pct = 0
    st.markdown(f"""
    <div style='background: rgba(253, 121, 168, 0.1); border-left: 3px solid #FD79A8; 
                padding: 0.8rem; border-radius: 8px; margin-top: -1rem;'>
        <p style='color: #E8E9ED; font-size: 0.9rem; margin: 0;'>
            <b>Insight:</b> {paypal_yes_pct:.1f}% express interest in PayPal, signaling demand for 
            international payment solutions. Local platforms should consider cross-border features 
            and global integration to capture this market segment.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 👍 Would Recommend?")
    rec_counts = filtered_df['Would_Recommend'].value_counts()
    fig7 = px.pie(values=rec_counts.values, names=rec_counts.index,
                  hole=0.4,
                  color_discrete_sequence=['#00E676', '#FFD600', '#FF1744', '#6C5CE7'])
    fig7.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8E9ED', size=14)
    )
    st.plotly_chart(fig7, use_container_width=True)
    recommend_positive = len(filtered_df[filtered_df['Would_Recommend'].isin(['Yes', 'Definitely'])])
    st.markdown(f"""
    <div style='background: rgba(253, 121, 168, 0.1); border-left: 3px solid #FD79A8; 
                padding: 0.8rem; border-radius: 8px; margin-top: -1rem;'>
        <p style='color: #E8E9ED; font-size: 0.9rem; margin: 0;'>
            <b>Insight:</b> {recommend_positive/len(filtered_df)*100:.1f}% would recommend their platform, 
            indicating strong Net Promoter Score (NPS). High recommendation rates drive organic growth 
            through word-of-mouth marketing and community trust.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Key Takeaways Section
st.markdown("""
<div style='background: linear-gradient(135deg, rgba(108, 92, 231, 0.2) 0%, rgba(0, 184, 212, 0.2) 100%); 
            border: 2px solid rgba(108, 92, 231, 0.4); border-radius: 16px; 
            padding: 2rem; margin: 2rem 0;'>
    <h3 style='color: #6C5CE7; margin-top: 0;'>🎯 Key Takeaways & Strategic Insights</h3>
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;'>
        <div>
            <h4 style='color: #00B8D4;'>✅ Strengths Identified</h4>
            <ul style='color: #E8E9ED; line-height: 2;'>
                <li><b>High Satisfaction:</b> Strong positive sentiment among majority users</li>
                <li><b>Daily Engagement:</b> Significant portion uses platforms daily</li>
                <li><b>Trust Foundation:</b> Users exhibit confidence in leading platforms</li>
                <li><b>Usability Success:</b> Most platforms rated easy to use</li>
            </ul>
        </div>
        <div>
            <h4 style='color: #FFD600;'>⚠️ Growth Opportunities</h4>
            <ul style='color: #E8E9ED; line-height: 2;'>
                <li><b>International Features:</b> Address PayPal preference with global payment options</li>
                <li><b>Security Transparency:</b> Enhance communication about data protection measures</li>
                <li><b>User Education:</b> Improve onboarding for occasional users</li>
                <li><b>Feature Parity:</b> Adopt best practices from international platforms</li>
            </ul>
        </div>
    </div>
    <h4 style='color: #00E676; margin-top: 1.5rem;'>🚀 Recommendations for Stakeholders</h4>
    <p style='color: #E8E9ED; line-height: 1.8; margin-bottom: 0;'>
        <b>For Platform Providers:</b> Prioritize security certifications, expand merchant networks, 
        and invest in AI-driven fraud detection. <b>For Policymakers:</b> Establish digital payment 
        standards and consumer protection frameworks. <b>For Users:</b> Leverage platform features 
        for bill payments, transfers, and cashless transactions to maximize convenience.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid rgba(108, 92, 231, 0.2); margin: 2rem 0;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A0A3BD; font-size: 0.9rem;'><b>Data Source:</b> User Perception of Digital Payment Platforms Survey | <b>Total Responses:</b> {} | <b>Powered by Plotly</b></p>".format(len(df)), unsafe_allow_html=True)
