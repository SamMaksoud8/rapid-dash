from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_plots as dp
import os
from pathlib import Path
import plotly.express as px
from dash_tabs import DashboardTab,DropDownTab,MultiTab,TableTab
import pathlib
from typing import Type,Union,Dict,List,Any,Callable,Optional

DATA_DIR = Path(os.path.dirname(__file__)) / "data"


class ExampleBarTab(DashboardTab):
    label: str = 'Example Bar Plot'
    value: str = 'tab-1-example-graph'
    csv_path: Union[str, Path] = DATA_DIR / "data.csv"
    plot_function: Callable = dp.BarPlot
    graph_columns: List[Dict[str, str]] = [
            {'x':'consensus', 'y':'price'},
            {'x':'consensus', 'y':'volume'}
            ]
    
    
    def __init__(self) -> None:
        super().__init__()
        

        

class ExampleScatterLineTab(DashboardTab):
    label='Example Line Plot'
    value='tab-1-example-line'
    csv_path=DATA_DIR / "data.csv"
    plot_function: Callable = dp.ScatterLinePlot
    graph_columns={'x':'date', 'y':'volume'}
    
    def __init__(self):
        super().__init__()
        

class ExampleScatterTab(DashboardTab):
    label='Example Scatter Plot'
    value='tab-2-example-graph'
    plot_function=dp.ScatterPlot
    graph_columns={'x':'sepal_width','y':'sepal_length'}
    
    
    def __init__(self):
        super().__init__()
        

    def data_loader(self):
        import plotly.express as px
        return px.data.iris()


class ExampleDropDownTab(DropDownTab):
    label='Example Drop Down'
    value='tab-3-example-graph'
    graph_id='graph-content'
    dropdown_id='dropdown-selection'
    csv_path=DATA_DIR / "drop_data.csv"
    sync_type='dynamic'
    
    options_column='country'
    start_value='Canada'
    graph_columns={'x':'year','y':'pop'}
    
    def __init__(self):
        super().__init__()

    
class ExampleTableTab(TableTab):
    label='Example Data Table'
    value='tab-1-example-dataframe'
    csv_path=DATA_DIR / "example_table.csv"
    table_columns=['State',
                        "Number of Solar Plants",
                        'Average MW Per Plant',
                        'Generation (GWh)']
    
    def __init__(self):
        super().__init__()
        
    
class ExampleMultiTab(MultiTab):
    label='Overview'
    value='tab-1-example-table-graph'

    tab_list = [ExampleTableTab,ExampleScatterTab,
                ExampleBarTab,ExampleScatterLineTab,
                ExampleDropDownTab]
    def __init__(self):
        super().__init__(self.tab_list)