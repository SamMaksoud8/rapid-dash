from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_plots as dp
import dash_tabs as dt
import os
from pathlib import Path

DATA_DIR = Path(os.path.dirname(__file__)) / "data"

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

