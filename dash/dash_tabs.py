from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_plots as dp
import os
from pathlib import Path
import plotly.express as px

DATA_DIR = Path(os.path.dirname(__file__)) / "data"

cache = {
    'Example Drop Down': None,
    'Example A':None,
    }

#Base classes for all tabs
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
 
    @property
    def cached_data(self):
        global cache
        return cache[self.label]
    
    def cache(self):
        global cache
        cache[self.label]=self.data_loader()
        
    def efficent_load_data(self):
        if self.cached_data is None:
            self.cache()
        return self.cached_data

    def load_data(self):
        self.cache()
        return self.cached_data
    
    @staticmethod
    def data_loader():
        raise NotImplementedError("This method must be implemented by the subclass")
 
class DropDownTab(CallbackTab):
    options=None
    graph_id=None
    dropdown_id=None
    start_value=None
    options_column=None
    
    def __init__(self):
        CallbackTab.__init__(self)
        self.graph_id=self.__class__.graph_id
        self.dropdown_id=self.__class__.dropdown_id
        self.start_value=self.__class__.start_value
        self.options_column=self.__class__.options_column
       
    @property
    def options(self):
        return cache[self.label][self.options_column].unique() 

    @property
    def dropdown(self):
        return dcc.Dropdown(self.options, 
                            self.start_value, 
                            id=self.dropdown_id)
    
    def generate_tab(self):
        self.tab = html.Div([
            html.H3(self.label),
            self.dropdown,
            dcc.Graph(id=self.graph_id),
            html.Div(id=self.value)
        ])

class DynamicCallbackTab(CallbackTab):
    def __init__(self):
        super().__init__()
        
        
    def generate_tab(self):
        self.tab = html.Div([
            html.H3(self.label),self.graph
        ])
        

class ExampleTabA(CallbackTab):
    label='Example A'
    value='tab-1-example-graph'
    tab_child = dcc.Tab(label=label, value=value)
    
    def __init__(self):
        super().__init__()
        self.load_data()
        self.data=[dp.BarPlot(self.cached_data,'consensus','price'),
                   dp.BarPlot(self.cached_data,'consensus','volume')]
        self.graph=dp.Graph(id=self.label,data=self.data,top_margin=80).plot
        self.generate_tab()
        
    def data_loader(self):
        return pd.read_csv(DATA_DIR / "data.csv")

class ExampleTabB(CallbackTab):
    label='Example B'
    value='tab-2-example-graph'
    tab_child = dcc.Tab(label=label, value=value)
    
    def __init__(self):
        super().__init__()
        self.load_data()
        self.load_graph()
        self.generate_tab()

    def data_loader(self):
        import plotly.express as px
        print("reloading from data loader",self.__class__.__name__)
        df = px.data.iris()
        data = [dp.ScatterPlot(df,x_name="sepal_width",y_name="sepal_length")]
        return data
    
    def load_graph(self):
        self.graph = dp.Graph(id=self.label,
                        data=self.cached_data,
                        top_margin=80).plot

class ExampleDropDownTab(DropDownTab):
    label='Example Drop Down'
    value='tab-3-example-graph'
    graph_id='graph-content'
    dropdown_id='dropdown-selection'
    tab_child = dcc.Tab(label=label, value=value)
    
    options_column='country'
    start_value='Canada'
    x_value='year'
    y_value='pop'
    
    def __init__(self):
        super().__init__()
        self.load_data()
        self.generate_tab()
            
    def data_loader(self):
        print("reloading from data loader",self.__class__.__name__)
        return pd.read_csv(DATA_DIR / "drop_data.csv")
    
    @staticmethod
    def update_graph(cls,value):
        # Create a function that updates the graph based on the dropdown value
        options_column = cls.options_column
        df=cache[cls.label]
        dff = df[df[options_column]==value]
        return px.line(dff, x=cls.x_value, y=cls.y_value)