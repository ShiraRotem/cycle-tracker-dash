import dash
import dash_html_components as html

# Create a Dash app instance
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Shira's app")
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

