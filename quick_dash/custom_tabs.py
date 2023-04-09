from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_plots as dp
import os
from pathlib import Path
import plotly.express as px
from dash_tabs import CallbackTab,DropDownTab,MultiTab

DATA_DIR = Path(os.path.dirname(__file__)) / "data"


class ExampleBarTab(CallbackTab):
    label='Example Bar Plot' 
    value='tab-1-example-graph' 
    csv_path=DATA_DIR / "data.csv"
    graph_columns =[
            {'x':'consensus','y':'price'},
            {'x':'consensus','y':'volume'}
            ]
    
    plot_function=dp.BarPlot
    
    def __init__(self):
        super().__init__()
        self.init_graph()
        self.generate_tab()
        

    
    def init_graph(self):
        graph_data=[]
        if isinstance(self.graph_columns,dict):
            self.graph_columns=[self.graph_columns]
        for column in self.graph_columns:
            graph_data.append(self.plot_function(self.data,column['x'],column['y']))
        self.graph=dp.Graph(id=self.label,data=graph_data,top_margin=self.top_margin).plot
        

class ExampleScatterLineTab(CallbackTab):
    label='Example Line Plot'
    value='tab-1-example-line'
    csv_path=DATA_DIR / "data.csv"
    
    def __init__(self):
        super().__init__()
        self.graph_data=[dp.ScatterLinePlot(self.data,'date','volume')]
        self.graph=dp.Graph(id=self.label,data=self.graph_data,top_margin=80).plot
        self.generate_tab()


class ExampleScatterTab(CallbackTab):
    label='Example Scatter Plot'
    value='tab-2-example-graph'
    
    def __init__(self):
        super().__init__()
        self.init_graph()
        self.generate_tab()

    def data_loader(self):
        import plotly.express as px
        df = px.data.iris()
        data = [dp.ScatterPlot(df,x_name="sepal_width",y_name="sepal_length")]
        return data
    
    def init_graph(self):
        self.graph = dp.Graph(id=self.label,
                        data=self.data,
                        top_margin=80).plot
        


class ExampleDropDownTab(DropDownTab):
    label='Example Drop Down'
    value='tab-3-example-graph'
    graph_id='graph-content'
    dropdown_id='dropdown-selection'
    csv_path=DATA_DIR / "drop_data.csv"
    sync_type='dynamic'
    
    options_column='country'
    start_value='Canada'
    x_value='year'
    y_value='pop'
    
    def __init__(self):
        super().__init__()
        self.init_global_vars()
        self.generate_tab()


    
class ExampleTableTab(CallbackTab):
    label='Example Data Table'
    value='tab-1-example-dataframe'

    csv_path=DATA_DIR / "example_table.csv"
    table_columns=['State',
                        "Number of Solar Plants",
                        'Average MW Per Plant',
                        'Generation (GWh)']
    
    def __init__(self):
        super().__init__()
        self.graph=dp.DataTable(self.value,
                                self.data,
                                columns=self.table_columns
                                ).table
        self.generate_tab()
        
    
class ExampleMultiTab(MultiTab):
    label='Overview'
    value='tab-1-example-table-graph'

    tab_list = [ExampleTableTab,ExampleScatterTab,
                ExampleBarTab,ExampleScatterLineTab,
                ExampleDropDownTab]
    def __init__(self):
        super().__init__(self.tab_list)