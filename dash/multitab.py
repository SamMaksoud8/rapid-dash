from dash import Dash, dcc
from dash.dependencies import Input, Output,State
from dashboards import ExampleDashboard


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

dashboard = ExampleDashboard()

app.layout = dashboard.get_layout

@app.callback([Output('tabs-content-example-dash', 'children'),
               Output('tab-data', 'data')] ,
            [Input("tabs-example-dash", 'value')],
            [State('tab-data', 'data')],
            [Input("interval-component", 'n_intervals')])
def render_content(tab,store,interval):
    print('this interval',interval)
    store = dashboard.update_store(tab,store,interval)
    return store[tab], store

if __name__ == '__main__':
    app.run_server(debug=True)