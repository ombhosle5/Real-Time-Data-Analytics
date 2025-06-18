import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
from kafka import KafkaConsumer
import json
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "🌍 Wikimedia Real-Time Dashboard"

# Kafka Consumer Setup
consumer = KafkaConsumer(
    'wikimedia-events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    group_id='dashboard_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Layout
app.layout = html.Div([
    html.H1("\U0001F4CA Wikimedia Real-Time Edits Dashboard", style={
        'textAlign': 'center', 'fontSize': '26px', 'color': '#2c3e50', 'fontFamily': 'Arial, sans-serif'
    }),
    html.H3(id='message-counter', style={'textAlign': 'center', 'color': '#e74c3c', 'fontSize': '20px'}),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),
    html.Div([
        dcc.Graph(id='live-graph', style={'height': '450px'}),
        dcc.Graph(id='pie-chart', style={'height': '300px'}),
        dcc.Graph(id='event-type-graph', style={'height': '290px'})
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr', 'gap': '15px'}),
    html.Div(id='live-updates', style={
        'height': '220px',
        'overflowY': 'auto',
        'borderRadius': '8px',
        'padding': '12px',
        'backgroundColor': '#ecf0f1',
        'fontSize': '15px'
    })
], style={'backgroundColor': '#f9f9f9', 'padding': '25px', 'borderRadius': '12px'})

# Data Storage
edit_data = []
total_messages_processed = 0  # Counter for total messages

# Callback for real-time updates
@app.callback(
    [Output('live-graph', 'figure'),
     Output('pie-chart', 'figure'),
     Output('event-type-graph', 'figure'),
     Output('live-updates', 'children'),
     Output('message-counter', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    global edit_data, total_messages_processed
    messages = []
    event_types = {}
    minor_major_count = {'Minor': 0, 'Major': 0}
    
    try:
        records = consumer.poll(timeout_ms=1000)
        if records:
            for message in records.values():
                for record in message:
                    data = record.value
                    edit_data.append({
                        'title': data.get('title', 'N/A'),
                        'user': data.get('user', 'Anonymous'),
                        'timestamp': data.get('timestamp'),
                        'server_name': data.get('server_name'),
                        'minor': data.get('minor', False),
                        'type': data.get('type', 'unknown')
                    })
                    total_messages_processed += 1  # Increment message counter
                    if len(edit_data) > 50:
                        edit_data.pop(0)
                    minor_major_count['Minor' if data.get('minor', False) else 'Major'] += 1
                    event_type = data.get('type', 'unknown')
                    event_types[event_type] = event_types.get(event_type, 0) + 1
                    messages.append(html.Div(f"\U0001F4CC Title: {data.get('title', 'N/A')} | \U0001F464 User: {data.get('user', 'Anonymous')} | \U0001F50D Type: {data.get('type', 'unknown')}", style={
                        'borderBottom': '1px solid #ddd',
                        'marginBottom': '5px',
                        'paddingBottom': '5px',
                        'fontFamily': 'Arial, sans-serif'
                    }))
    except Exception as e:
        print(f"Error while consuming messages: {e}")
    
    df = pd.DataFrame(edit_data)
    fig = px.bar(df, x='user', title='\U0001F539 Edits Per User (Last 50 Changes)',
                 labels={'user': 'Editor'}, color='user',
                 color_discrete_sequence=px.colors.qualitative.Set2) if not df.empty else px.bar()
    pie_fig = px.pie(
        names=list(minor_major_count.keys()),
        values=list(minor_major_count.values()),
        title='\U0001F7E2 Minor vs \U0001F534 Major Edits',
        color_discrete_sequence=px.colors.qualitative.Pastel
    ) if sum(minor_major_count.values()) > 0 else px.pie()
    event_type_fig = px.bar(
        x=list(event_types.keys()),
        y=list(event_types.values()),
        title='\U0001F4CC Event Types Distribution',
        labels={'x': 'Event Type', 'y': 'Count'},
        color=list(event_types.keys()),
        color_discrete_sequence=px.colors.qualitative.Set3
    ) if event_types else px.bar()
    
    return fig, pie_fig, event_type_fig, messages, f"Total Messages Processed: {total_messages_processed}" 

if __name__ == '__main__':
    app.run_server(debug=True)