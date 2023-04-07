from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_tabs as dt



class Dashboard:
    h1_title=None
    tabs_value =None
    tabs=None
    starting_value=None
    div_id=None
    id=None
    
    def __init__(self):
        self.h1_title=self.__class__.h1_title
        self.tabs_value=self.__class__.tabs_value
        self.div_id=self.__class__.div_id
        self.tabs=self.__class__.tabs
        self.starting_value=self.__class__.starting_value
        self.id=self.__class__.id
        self.init_layout()
        
        
    def get_tabs(self):
        children = []
        for tab in self.tabs:
            children.append(tab.tab_child)
        return children
        
    def init_layout(self):
        self.layout=html.Div([
            html.H1(self.h1_title),
            dcc.Tabs(id=self.tabs_value, value=self.starting_value, children=self.get_tabs()),
            html.Div(id=self.div_id)
        ])
    
    def render_content(self,tab):
        for cls in self.tabs:
            if tab==cls.value:
                return cls().tab
                   


class ExampleDashboard(Dashboard):
    id="tabs-example-graph"
    h1_title='Dash Tabs component demo'
    tabs_value = "tabs-example-graph"
    div_id='tabs-content-example-graph'
    tabs=[dt.ExampleTabA,dt.ExampleTabB,dt.ExampleDropDownTab]
    starting_value = dt.ExampleDropDownTab.value
    
    def __init__(self):
        Dashboard.__init__(self)
        
