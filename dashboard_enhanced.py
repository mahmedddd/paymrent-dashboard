import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np

# Load and prepare data
df = pd.read_csv('User Perception of Digital Payment Platforms .csv')

# Simplify column names
df.columns = ['Timestamp', 'Username', 'Platforms_Used', 'Primary_Wallet', 'Usage_Frequency', 
              'Most_Reliable', 'Best_Issue_Handler', 'Satisfaction', 'Data_Protection_Confidence',
              'Most_Trusted_Security', 'Most_Innovative', 'Ease_of_Use', 'Adapts_Quickly',
              'Would_Recommend', 'Prefer_PayPal', 'PayPal_Reason', 'Not_Switch_Reason',
              'PayPal_Features_to_Adopt', 'Should_Adopt_PayPal_Practices']

# Data preprocessing
def extract_platforms(text):
    if pd.isna(text) or text == '':
        return []
    platforms = text.split(';')
    cleaned = []
    for p in platforms:
        p = p.strip()
        if 'Easypaisa' in p:
            cleaned.append('Easypaisa')
        elif 'JazzCash' in p:
            cleaned.append('JazzCash')
        elif 'NayaPay' in p:
            cleaned.append('NayaPay')
        elif p and p != 'Other digital wallet':
            cleaned.append('Other')
    return list(set(cleaned))

# Create platform usage count
all_platforms = []
for platforms in df['Platforms_Used']:
    all_platforms.extend(extract_platforms(str(platforms)))
platform_counts = pd.Series(all_platforms).value_counts()

# Primary wallet distribution
primary_wallet = df['Primary_Wallet'].value_counts()

# Satisfaction levels
satisfaction_order = ['Very dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very satisfied']
satisfaction_counts = df['Satisfaction'].value_counts()

# Usage frequency
frequency_order = ['Rarely', 'Occasionally', 'Several times a week', 'Daily']
frequency_counts = df['Usage_Frequency'].value_counts()

# Trust and security
trust_counts = df['Most_Trusted_Security'].value_counts()

# Ease of use
ease_order = ['Very difficult to use', 'Difficult to use', 'Average', 'Easy to use', 'Very easy to use']
ease_counts = df['Ease_of_Use'].value_counts()

# PayPal preference
paypal_pref = df['Prefer_PayPal'].value_counts()

# Recommendation
recommend_counts = df['Would_Recommend'].value_counts()

# Data protection confidence
protection_order = ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']
protection_counts = df['Data_Protection_Confidence'].value_counts()

# Initialize Dash app
external_stylesheets = [
    dbc.themes.SLATE,
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Digital Payment Analytics Dashboard"
server = app.server  # Expose the server for deployment

# Premium Color Palette
colors = {
    'background': '#0A0E27',
    'text': '#E8E9ED',
    'primary': '#6C5CE7',
    'secondary': '#00B8D4',
    'success': '#00E676',
    'warning': '#FFD600',
    'danger': '#FF1744',
    'accent1': '#A29BFE',
    'accent2': '#FD79A8',
    'accent3': '#FDCB6E',
    'accent4': '#00CEC9',
}

# Styling
card_style = {
    'background': 'rgba(30, 30, 47, 0.7)',
    'backdropFilter': 'blur(10px)',
    'border': '1px solid rgba(108, 92, 231, 0.2)',
    'borderRadius': '16px',
    'padding': '24px',
    'boxShadow': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
}

kpi_card_style = {
    'background': 'rgba(30, 30, 47, 0.9)',
    'backdropFilter': 'blur(10px)',
    'border': '1px solid rgba(108, 92, 231, 0.3)',
    'borderRadius': '20px',
    'padding': '28px',
    'boxShadow': '0 12px 40px 0 rgba(108, 92, 231, 0.15)',
    'height': '100%',
}

filter_card_style = {
    'background': 'rgba(30, 30, 47, 0.85)',
    'backdropFilter': 'blur(15px)',
    'border': '1px solid rgba(0, 184, 212, 0.3)',
    'borderRadius': '16px',
    'padding': '20px',
    'boxShadow': '0 8px 32px 0 rgba(0, 184, 212, 0.1)',
}

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1([
                    html.I(className="fas fa-chart-line", style={'marginRight': '20px', 'color': colors['primary']}),
                    "Digital Payment Platforms"
                ], style={
                       'textAlign': 'center', 
                       'fontWeight': '800', 
                       'fontSize': '3.5rem',
                       'marginTop': '40px',
                       'marginBottom': '5px',
                       'letterSpacing': '-0.02em',
                       'background': 'linear-gradient(135deg, #6C5CE7 0%, #00B8D4 50%, #00E676 100%)',
                       'WebkitBackgroundClip': 'text',
                       'WebkitTextFillColor': 'transparent',
                       'backgroundClip': 'text'
                   }),
                html.H2("User Perception Analysis", style={
                    'textAlign': 'center',
                    'fontWeight': '600',
                    'fontSize': '1.8rem',
                    'color': colors['accent1'],
                    'marginBottom': '20px',
                    'letterSpacing': '0.02em'
                }),
                html.Div([
                    html.Span("Real-Time Insights", style={
                        'background': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                        'padding': '8px 24px',
                        'borderRadius': '30px',
                        'fontSize': '1rem',
                        'fontWeight': '600',
                        'color': '#0A0E27',
                        'marginRight': '12px',
                        'boxShadow': '0 4px 15px rgba(0, 184, 212, 0.4)'
                    }),
                    html.Span(" • ", style={'color': colors['accent1'], 'fontSize': '1.2rem', 'marginRight': '12px'}),
                    html.Span("Interactive Dashboard", style={
                        'color': colors['accent2'],
                        'fontSize': '1rem',
                        'fontWeight': '500'
                    }),
                    html.Span(" • ", style={'color': colors['accent1'], 'fontSize': '1.2rem', 'margin': '0 12px'}),
                    html.Span(f"Survey Responses: {len(df)}", style={
                        'color': colors['success'],
                        'fontSize': '1rem',
                        'fontWeight': '600'
                    })
                ], style={'textAlign': 'center', 'marginBottom': '40px'})
            ])
        ], width=12)
    ], className='fade-in'),
    
    # KPI Cards
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-users", style={
                                'fontSize': '2.5rem', 
                                'color': colors['primary'],
                                'marginBottom': '12px'
                            }),
                        ]),
                        html.H6("Total Responses", style={
                            'color': colors['accent1'], 
                            'fontWeight': '600',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '1px',
                            'marginBottom': '8px'
                        }),
                        html.H2(str(len(df)), className='metric-number', style={
                            'color': colors['text'], 
                            'fontSize': '3rem',
                            'marginBottom': '8px'
                        }),
                        html.P("Survey Participants", style={
                            'color': 'rgba(232, 233, 237, 0.6)', 
                            'fontSize': '0.85rem',
                            'margin': '0'
                        })
                    ])
                ], style=kpi_card_style, className='kpi-card')
            ])
        ], width=3, className='mb-4'),
        
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-mobile-alt", style={
                                'fontSize': '2.5rem', 
                                'color': colors['secondary'],
                                'marginBottom': '12px'
                            }),
                        ]),
                        html.H6("Platforms Tracked", style={
                            'color': colors['accent4'], 
                            'fontWeight': '600',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '1px',
                            'marginBottom': '8px'
                        }),
                        html.H2(str(len(platform_counts)), className='metric-number', style={
                            'color': colors['text'], 
                            'fontSize': '3rem',
                            'marginBottom': '8px'
                        }),
                        html.P("Main Payment Apps", style={
                            'color': 'rgba(232, 233, 237, 0.6)', 
                            'fontSize': '0.85rem',
                            'margin': '0'
                        })
                    ])
                ], style=kpi_card_style, className='kpi-card')
            ])
        ], width=3, className='mb-4'),
        
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-smile", style={
                                'fontSize': '2.5rem', 
                                'color': colors['success'],
                                'marginBottom': '12px'
                            }),
                        ]),
                        html.H6("Satisfaction Rate", style={
                            'color': colors['success'], 
                            'fontWeight': '600',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '1px',
                            'marginBottom': '8px'
                        }),
                        html.H2(f"{round((satisfaction_counts.get('Satisfied', 0) + satisfaction_counts.get('Very satisfied', 0)) / len(df) * 100)}%", 
                               className='metric-number',
                               style={
                                   'color': colors['text'], 
                                   'fontSize': '3rem',
                                   'marginBottom': '8px'
                               }),
                        html.P("Users Satisfied", style={
                            'color': 'rgba(232, 233, 237, 0.6)', 
                            'fontSize': '0.85rem',
                            'margin': '0'
                        })
                    ])
                ], style=kpi_card_style, className='kpi-card')
            ])
        ], width=3, className='mb-4'),
        
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-chart-line", style={
                                'fontSize': '2.5rem', 
                                'color': colors['warning'],
                                'marginBottom': '12px'
                            }),
                        ]),
                        html.H6("Daily Users", style={
                            'color': colors['warning'], 
                            'fontWeight': '600',
                            'fontSize': '0.9rem',
                            'textTransform': 'uppercase',
                            'letterSpacing': '1px',
                            'marginBottom': '8px'
                        }),
                        html.H2(f"{round(frequency_counts.get('Daily', 0) / len(df) * 100)}%", 
                               className='metric-number',
                               style={
                                   'color': colors['text'], 
                                   'fontSize': '3rem',
                                   'marginBottom': '8px'
                               }),
                        html.P("Active Daily", style={
                            'color': 'rgba(232, 233, 237, 0.6)', 
                            'fontSize': '0.85rem',
                            'margin': '0'
                        })
                    ])
                ], style=kpi_card_style, className='kpi-card')
            ])
        ], width=3, className='mb-4'),
    ]),
    
    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-filter", style={
                            'color': colors['primary'], 
                            'marginRight': '10px',
                            'fontSize': '1.2rem'
                        }),
                        html.Label("Filter by Platform", style={
                            'color': colors['text'], 
                            'fontWeight': '600',
                            'fontSize': '1rem',
                            'marginBottom': '12px',
                            'display': 'inline-block'
                        }),
                    ]),
                    dcc.Dropdown(
                        id='platform-filter',
                        options=[{'label': '🌐 All Platforms', 'value': 'ALL'}] + 
                                [{'label': f'📱 {p}', 'value': p} for p in ['Easypaisa', 'JazzCash', 'NayaPay']],
                        value='ALL',
                        style={
                            'backgroundColor': 'rgba(10, 14, 39, 0.8)',
                            'borderRadius': '10px',
                        },
                        clearable=False
                    )
                ])
            ], style=filter_card_style, className='chart-card')
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-clock", style={
                            'color': colors['secondary'], 
                            'marginRight': '10px',
                            'fontSize': '1.2rem'
                        }),
                        html.Label("Filter by Usage Frequency", style={
                            'color': colors['text'], 
                            'fontWeight': '600',
                            'fontSize': '1rem',
                            'marginBottom': '12px',
                            'display': 'inline-block'
                        }),
                    ]),
                    dcc.Dropdown(
                        id='frequency-filter',
                        options=[{'label': '⏰ All Frequencies', 'value': 'ALL'}] + 
                                [{'label': f'📊 {f}', 'value': f} for f in frequency_order],
                        value='ALL',
                        style={
                            'backgroundColor': 'rgba(10, 14, 39, 0.8)',
                            'borderRadius': '10px',
                        },
                        clearable=False
                    )
                ])
            ], style=filter_card_style, className='chart-card')
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-info-circle", style={
                            'color': colors['success'], 
                            'marginRight': '10px',
                            'fontSize': '1.2rem'
                        }),
                        html.Label("Active Filters", style={
                            'color': colors['text'], 
                            'fontWeight': '600',
                            'fontSize': '1rem',
                            'marginBottom': '12px',
                            'display': 'block'
                        }),
                    ]),
                    html.Div(id='filter-info', style={
                        'color': colors['accent1'],
                        'fontSize': '0.9rem',
                        'padding': '10px',
                        'background': 'rgba(108, 92, 231, 0.1)',
                        'borderRadius': '8px',
                        'marginTop': '8px'
                    })
                ])
            ], style=filter_card_style, className='chart-card')
        ], width=4),
    ], style={'marginBottom': '40px'}),
    
    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='platform-usage-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='satisfaction-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
    ]),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='frequency-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='trust-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
    ]),
    
    # Charts Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='ease-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='paypal-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
    ]),
    
    # Charts Row 4
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='heatmap-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=8, className='mb-4'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='gauge-chart', config={'displayModeBar': False, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=4, className='mb-4'),
    ]),
    
    # Charts Row 5
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='reasons-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='features-chart', config={'displayModeBar': True, 'displaylogo': False})
                ])
            ], style=card_style, className='chart-card')
        ], width=6, className='mb-4'),
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Hr(style={'borderColor': 'rgba(108, 92, 231, 0.3)', 'marginTop': '40px', 'marginBottom': '20px'}),
                html.P([
                    "💡 ",
                    html.Strong("Dashboard Insights:", style={'color': colors['primary']}),
                    " All visualizations are interactive. Hover over elements for detailed information. Use filters to explore specific segments."
                ], style={
                    'textAlign': 'center',
                    'color': colors['accent1'],
                    'fontSize': '0.95rem',
                    'marginBottom': '30px'
                })
            ])
        ], width=12)
    ]),
    
], fluid=True, style={
    'background': f'linear-gradient(135deg, {colors["background"]} 0%, #1a1f3a 100%)',
    'minHeight': '100vh',
    'padding': '20px'
})


# Callback
@callback(
    [Output('platform-usage-chart', 'figure'),
     Output('satisfaction-chart', 'figure'),
     Output('frequency-chart', 'figure'),
     Output('trust-chart', 'figure'),
     Output('ease-chart', 'figure'),
     Output('paypal-chart', 'figure'),
     Output('heatmap-chart', 'figure'),
     Output('gauge-chart', 'figure'),
     Output('reasons-chart', 'figure'),
     Output('features-chart', 'figure'),
     Output('filter-info', 'children')],
    [Input('platform-filter', 'value'),
     Input('frequency-filter', 'value')]
)
def update_all(platform, freq):
    filtered_df = df.copy()
    
    filter_text = []
    if platform != 'ALL':
        filtered_df = filtered_df[filtered_df['Primary_Wallet'].str.contains(platform, na=False)]
        filter_text.append(f"Platform: {platform}")
    else:
        filter_text.append("Platform: All")
    
    if freq != 'ALL':
        filtered_df = filtered_df[filtered_df['Usage_Frequency'] == freq]
        filter_text.append(f"Frequency: {freq}")
    else:
        filter_text.append("Frequency: All")
    
    # Handle empty filtered data
    if len(filtered_df) == 0:
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="No data matches the selected filters",
            showarrow=False,
            font=dict(size=18, color=colors['text'])
        )
        empty_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        filter_info = html.Div([
            html.P("⚠️ No data available for selected filters", 
                   style={'color': colors['warning'], 'fontWeight': '600'})
        ])
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, filter_info
    
    filter_info = html.Div([
        html.P([html.I(className="fas fa-check-circle", style={'marginRight': '8px', 'color': colors['success']}), 
                text], style={'margin': '4px 0'}) 
        for text in filter_text
    ] + [html.P(f"📊 Showing {len(filtered_df)} of {len(df)} responses", 
                style={'margin': '8px 0', 'fontWeight': '600', 'color': colors['warning']})])
    
    base_layout = {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': colors['text'], 'family': 'Inter, sans-serif', 'size': 14},
        'title_font_size': 20,
        'title_font_weight': 700,
        'title_font_color': colors['text'],
        'hoverlabel': {
            'bgcolor': 'rgba(108, 92, 231, 0.95)',
            'font_size': 15,
            'font_family': 'Inter, sans-serif',
            'font_color': '#FFFFFF',
            'bordercolor': colors['primary']
        },
        'margin': dict(t=80, b=80, l=80, r=80),
    }
    
    # Chart 1: Platform Usage
    all_plat = []
    for p in filtered_df['Platforms_Used']:
        all_plat.extend(extract_platforms(str(p)))
    
    if len(all_plat) > 0:
        plat_df = pd.Series(all_plat).value_counts().reset_index()
        plat_df.columns = ['Platform', 'Count']
        
        fig1 = px.bar(plat_df, x='Platform', y='Count',
                      title='<b>📱 Digital Payment Platform Usage</b>',
                      color='Count',
                      color_continuous_scale=['#6C5CE7', '#00B8D4', '#00E676'],
                      text='Count')
        fig1.update_layout(**base_layout)
        fig1.update_traces(textposition='outside', textfont=dict(size=16, weight='bold', color=colors['text']),
                          marker_line_color='rgba(108, 92, 231, 0.8)', marker_line_width=2,
                          hovertemplate='<b>%{x}</b><br>Users: %{y}<extra></extra>')
        fig1.update_xaxes(showgrid=False, title='<b>Platform</b>', title_font=dict(size=16), tickfont=dict(size=14))
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(108, 92, 231, 0.1)', title='<b>Users</b>', title_font=dict(size=16), tickfont=dict(size=14))
    else:
        fig1 = go.Figure()
        fig1.add_annotation(text="No platform data", showarrow=False, font=dict(size=16, color=colors['text']))
        fig1.update_layout(**base_layout, title='<b>📱 Digital Payment Platform Usage</b>')
    
    # Chart 2: Satisfaction
    sat_df = filtered_df['Satisfaction'].value_counts().reset_index()
    sat_df.columns = ['Level', 'Count']
    
    color_map = {
        'Very satisfied': colors['success'],
        'Satisfied': colors['accent4'],
        'Neutral': colors['warning'],
        'Dissatisfied': colors['accent2'],
        'Very dissatisfied': colors['danger']
    }
    
    fig2 = go.Figure(data=[go.Pie(
        labels=sat_df['Level'],
        values=sat_df['Count'],
        hole=0.5,
        marker=dict(
            colors=[color_map.get(l, colors['primary']) for l in sat_df['Level']],
            line=dict(color='#0A0E27', width=3)
        ),
        textfont=dict(size=15, weight='bold', color='#FFFFFF'),
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
    )])
    fig2.update_layout(**base_layout, title='<b>😊 User Satisfaction Distribution</b>',
                      legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=14)))
    fig2.add_annotation(text=f'<b>{len(filtered_df)}</b><br>Total',
                       x=0.5, y=0.5, font_size=20, font=dict(weight='bold'), showarrow=False, font_color=colors['primary'])
    
    # Chart 3: Frequency
    freq_df = filtered_df['Usage_Frequency'].value_counts().reset_index()
    freq_df.columns = ['Frequency', 'Count']
    
    freq_colors = {
        'Rarely': '#FF1744',
        'Occasionally': '#FF9800',
        'Several times a week': '#FFD600',
        'Daily': '#00E676'
    }
    
    fig3 = go.Figure(data=[go.Bar(
        x=freq_df['Frequency'], 
        y=freq_df['Count'],
        marker=dict(
            color=[freq_colors.get(f, colors['primary']) for f in freq_df['Frequency']],
            line=dict(color='rgba(10, 14, 39, 0.8)', width=2)
        ),
        text=freq_df['Count'],
        textposition='outside',
        textfont=dict(size=16, weight='bold', color=colors['text']),
        hovertemplate='<b>%{x}</b><br>Users: %{y}<extra></extra>'
    )])
    fig3.update_layout(**base_layout, title='<b>⏰ Transaction Frequency Patterns</b>')
    fig3.update_xaxes(showgrid=False, title='<b>Frequency</b>', title_font=dict(size=16), tickfont=dict(size=13))
    fig3.update_yaxes(showgrid=True, gridcolor='rgba(108, 92, 231, 0.1)', title='<b>Users</b>', title_font=dict(size=16), tickfont=dict(size=14))
    
    # Chart 4: Trust
    trust_df = filtered_df['Most_Trusted_Security'].value_counts().reset_index()
    trust_df.columns = ['Platform', 'Count']
    trust_df = trust_df[trust_df['Platform'] != 'None']
    
    if len(trust_df) > 0:
        platform_colors = {
            'Easypaisa': '#6C5CE7',
            'JazzCash': '#00B8D4',
            'NayaPay': '#00E676',
            'Other': '#FD79A8'
        }
        
        fig4 = go.Figure()
        for _, row in trust_df.iterrows():
            fig4.add_trace(go.Scatter(
                x=[row['Platform']],
                y=[row['Count']],
                mode='markers',
                name=row['Platform'],
                marker=dict(
                    size=row['Count'] * 15,
                    color=platform_colors.get(row['Platform'], colors['accent1']),
                    line=dict(width=2, color='#0A0E27'),
                    opacity=0.8
                ),
                hovertemplate=f'<b>{row["Platform"]}</b><br>Trust: {row["Count"]}<extra></extra>',
            ))
        
        fig4.update_layout(**base_layout, title='<b>🔒 Most Trusted Platforms</b>',
                          legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(size=14)))
        fig4.update_xaxes(showgrid=False, title_font=dict(size=16), tickfont=dict(size=14))
        fig4.update_yaxes(showgrid=True, gridcolor='rgba(108, 92, 231, 0.1)', title_font=dict(size=16), tickfont=dict(size=14))
    else:
        fig4 = go.Figure()
        fig4.add_annotation(text="No trust data", showarrow=False, font=dict(size=16, color=colors['text']))
        fig4.update_layout(**base_layout, title='<b>🔒 Most Trusted Platforms</b>')
    
    # Chart 5: Ease of Use
    ease_df = filtered_df['Ease_of_Use'].value_counts().reset_index()
    ease_df.columns = ['Level', 'Count']
    
    fig5 = go.Figure()
    fig5.add_trace(go.Scatterpolar(
        r=ease_df['Count'],
        theta=ease_df['Level'],
        fill='toself',
        fillcolor='rgba(0, 230, 118, 0.3)',
        line=dict(color=colors['success'], width=3),
        marker=dict(size=10, color=colors['warning'], line=dict(width=2, color='#0A0E27')),
        hovertemplate='<b>%{theta}</b><br>Count: %{r}<extra></extra>',
    ))
    
    fig5.update_layout(**base_layout, title='<b>✨ Ease of Use Experience</b>',
                      polar=dict(
                          radialaxis=dict(visible=True, color=colors['text'],
                                        gridcolor='rgba(108, 92, 231, 0.2)',
                                        tickfont=dict(size=13)),
                          bgcolor='rgba(0,0,0,0)',
                          angularaxis=dict(gridcolor='rgba(108, 92, 231, 0.2)',
                                         tickfont=dict(size=14))
                      ))
    
    # Chart 6: PayPal Preference
    pp_df = filtered_df['Prefer_PayPal'].value_counts().reset_index()
    pp_df.columns = ['Preference', 'Count']
    pp_df = pp_df[pp_df['Preference'] != '']
    
    fig6 = go.Figure(go.Funnel(
        y=pp_df['Preference'],
        x=pp_df['Count'],
        textposition="inside",
        textfont=dict(size=15, weight='bold', color='#FFFFFF'),
        marker=dict(color=['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']),
        textinfo="value+percent initial",
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
    ))
    fig6.update_layout(**base_layout, title='<b>💳 PayPal Preference Analysis</b>')
    fig6.update_yaxes(tickfont=dict(size=14))
    
    # Chart 7: Heatmap
    sat_map = {'Very dissatisfied': 1, 'Dissatisfied': 2, 'Neutral': 3, 'Satisfied': 4, 'Very satisfied': 5}
    prot_map = {'Strongly disagree': 1, 'Disagree': 2, 'Neutral': 3, 'Agree': 4, 'Strongly agree': 5}
    ease_map = {'Very difficult to use': 1, 'Difficult to use': 2, 'Average': 3, 'Easy to use': 4, 'Very easy to use': 5}
    
    hm_df = filtered_df.copy()
    hm_df['Sat_Score'] = hm_df['Satisfaction'].map(sat_map)
    hm_df['Prot_Score'] = hm_df['Data_Protection_Confidence'].map(prot_map)
    hm_df['Ease_Score'] = hm_df['Ease_of_Use'].map(ease_map)
    
    platforms = ['Easypaisa', 'JazzCash', 'NayaPay']
    metrics = ['Satisfaction', 'Security Trust', 'Ease of Use']
    
    hm_data = []
    for plat in platforms:
        plat_data = hm_df[hm_df['Primary_Wallet'].str.contains(plat, na=False)]
        if len(plat_data) > 0:
            hm_data.append([
                plat_data['Sat_Score'].mean(),
                plat_data['Prot_Score'].mean(),
                plat_data['Ease_Score'].mean()
            ])
        else:
            hm_data.append([0, 0, 0])
    
    fig7 = go.Figure(data=go.Heatmap(
        z=hm_data,
        x=metrics,
        y=platforms,
        colorscale='Turbo',
        text=[[f'{val:.2f}' for val in row] for row in hm_data],
        texttemplate='%{text}',
        textfont={"size": 16, "weight": "bold", "color": "#FFFFFF"},
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.2f}<extra></extra>',
        colorbar=dict(
            title=dict(text="Score", font=dict(size=14)),
            tickfont=dict(size=13)
        )
    ))
    fig7.update_layout(**base_layout, title='<b>📊 Platform Performance Heatmap</b>')
    fig7.update_xaxes(tickfont=dict(size=14))
    fig7.update_yaxes(tickfont=dict(size=14))
    
    # Chart 8: Recommendation Gauge
    rec = filtered_df['Would_Recommend'].value_counts()
    yes = rec.get('Yes', 0)
    total = rec.sum()
    rate = (yes / total * 100) if total > 0 else 0
    
    fig8 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>Would Recommend</b>", 'font': {'size': 20}},
        number={'font': {'size': 40, 'weight': 'bold'}},
        delta={'reference': 80, 'increasing': {'color': colors['success']}, 'font': {'size': 18}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': colors['text'], 'tickfont': {'size': 14}},
            'bar': {'color': colors['primary'], 'thickness': 0.8},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': colors['text'],
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255, 107, 53, 0.3)'},
                {'range': [50, 75], 'color': 'rgba(255, 193, 7, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(76, 175, 80, 0.3)'}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig8.update_layout(**base_layout, height=400)
    
    # Chart 9: PayPal Reasons
    reasons = []
    for r in filtered_df['PayPal_Reason'].dropna():
        if r and r != '':
            reasons.append(r)
    
    if reasons:
        reas_df = pd.Series(reasons).value_counts().reset_index()
        reas_df.columns = ['Reason', 'Count']
        
        fig9 = px.bar(reas_df, y='Reason', x='Count',
                      title='<b>💡 Why Users Choose PayPal</b>',
                      orientation='h',
                      color='Count',
                      color_continuous_scale='Blues',
                      text='Count')
        fig9.update_layout(**base_layout)
        fig9.update_traces(textposition='outside', textfont=dict(size=15, weight='bold', color=colors['text']),
                          hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>')
        fig9.update_xaxes(title_font=dict(size=16), tickfont=dict(size=14))
        fig9.update_yaxes(title_font=dict(size=16), tickfont=dict(size=13))
    else:
        fig9 = go.Figure()
        fig9.add_annotation(text="No data available", showarrow=False, font=dict(size=20, color=colors['text']))
        fig9.update_layout(**base_layout)
    
    # Chart 10: Features to Adopt
    features = []
    for f in filtered_df['PayPal_Features_to_Adopt'].dropna():
        if f and f != '':
            features.extend([x.strip() for x in str(f).split(';')])
    
    if features:
        feat_df = pd.Series(features).value_counts().reset_index()
        feat_df.columns = ['Feature', 'Count']
        feat_df = feat_df[feat_df['Count'] > 0]
        
        fig10 = px.treemap(feat_df, path=['Feature'], values='Count',
                           title='<b>🚀 Features to Adopt from PayPal</b>',
                           color='Count',
                           color_continuous_scale='Viridis')
        fig10.update_layout(**base_layout)
        fig10.update_traces(textinfo='label+value', 
                           textfont=dict(size=14, weight='bold', color='#FFFFFF'),
                           hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>')
    else:
        fig10 = go.Figure()
        fig10.add_annotation(text="No data available", showarrow=False, font=dict(size=20, color=colors['text']))
        fig10.update_layout(**base_layout)
    
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, filter_info


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
