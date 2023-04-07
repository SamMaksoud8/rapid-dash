from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_plots as dp
import dash_tabs as dt
import os
from pathlib import Path
import plotly.express as px

DATA_DIR = Path(os.path.dirname(__file__)) / "data"
EXAMPLE_DROPDOWN_DF=None 

class CallbackTab:
    label=None
    value=None
    tab_child=None
    def __init__(self):
        self.label=self.__class__.label
        self.value=self.__class__.value
        self.tab_child=self.__class__.tab_child
        self.data=None
        self.graph=None
        self.children=[]
    
    def generate_tab(self):
        self.tab = html.Div([
            html.H3(self.label),self.graph
        ])     
 

class DropDownTab(CallbackTab):
    options=None
    def __init__(self):
        CallbackTab.__init__(self)
        
    def generate_tab(self):
        self.tab = html.Div([
            html.H3(self.label),
            self.dropdown,
            dcc.Graph(id='graph-content'),
            html.Div(id=self.value)
        ])
        

class ExampleDropDownTab(DropDownTab):
    label='Example Drop Down'
    value='tab-3-example-graph'
    tab_child = dcc.Tab(label=label, value=value)
    start_value='Canada'
    
    def __init__(self):
        DropDownTab.__init__(self)
        global EXAMPLE_DROPDOWN_DF
        if EXAMPLE_DROPDOWN_DF is None:
            EXAMPLE_DROPDOWN_DF=pd.read_csv(DATA_DIR / "drop_data.csv")
        self.dropdown= dcc.Dropdown(EXAMPLE_DROPDOWN_DF.country.unique(), self.start_value, id='dropdown-selection')
        self.generate_tab()

    @callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        dff = EXAMPLE_DROPDOWN_DF[EXAMPLE_DROPDOWN_DF.country==value]
        return px.line(dff, x='year', y='pop')


class ExampleTabA(CallbackTab):
    label='Example A'
    value='tab-1-example-graph'
    tab_child = dcc.Tab(label=label, value=value)
    
    def __init__(self):
        CallbackTab.__init__(self)
        df = pd.read_csv(DATA_DIR / "data.csv")
        self.data=[dp.BarPlot(df,'consensus','price'),
                   dp.BarPlot(df,'consensus','volume')]
        self.graph=dp.Graph(id=self.label,data=self.data,top_margin=80).plot
        self.generate_tab()


class ExampleTabB(CallbackTab):
    label='Example B'
    value='tab-example-graph'
    tab_child = dcc.Tab(label=label, value=value)
    
    def __init__(self):
        dt.CallbackTab.__init__(self)
        self.data=[{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
        self.graph=dp.Graph(id=self.label,data=self.data,x_title="yo yo",y_title="no no",top_margin=80).plot
        self.generate_tab()

