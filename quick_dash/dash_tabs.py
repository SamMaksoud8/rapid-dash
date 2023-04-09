from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_plots as dp
import os
from pathlib import Path
import plotly.express as px
from typing import Any, Type, Dict, List, Union,Optional
from abc import ABC
cache = {}

#Base classes for all tabs
class CallbackTab(ABC):
    """Represents a generic callback tab for the dashboard.

    Attributes:
        sync_type (str): SyncType for the tab.
        label (Optional[str]): Label for the tab. Must be unique.
        value (Optional[str]): Defines html value attribute for the tab. Must be unique.
        style (Dict[str, str]): Defines the style for the tab.
        cached_data (Optional[pd.DataFrame]): Defines the data for the tab.
        graph (Optional[dcc.Graph]): Defines the graph for the tab.
        children (List[Union[html.Div, dcc.Graph]]): Defines the children for the tab.
        csv_path (Optional[str]): Defines the csv path to load the data for the tab.
        tab (html.Div): Defines the tab.
        top_margin (int): Defines the top margin for the graph.
        graph_columns (List[Dict[str, Optional[str]]]): Defines the x,y values for the graph as list of dicts.
    """
    
    sync_type: str = 'static'
    label: Optional[str] = None 
    value: Optional[str] = None 
    style: Dict[str, str] = {'width': '100%'}
    cached_data: Optional[Union[pd.DataFrame,Any]] = None
    graph: Optional[dcc.Graph] = None
    children: List[Union[html.Div, dcc.Graph]] = []
    csv_path: Optional[str] = None
    tab: html.Div = None
    top_margin: int = 80
    graph_columns: List[Dict[str, Optional[str]]] = [{'x': None, 'y': None}]
    
    def __init__(self):
        pass
    
    def generate_tab(self) -> html.Div:
        """
        Generate the tab for the CallbackTab object.

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
        Getter method for the `data` property of the CallbackTab. If the `cached_data` attribute is None, 
        the `data_loader()` method is called to load the data, and the result is saved in `cached_data`. 
        The cached data is returned.

        Returns:
        -------
        Any:
            The cached data for the CallbackTab.
        """
        if self.cached_data is None:
            self.cached_data=self.data_loader()
        return self.cached_data

    
    def data_loader(self) -> pd.DataFrame:
        """
        Load data from CSV file and return as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: A pandas DataFrame with data from the specified CSV file.
        """
        return pd.read_csv(self.csv_path)

 
class DropDownTab(CallbackTab):
    """
    Class for defining a tab with a dropdown menu.

    Attributes:
    -----------
    graph_id: Optional[str]
        Defines the ID for the graph.
    dropdown_id: Optional[str]
        Defines the ID that stores the current selection of the dropdown.
    start_value: Optional[Union[str, int]]
        Defines the start value for the dropdown.
    options_column: Optional[str]
        Defines the column name for the options.
    """

    graph_id: Optional[str] = None
    dropdown_id: Optional[str] = None
    start_value: Optional[Union[str, int]] = None
    options_column: Optional[str] = None

    
    def __init__(self):
        CallbackTab.__init__(self)
    
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
    
    def init_global_vars(self)->None:
        """Initializes the global variables for caching data."""
        global cache
        cache[self.label]=self.data

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
        return px.line(dff, x=cls.x_value, y=cls.y_value)

class MultiTab(CallbackTab):
    """
    Class for creating multiple tabs with the same layout.

    Parameters
    ----------
    tab_list : list
        A list of tab labels that will be used to create the tabs.

    Attributes
    ----------
    style : dict
        A dictionary of CSS styles for the tab.
    """

    def __init__(self, tab_list: List[CallbackTab]):
        """
        Initializes a new instance of the `MultiTab` class.

        Parameters
        ----------
        tab_list : list
            A list of tab labels (subclasses of CallbackTab) that will be used to create the tabs.
        """
        super().__init__()
        self.style = {'width': '10%'}
        self.generate_tab(tab_list)


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
                    style={'display': 'flex', 'flex-direction': 'row','width': '100%'})
        

    def generate_tab(self, tab_list: List[CallbackTab]):
        """
        Generates the layout of the `MultiTab` instance as a `html.Div`.
        
        Parameters:
        -----------
        tab_list : List[CallbackTab]
            A list of `CallbackTab` instances to be displayed in a multi-tab format.
            
        Returns:
        --------
        tab : dash_html_components.Div
            The layout of the `MultiTab` instance.
        """
        data=[i().tab for i in tab_list]
        chunks = [data[i:i+2] for i in range(0, len(data), 2)]
        children=[self.flex_row(i) for i in chunks]
        self.tab = html.Div(className='row', children=children)



