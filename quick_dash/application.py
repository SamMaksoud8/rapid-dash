from dash import Dash, dcc
from dash.dependencies import Input, Output,State
from dashboards import ExampleDashboard


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, 
           external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True)

application = app.server

cls=ExampleDashboard
dashboard = cls()

app.layout = dashboard.get_layout

@app.callback(Output(cls.interval_id, 'disabled'),
            [Input(cls.tabs_value, 'value')])
def update_interval(tab):
    return not cls.check_if_tab_dynamic(cls, tab)

@app.callback([Output(cls.div_id, 'children'),
               Output(cls.store_id, 'data')] ,
            [Input(cls.tabs_value, 'value')],
            [State(cls.store_id, 'data')],
            [Input(cls.interval_id, 'n_intervals')])
def render_content(tab,store,interval):
    store = dashboard.update_store(tab,store,interval)
    return store[tab], store

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)