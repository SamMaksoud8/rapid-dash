from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_plots as dp
import os
from pathlib import Path
import plotly.express as px

cache = {}

#Base classes for all tabs
class CallbackTab:
    #SyncType for the tab.
    sync_type='static'
    #Label for the tab. Must be unique.
    label=None 
    #Defines html value attribute for the tab. Must be unique.
    value=None 
    #Defines the style for the tab.
    style={'width': '100%'}
    #Defines the data for the tab.
    cached_data=None
    #Defines the graph for the tab.
    graph=None
    #Defines the children for the tab.
    children=[]
    #Defines the csv path to load the data for the tab.
    csv_path=None
    #Defines the tab.
    tab=None
    #Defines the top margin for the graph.
    top_margin=80
    #Defines the x,y values for the graph as list of dicts.
    graph_columns=[{'x':None,'y':None}]
    
    def __init__(self):
        print("triggered",self.label)
        pass
    
    def generate_tab(self):
        self.tab = html.Div([
            html.H3(self.label),self.graph
        ], style=self.style)     

    @property
    def data(self):
        if self.cached_data is None:
            self.cached_data=self.data_loader()
        return self.cached_data

    
    def data_loader(self):
        print('data reloaded',self.label)
        return pd.read_csv(self.csv_path)
 
class DropDownTab(CallbackTab):
    #Defines the ID for the graph
    graph_id=None
    #Defines the ID that stores the current selection of the dropdown.
    dropdown_id=None
    #Defines the start value for the dropdown.
    start_value=None
    #Defines the column name for the options.
    options_column=None

    
    def __init__(self):
        CallbackTab.__init__(self)
    
    @property
    def options(self):
        return self.data[self.options_column].unique() 

    @property
    def dropdown(self):
        return dcc.Dropdown(self.options, 
                            self.start_value, 
                            id=self.dropdown_id)
    
    def init_global_vars(self):
        global cache
        cache[self.label]=self.data

    def generate_tab(self):
        self.tab = html.Div([
            html.H3(self.label),
            self.dropdown,
            dcc.Graph(id=self.graph_id),
            html.Div(id=self.value)
        ])
        
    @staticmethod
    def update_graph(cls,value):
        # Create a function that updates the graph based on the dropdown value
        options_column = cls.options_column
        df=cache[cls.label]
        dff = df[df[options_column]==value]
        return px.line(dff, x=cls.x_value, y=cls.y_value)

class MultiTab(CallbackTab):
    def __init__(self,tab_list):
        super().__init__()
        self.style={'width': '10%'}
        self.generate_tab(tab_list)

    def flex_row(self,data):
        if len(data)==1:
            return html.Div(data)
        else:
            return html.Div(data,
                    style={'display': 'flex', 'flex-direction': 'row','width': '100%'})
        

    def generate_tab(self,tab_list):
        data=[i().tab for i in tab_list]
        chunks = [data[i:i+2] for i in range(0, len(data), 2)]
        children=[self.flex_row(i) for i in chunks]
        self.tab = html.Div(className='row', children=children)



