import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
import datetime

# Create a Dash app instance
app = dash.Dash(__name__)

# Initialize cycle data storage
data_columns = ["Date", "Day of Cycle", "Note", "Sex", "Bleeding", "Fluid", "Cramps", "Mood", "Acne", "Stress Level", "Presumed Ovulation", "Sleep Duration", "Weight", "Exercise", "Pregnancy Test"]
cycle_data = pd.DataFrame(columns=data_columns)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Cycle Tracker"),
    html.H3("Insert Data"),
    
    # Section 1: Date and Day of Cycle
    html.Div([
        html.Label("Date (DD-MM-YYYY)"),
        dcc.Input(id='date', type='text', value=datetime.datetime.now().strftime('%d-%m-%Y'), placeholder='Enter date', style={'margin-bottom': '10px', 'width': '100%'}),
        
        html.Label("Day of Cycle"),
        dcc.Input(id='day_of_cycle', type='number', placeholder='Enter day of cycle', value=1 if cycle_data.empty else (datetime.datetime.now() - pd.to_datetime(cycle_data.iloc[0]['Date'], format='%d-%m-%Y')).days + 1, style={'margin-bottom': '10px', 'width': '100%'})
    ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
    
    # Section 2: Note
    html.Div([
        html.Label("Note"),
        dcc.Input(id='note', type='text', placeholder='Enter note', style={'margin-bottom': '10px', 'width': '100%'})
    ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
    
    # Section 3: Sex, Bleeding, Fluid, Cramps, Acne, Stress Level, Mood, and Exercise
    html.Div([
        html.Label("Sex"),
        html.Div([
            dcc.Checklist(
                id='sex_toggle',
                options=[{'label': 'Enable Sex Selection', 'value': 'True'}],
                value=[],
                style={'display': 'inline-block', 'margin-right': '10px'}
            ),
            dcc.Dropdown(
                id='sex',
                options=[
                    {'label': 'Unprotected', 'value': 'Unprotected'},
                    {'label': 'Condom', 'value': 'Condom'},
                    {'label': 'Withdrawal', 'value': 'Withdrawal'},
                    {'label': 'Other', 'value': 'Other'}
                ],
                value='Other',
                style={'margin-bottom': '10px', 'width': '80%'},
                disabled=True
            )
        ], style={'margin-bottom': '10px', 'width': '100%'}),
        
        html.Label("Bleeding"),
        dcc.Slider(id='bleeding', min=0, max=4, step=1, value=0, marks={i: str(i) for i in range(5)}, tooltip={'always_visible': True}),
        
        html.Label("Fluid"),
        dcc.Dropdown(
            id='fluid',
            options=[
                {'label': 'Baseline', 'value': 'Baseline'},
                {'label': 'Fertile', 'value': 'Fertile'},
                {'label': 'Super Fertile', 'value': 'Super Fertile'},
                {'label': 'Dry', 'value': 'Dry'}
            ],
            placeholder='Select fluid type',
            style={'margin-bottom': '10px', 'width': '100%'}
        ),
        
        html.Label("Cramps"),
        dcc.Slider(id='cramps', min=0, max=3, step=1, value=0, marks={i: str(i) for i in range(4)}, tooltip={'always_visible': True}),
        
        html.Label("Acne"),
        dcc.Slider(id='acne', min=0, max=3, step=1, value=0, marks={i: str(i) for i in range(4)}, tooltip={'always_visible': True}),
        
        html.Label("Stress Level"),
        dcc.Slider(id='stress', min=0, max=3, step=1, value=0, marks={i: str(i) for i in range(4)}, tooltip={'always_visible': True}),
        
        html.Label("Mood"),
        dcc.Dropdown(
            id='mood',
            options=[
                {'label': 'Happy 😊', 'value': 'Happy'},
                {'label': 'Sad 😢', 'value': 'Sad'},
                {'label': 'Angry 😠', 'value': 'Angry'}
            ],
            placeholder='Select mood',
            style={'margin-bottom': '10px', 'width': '100%'}
        ),
        
        html.Label("Exercise"),
        dcc.Checklist(id='exercise', options=[{'label': 'Exercise', 'value': 'True'}], value=[], style={'margin-bottom': '10px'})
    ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
    
    # Section 4: Sleep Duration and Weight
    html.Div([
        html.Label("Sleep Duration"),
        dcc.Input(id='sleep_duration', type='text', placeholder='Enter sleep duration', style={'margin-bottom': '10px', 'width': '100%'}),
        
        html.Label("Weight"),
        dcc.Input(id='weight', type='text', placeholder='Enter weight', style={'margin-bottom': '10px', 'width': '100%'})
    ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
    
    # Section 5: Presumed Ovulation and Pregnancy Test
    html.Div([
        html.Label("Presumed Ovulation"),
        dcc.Checklist(id='presumed_ovulation', options=[{'label': 'Presumed Ovulation', 'value': 'True'}], value=[], style={'margin-bottom': '10px'}),
        
        html.Label("Pregnancy Test"),
        dcc.Dropdown(
            id='pregnancy_test',
            options=[
                {'label': 'Positive', 'value': 'Positive'},
                {'label': 'Negative', 'value': 'Negative'},
                {'label': 'Other', 'value': 'Other'}
            ],
            placeholder='Select result',
            style={'margin-bottom': '10px', 'width': '100%'}
        )
    ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
    
    # Section 6: Buttons
    html.Div([
        html.Button('Save Data', id='save_data', n_clicks=0),
        html.Button('Cycles', id='view_cycles', n_clicks=0)
    ], style={'margin-top': '20px', 'display': 'flex', 'gap': '10px', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
    
    html.H2("Cycle Data"),
    dash_table.DataTable(
        id='cycle_table',
        columns=[{"name": i, "id": i} for i in data_columns],
        data=cycle_data.to_dict('records'),
        style_table={'overflowX': 'auto', 'margin-top': '20px'}
    )
])

# Callback to enable/disable Sex dropdown
@app.callback(
    Output('sex', 'disabled'),
    Input('sex_toggle', 'value')
)
def toggle_sex_dropdown(toggle_value):
    return not bool(toggle_value)

# Callback to add data to the table
@app.callback(
    Output('cycle_table', 'data'),
    Input('save_data', 'n_clicks'),
    [State('date', 'value'),
     State('day_of_cycle', 'value'),
     State('note', 'value'),
     State('sex', 'value'),
     State('bleeding', 'value'),
     State('fluid', 'value'),
     State('cramps', 'value'),
     State('mood', 'value'),
     State('acne', 'value'),
     State('stress', 'value'),
     State('presumed_ovulation', 'value'),
     State('sleep_duration', 'value'),
     State('weight', 'value'),
     State('exercise', 'value'),
     State('pregnancy_test', 'value')]
)
def update_table(n_clicks, date, day_of_cycle, note, sex, bleeding, fluid, cramps, mood, acne, stress, presumed_ovulation, sleep_duration, weight, exercise, pregnancy_test):
    if n_clicks > 0:
        new_entry = {
            "Date": date,
            "Day of Cycle": day_of_cycle,
            "Note": note,
            "Sex": sex,
            "Bleeding": bleeding,
            "Fluid": fluid,
            "Cramps": cramps,
            "Mood": mood,
            "Acne": acne,
            "Stress Level": stress,
            "Presumed Ovulation": 'Yes' if 'True' in presumed_ovulation else 'No',
            "Sleep Duration": sleep_duration,
            "Weight": weight,
            "Exercise": 'Yes' if 'True' in exercise else 'No',
            "Pregnancy Test": pregnancy_test
        }
        global cycle_data
        cycle_data = cycle_data.append(new_entry, ignore_index=True)
    return cycle_data.to_dict('records')

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
