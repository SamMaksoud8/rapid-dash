"""_
This module contains the classes for creating the tabs for the dashboard.
"""

from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_plots as dp
import os
from pathlib import Path
import plotly.express as px
from typing import Any, Type, Dict, List, Union,Optional
from abc import ABC,abstractclassmethod,abstractmethod

cache = {}

class BaseTab(object):
    
    @property
    def sync_type(self) -> str:
        return 'static'
    
    @property
    @abstractclassmethod
    def tab(cls) -> html.Div:
        """Defines the tab. This method is intended to be implemented by subclasses."""
        pass
    
    @abstractclassmethod
    def init_tab(self):
        "Initializes the tab. This method is intended to be implemented by subclasses."
        pass
    
    @property
    @abstractclassmethod
    def label(cls) -> str:
        """Label for the tab. Must be unique. This method is intended to be implemented by subclasses."""
        pass
    
    @property
    @abstractclassmethod
    def value(cls) -> str:
        """ Defines html value attribute for the tab. Must be unique. This method is intended to be implemented by subclasses."""
        pass
    
    @abstractmethod
    def generate_tab(self) -> html.Div:
        """Generates the div for the tab. This method is intended to be implemented by subclasses."""
        pass


class SingleTAB(BaseTab):
    """Represents a generic single tab for the dashboard.

    Attributes:
        style (Dict[str, str]): Defines the style for the tab.
        cached_data (Union[pd.DataFrame,Any]): Defines the data for the tab.
        graph (dcc.Graph): Defines the graph for the tab.
        children (List[Union[html.Div, dcc.Graph]]): Defines the children for the tab.
        tab (html.Div): Defines the tab.
        top_margin (int): Defines the top margin for the graph.
        graph_columns (Union[List[Dict[str, str]],Dict[str,str]]): Defines the x,y values for the graph as dict or list of dicts.
    """
    
    sync_type: str = 'static'
    style: Dict[str, str] = {'width': '100%'}
    children: List[Union[html.Div, dcc.Graph]] = []
    top_margin: int = 80
    tab: Optional[html.Div] = None
    cached_data : Union[pd.DataFrame,Any] = None
    
    def __init__(self):
        pass
        #self.init_tab()
    
    @property
    @abstractclassmethod
    def label(cls) -> str:
        """Label for the tab. Must be unique. This method is intended to be implemented by subclasses."""
        pass
    
    @property
    @abstractclassmethod
    def value(cls) -> str:
        """ Defines html value attribute for the tab. Must be unique. This method is intended to be implemented by subclasses."""
        pass
    
    @property
    @abstractclassmethod
    def graph(cls) -> dcc.Graph:
        """Defines the graph for the tab. This method is intended to be implemented by subclasses."""
        pass
    
    @property
    @abstractclassmethod
    def graph_columns(cls) -> Union[List[Dict[str, str]],Dict[str,str]]:
        """Defines the x,y column names for the graph as dicts or list of dicts.
        For example a pd.DataFrame, df, with columns ['disease','lifespan'] should have a property
        graph columns = [{'x':'disease','y':'lifespan'}] to plot the disease on the x-axis and the lifespan on the y-axis.
        """
        pass
    
    @abstractmethod
    def data_loader(self)->Any:
        """Loads the data for the tab. This method is intended to be implemented by subclasses.
        """
        pass
       
    @abstractmethod 
    def init_tab(self):
        """
        Initializes the tab by setting up the plot and generating the tab.
        This method is intended to be implemented by subclasses.
        """
        pass
    
    def generate_tab(self) -> html.Div:
        """
        Generate the tab for the DashboardTab object.

        Returns:
            html.Div: The generated tab with the label and graph.
        """
        self.tab = html.Div([
            html.H3(self.label), self.graph
        ], style=self.style)
        return self.tab
   
    @property
    def data(self) -> Any:
        """
        Getter method for the `data` property of the DashboardTab. If the `cached_data` attribute is None, 
        the `data_loader()` method is called to load the data, and the result is saved in `cached_data`. 
        The cached data is returned.

        Returns:
        -------
        Any:
            The cached data for the DashboardTab.
        """
        if self.cached_data is None:
            self.cached_data=self.data_loader()
        return self.cached_data
 
 
class DashboardTab(SingleTAB):
    graph=None
    def __init__(self):
        super().__init__()
    
    @property
    def plot_function(cls) -> dp.SubPlot:
        """Defines the SubPlot function for the Tab. This method is intended to be implemented by subclasses."""
        raise ValueError("plot_function must be defined in subclass to use default init_graph method.")
        
    @property
    def csv_path(cls) -> str:
        """Defines the csv path to load the data for the tab. This method is intended to be implemented by subclasses."""
        raise ValueError("csv_path must be defined in subclass to use default DashboardTab data_loader method.")
    
    def csv_loader(self) -> pd.DataFrame:
        """
        Load data from CSV file and return as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: A pandas DataFrame with data from the specified CSV file.
        """
        return pd.read_csv(self.csv_path)

    def data_loader(self) -> pd.DataFrame:
        """
        Load data from CSV file and return as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: A pandas DataFrame with data from the specified CSV file.
        """
        return self.csv_loader()

    def init_graph(self)->None:
        """
        Initializes the graph with the data from the csv file.

        Returns:
            None
        """
        graph_data=[]
        if isinstance(self.graph_columns,dict):
            self.graph_columns=[self.graph_columns]
        for column in self.graph_columns:
            graph_data.append(self.plot_function(self.data,column['x'],column['y']))
        self.graph=dp.Graph(id=self.label,data=graph_data,top_margin=self.top_margin).plot
  
    def init_tab(self):
        self.init_graph()
        self.generate_tab()
  

class TableTab(DashboardTab):
    
    @property
    def graph_columns(self)->None:
        print("graph_columns not required for TableTab")
        return None

    @property
    @abstractclassmethod
    def table_columns(cls) -> List[str]:
        """Defines the list of columns to include in the data table. This method is intended to be implemented by subclasses."""
        pass

    def init_graph(self) -> None:
        self.graph= dp.DataTable(self.value,
                            self.data,
                            columns=self.table_columns
                            ).table
  

class DropDownTab(DashboardTab):
    graph_id: Optional[str] = None
    dropdown_id: Optional[str] = None
    start_value: Optional[Union[str, int]] = None
    options_column: Optional[str] = None
    
    def __init__(self):
        super().__init__()

    @property
    def graph_columns(self)->None:
        print("graph_columns not required for DropDownTab")
        return None

    @property
    def options(self) -> pd.Series:
        """Return the unique options for the dropdown."""
        return self.data[self.options_column].unique()


    @property
    def dropdown(self) -> dcc.Dropdown:
        """Return a dropdown component with the options and start value defined in the class."""
        return dcc.Dropdown(self.options, 
                            self.start_value, 
                            id=self.dropdown_id)
    

    def init_tab(self) -> None:
        """
        Initializes the tab by setting up the global variables and generating the tab.

        Returns:
            None
        """
        self.data_loader()
        self.init_global_vars()
        self.generate_tab()

    def init_global_vars(self)->None:
        global cache
        cache[self.label] = self.data
        

    def generate_tab(self) -> html.Div:
        """
        Generates the layout of the `DropDownTab` instance as a `html.Div`.
        
        Returns:
        --------
        tab : dash_html_components.Div
            The layout of the `DropDownTab` instance.
        """
        self.tab = html.Div([
            html.H3(self.label),
            self.dropdown,
            dcc.Graph(id=self.graph_id),
            html.Div(id=self.value)
        ])
        return self.tab
        
    @staticmethod
    def update_graph(cls: Type["DropDownTab"], value: Union[str, int]) -> px.line:
        """
        Update the graph based on the selected dropdown value.

        Parameters:
        -----------
        cls: Type[DropDownTab]
            The DropDownTab instance.
        value: str or int
            The selected value from the dropdown.

        Returns:
        --------
        fig: px.line
            The updated graph with the data filtered by the selected value.
        """
        # Create a function that updates the graph based on the dropdown value
        options_column = cls.options_column
        df=cache[cls.label]
        dff = df[df[options_column]==value]
        return px.line(dff, x=cls.graph_columns['x'], y=cls.graph_columns['y'])


class MultiTab(BaseTab):
    flex_style: Dict[str, str] = {'display': 'flex', 'flex-direction': 'row','width': '100%'}
    tab: Optional[html.Div] = None

    def __init__(self, tab_list: List[DashboardTab]):
        """
        Initializes a new instance of the `MultiTab` class.

        Parameters
        ----------
        tab_list : list
            A list of tab labels (subclasses of DashboardTab) that will be used to create the tabs.
        """
        #super().__init__()
        self.generate_tab(tab_list)


    @property
    @abstractclassmethod
    def tab_list(cls) -> List[DashboardTab]:
        """Defines the list of tabs to create. This method is intended to be implemented by subclasses."""
        pass

    def flex_row(self, data: List[Union[dcc.Graph, html.Div]]) -> html.Div:
        """
        Given a list of dcc.Graph or html.Div instances, this function creates a flex row
        layout if the length of the list is greater than 1. Otherwise, it returns the
        only element in the list.

        Parameters
        ----------
        data : List[Union[dcc.Graph, html.Div]]
            List of dcc.Graph or html.Div instances.

        Returns
        -------
        html.Div
            A flex row layout of the given elements, or the only element in the list.
        """
        if len(data)==1:
            return html.Div(data)
        else:
            return html.Div(data,
                    style=self.flex_style)
        

    def generate_tab(self, tab_list: List[DashboardTab])-> html.Div:
        """
        Generates the layout of the `MultiTab` instance as a `html.Div`.
        
        Parameters:
        -----------
        tab_list : List[DashboardTab]
            A list of `DashboardTab` instances to be displayed in a multi-tab format.
            
        Returns:
        --------
        tab : dash_html_components.Div
            The layout of the `MultiTab` instance.
        """
        data=[i().tab for i in tab_list]
        chunks = [data[i:i+2] for i in range(0, len(data), 2)]
        children=[self.flex_row(i) for i in chunks]
        self.tab = html.Div(className='row', children=children)
        return self.tab
    


