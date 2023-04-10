from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from typing import Any, Type, Dict, List, Union,Optional
from abc import ABC, abstractmethod, abstractproperty,abstractclassmethod


class FigureData(object):
    """
    Abstract base class used to define the data for a plotly graph figure.
    All concrete classes derived from this base class must implement the `plot` method.
    """
    x_name="x"
    y_name="y"

    @abstractproperty
    def plot(self) -> Any:
        """
        This method must be implemented by concrete classes derived from this base class.
        It should return the data to be plotted in a plotly graph figure.
        """
        pass


class SubPlot(FigureData):
    """
    A class to create subplots for Dash apps.
    See https://plotly.com/python/reference/ for more information on plotly properties.

    Methods:
    --------
    __init__(self, df: pd.DataFrame, x_name: str, y_name: str) -> None:
        Initializes a SubPlot object with a given pandas DataFrame, x and y axis column names.

    """
    
    def __init__(self, df: pd.DataFrame, x_name: str, y_name: str)-> None:
        """
        Initializes a SubPlot object with a given pandas DataFrame, x and y axis column names.

        Parameters:
        -----------
        df : pandas.DataFrame
            The dataframe containing the data for the subplot.
        x_name : str
            The name of the x-axis column in the dataframe.
        y_name : str
            The name of the y-axis column in the dataframe.
        """
        self.data=df
        self.x_name = x_name
        self.y_name = y_name
        self.plot_name = y_name

    @abstractclassmethod
    def plot_type(cls) -> str:
        """
        This method must be implemented by concrete classes derived from this base class.
        It should return the type of plot to be generated.
        """
        pass
    
    
    @abstractclassmethod
    def mode(cls) -> str:
        """
        This method must be implemented by concrete classes derived from this base class.
        It should return the mode of the plot to be generated.
        """
        pass
    
    @classmethod
    @property
    def marker(cls) -> dict:
        """
        The marker style to be used in the plot. 
        Default is {'color': 'blue', 'size': 5, 'opacity': 0.6, 'symbol': 'circle'}.
        """
        return {'color': 'blue', 'size': 5, 'opacity': 0.6, 'symbol': 'circle'}

    @classmethod
    @property
    def line(cls) -> dict:
        """
        The line style to be used in the plot. Default is {'color': 'blue'}.
        """
        return {'color': 'blue'}


    @property
    def x_values(self) -> pd.Series:
        """
        Getter method for the x values from the dataframe.

        Returns:
            pd.Series: The x values.
        """
        return self.data[self.x_name]
      
    @property
    def y_values(self) -> pd.Series:
        """
        Returns the y values from the DataFrame for the plot.

        Returns:
            pd.Series: A Pandas series of y values from the DataFrame.
        """
        return self.data[self.y_name]

    @property
    def plot(self):
        """
        Creates a generic plot with the given subplot properties.
        

        Returns:
        --------
        None
        """
        return {
                        'x': self.x_values,
                        'y': self.y_values,
                        'type': self.plot_type,
                        'mode': self.mode,
                        'marker': self.marker,
                        'line': self.line,
                    }


class BarPlot(SubPlot):
    """A subclass of SubPlot that generates a bar plot.

    Attributes:
    -----------
    plot_type : str
        Type of plot. This is set to "bar" for BarPlot.
    """
    plot_type: str = "bar"
    mode: str="group"
    
    def __init__(self, df: pd.DataFrame, x_name: str, y_name: str):
        """
        Initialize BarPlot object.

        Args:
            df (pd.DataFrame): Dataframe containing the x and y values.
            x_name (str): Name of the column containing the x values.
            y_name (str): Name of the column containing the y values.

        Returns:
            None
        """
        super().__init__(df, x_name, y_name)

  
class ScatterPlot(SubPlot):
    """
    A subclass of SubPlot that plots a scatter plot.

    Attributes:
    -----------
    plot_type : str
        The type of plot. In this case it is 'markers'.
    """
    plot_type: str = 'scatter'
    mode: str = "markers"
    
    
    def __init__(self, df: pd.DataFrame, x_name: str, y_name: str) -> None:
        """
        Constructs a ScatterPlot object.

        Args:
            df (pd.DataFrame): A pandas DataFrame that contains the data.
            x_name (str): A string that represents the name of the x-axis variable.
            y_name (str): A string that represents the name of the y-axis variable.

        Returns:
            None
        """
        SubPlot.__init__(self, df, x_name, y_name)

class LinePlot(SubPlot):
    """
    A subclass of `SubPlot` representing a line plot.

    Attributes:
    -----------
    mode: str
        The type of line to display in the plot.
    """
    plot_type: str = "line"
    mode: str = "lines"

    def __init__(self, df: pd.DataFrame, x_name: str, y_name: str) -> None:
        """
        Constructs a LinePlot object.

        Args:
            df (pd.DataFrame): A pandas DataFrame that contains the data.
            x_name (str): A string that represents the name of the x-axis variable.
            y_name (str): A string that represents the name of the y-axis variable.

        Returns:
            None
        """
        SubPlot.__init__(self, df, x_name, y_name)

class ScatterLinePlot(SubPlot):
    """
    A subclass of SubPlot used to create scatter and line plots.
    """
    plot_type: str = 'scatter'
    mode: str = 'lines+markers'
    def __init__(self, df: pd.DataFrame, x_name: str, y_name: str) -> None:
        """
        Constructs a ScatterLinePlot object.

        Args:
            df (pd.DataFrame): A pandas DataFrame that contains the data.
            x_name (str): A string that represents the name of the x-axis variable.
            y_name (str): A string that represents the name of the y-axis variable.

        Returns:
            None
        """
        SubPlot.__init__(self, df, x_name, y_name)


class DataTable(FigureData):
    def __init__(self, id: str, df: pd.DataFrame, columns: List[str] = []) -> None:
        """
        Initializes a DataTable instance with the given ID, DataFrame, and list of columns.
        This class can be used to display a table in a Dash app.

        Args:
            id (str): The ID of the table.
            df (pd.DataFrame): The DataFrame to be used to populate the table.
            columns (List[str], optional): A list of columns to be displayed in the table. Defaults to [] which will display all columns.

        Returns:
            None
        """
        self.id = id
        self.table = self.construct_table(df, columns)

        
    def filter_df(self, df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """
        Filters a Pandas DataFrame based on a list of column names. If the list is empty,
        returns the original DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to be filtered.
            cols (List[str]): A list of column names to be used as a filter.

        Returns:
            pd.DataFrame: A filtered DataFrame if cols is not empty, else the original DataFrame.
        """
        return df if len(cols) == 0 else df[cols]

    
    @property
    def plot(self):
        """
        This is hack to make the table accesible from a plot attribute like other plots. 
        This is because the table is not a plotly object but tables are handled similarly to plots.
        """
        return self.table


    def construct_table(self, df: pd.DataFrame, cols: List[str]) -> dash_table.DataTable:
        """
        Constructs a Dash DataTable from a Pandas DataFrame.

        Args:
            df (pd.DataFrame): The input data.
            cols (List[str]): The list of columns to include.

        Returns:
            dash_table.DataTable: The constructed DataTable object.
        """
        df = self.filter_df(df, cols)
        return dash_table.DataTable(
            id=self.id,
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records')
        )


class Graph:
    """
    A class representing a Plotly graph object.
    """
    def __init__(self, id: str, data:  Union[List[FigureData], FigureData], title: str = None, x_title: str = None, y_title: str = None, 
                 left_margin: int = 60, bottom_margin: int = 60, top_margin: int = 10, right_margin: int = 10, 
                 x_legend: int = 0, y_legend: int = 1, hovermode: str = "closest"):
        """
        Initializes a Graph object.

        Parameters:
        -----------
        id : str
            A unique identifier for the graph.
        data :  Union[List[FigureData], FigureData]
            A list of FigureData objects or a single FigureData object.
        title : str, optional
            The title of the graph.
        x_title : str, optional
            The label for the x-axis.
        y_title : str, optional
            The label for the y-axis.
        left_margin : int, optional
            The size of the left margin of the plot in pixels.
        bottom_margin : int, optional
            The size of the bottom margin of the plot in pixels.
        top_margin : int, optional
            The size of the top margin of the plot in pixels.
        right_margin : int, optional
            The size of the right margin of the plot in pixels.
        x_legend : int, optional
            The x-position of the legend. 0 means left, 1 means right.
        y_legend : int, optional
            The y-position of the legend. 0 means bottom, 1 means top.
        hovermode : str, optional
            The hovermode of the plot. Can be "closest" or "x" or "y".
        """
        self.title: str = id if title is None else title
        self.id: str = id
        self.x_legend: int = x_legend
        self.y_legend: int = y_legend
        self.left_margin: int = left_margin
        self.bottom_margin: int = bottom_margin
        self.top_margin: int = top_margin
        self.right_margin: int = right_margin
        self.hovermode: str = hovermode
        self.init_data(data)
        self.init_axis_titles(x_title, y_title)
        self.plot_graph()
        
    def init_axis_titles(self, x_title: str = None, y_title: str = None) -> None:
        """
        Initialize the titles for the x and y axis.

        Parameters:
        -----------
        x_title: str, optional
            The title to display for the x-axis. If not provided, the method will try to infer the name of the x-axis
            from the `x_name` attribute of the first element in `self.data`. If that is not available, a default value of "x"
            will be used.
        y_title: str, optional
            The title to display for the y-axis. If not provided, the method will try to infer the name of the y-axis
            from the `y_name` attribute of the first element in `self.data`. If that is not available, a default value of "y"
            will be used.
        """
        if x_title is None:
            self.x_title=self.data[0].x_name
        else:
            self.x_title=x_title
        
        if y_title is None:
            self.y_title=self.data[0].y_name
        else:
            self.y_title = y_title
        
    def init_data(self, data: Union[List[FigureData], FigureData]) -> None:
        """
        Initializes the data for the plot.

        Parameters:
        -----------
        data : Union[List[FigureData], FigureData]
            A list of FigureData objects or a single FigureData object.

        Returns:
        --------
        None

        """
        if isinstance(data, list):
            self.data = data
        else:
            self.data = [data]

    def render_data(self) -> List[Any]:
        """
        Returns the plot data for the plotly plot.

        Returns:
            List[FigureData.plot]: A list of plot data for the plotly plot.
        """
        return [i.plot for i in self.data]

    
    def layout(self) -> go.Layout:
        """
        Generate the layout for the plot.

        Returns
        -------
        go.Layout
            The layout object for the plot.
        """
        return go.Layout(
                    title=self.title,
                    xaxis={'title': self.x_title},
                    yaxis={'title': self.y_title},
                    margin={'l': self.left_margin, 'b': self.bottom_margin, 't': self.top_margin, 'r': self.right_margin},
                    legend={'x': self.x_legend, 'y': self.y_legend},
                    hovermode=self.hovermode
                )
        
        
    def plot_graph(self) -> dcc.Graph:
        """
        Plot the graph using Dash Core Components Graph object.

        Returns:
        dcc.Graph: Dash Core Components Graph object representing the plotted graph.
        """
        self.plot = dcc.Graph(
            id=self.id,
            figure={
                'data': self.render_data(),
                'layout': self.layout(), 
            }
        )
        return self.plot

