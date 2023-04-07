from dash import Dash
from dash.dependencies import Input, Output
from dashboards import ExampleDashboard


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)


app.layout = ExampleDashboard().layout

@app.callback(Output(ExampleDashboard.div_id, 'children'),
              Input(ExampleDashboard.tabs_value, 'value'))

def render_content(tab):
    return ExampleDashboard().render_content(tab)

if __name__ == '__main__':
    app.run_server(debug=True)