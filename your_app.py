import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table

# Create a Dash app instance
app = dash.Dash(__name__)

# Initialize cycle data storage
data_columns = ["Date", "Day of Cycle", "Note", "Sex", "Bleeding", "Fluid", "Cramps", "Mood"]
cycle_data = pd.DataFrame(columns=data_columns)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Menstrual Cycle Tracker"),
    
    html.Div([
        html.Label("Date (DD-MM-YYYY)"),
        dcc.Input(id='date', type='text', placeholder='Enter date'),
        
        html.Label("Day of Cycle"),
        dcc.Input(id='day_of_cycle', type='number', placeholder='Enter day of cycle'),
        
        html.Label("Note"),
        dcc.Input(id='note', type='text', placeholder='Enter note'),
        
        html.Label("Sex"),
        dcc.Input(id='sex', type='text', placeholder='Enter sex method'),
        
        html.Label("Bleeding (0-4)"),
        dcc.Input(id='bleeding', type='number', placeholder='Enter bleeding level'),
        
        html.Label("Fluid"),
        dcc.Input(id='fluid', type='text', placeholder='Enter fluid type'),
        
        html.Label("Cramps (0-3)"),
        dcc.Input(id='cramps', type='number', placeholder='Enter cramps level'),
        
        html.Label("Mood"),
        dcc.Input(id='mood', type='text', placeholder='Enter mood'),
        
        html.Button('Add Entry', id='add_entry', n_clicks=0)
    ], style={'margin-bottom': '20px'}),
    
    html.H2("Cycle Data"),
    dash_table.DataTable(
        id='cycle_table',
        columns=[{"name": i, "id": i} for i in data_columns],
        data=cycle_data.to_dict('records'),
        style_table={'overflowX': 'auto'}
    )
])

# Callback to add data to the table
@app.callback(
    Output('cycle_table', 'data'),
    Input('add_entry', 'n_clicks'),
    [State('date', 'value'),
     State('day_of_cycle', 'value'),
     State('note', 'value'),
     State('sex', 'value'),
     State('bleeding', 'value'),
     State('fluid', 'value'),
     State('cramps', 'value'),
     State('mood', 'value')]
)
def update_table(n_clicks, date, day_of_cycle, note, sex, bleeding, fluid, cramps, mood):
    if n_clicks > 0 and all([date, day_of_cycle, note, sex, bleeding, fluid, cramps, mood]):
        new_entry = {
            "Date": date,
            "Day of Cycle": day_of_cycle,
            "Note": note,
            "Sex": sex,
            "Bleeding": bleeding,
            "Fluid": fluid,
            "Cramps": cramps,
            "Mood": mood
        }
        global cycle_data
        cycle_data = cycle_data.append(new_entry, ignore_index=True)
    return cycle_data.to_dict('records')

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')


