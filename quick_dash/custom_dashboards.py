""" This module contains custom dashboards."""
from dashboards import Dashboard
from dash import Dash, html, dcc, callback, Output, Input, State
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import custom_tabs as ct
import dash_tabs as dt
import datetime
from typing import Any, Type, Dict, List, Union


class ExampleDashboard(Dashboard):
    """
    A dashboard class that demonstrates the use of Dash Tabs component with various types of tabs,
    including multi-tab, dropdown-tab, table-tab, and scatter-tab.

    Attributes:
        h1_title (str): The title of the dashboard displayed in a H1 HTML element.
        tabs_value (str): The ID of the Tabs component.
        div_id (str): The ID of the HTML div element where the tab content is displayed.
        tabs (list): A list of tab classes to be included in the dashboard.
    """
    h1_title = 'Dashboard Demo'
    tabs_value = "tabs-example-dash"
    div_id = 'tabs-content-example-dash'
    tabs = [
            ct.ExampleTableTab,
            ct.ExampleBarTab,
            ct.ExampleScatterLineTab,
            ct.ExampleScatterTab]

    def __init__(self)-> None:
        super().__init__()


class ExampleDropDownDashboard(Dashboard):
    """
    A dashboard class that demonstrates the use of Dash Tabs component with the dropdown-tab.

    Attributes:
        h1_title (str): The title of the dashboard displayed in a H1 HTML element.
        tabs_value (str): The ID of the Tabs component.
        div_id (str): The ID of the HTML div element where the tab content is displayed.
        tabs (list): A list of tab classes to be included in the dashboard.
    """
    h1_title = 'Dropdown tab demo'
    tabs_value = "tabs-example-dash-dropodown"
    div_id = 'tabs-content-example-dash-dropdown'
    tabs = [ct.ExampleMultiTab,
            ct.ExampleDropDownTab,
            ct.ExampleTableTab,
            ct.ExampleScatterTab]

    def __init__(self)-> None:
        Dashboard.__init__(self)

    #Add a callback to update the dropdown options when the dropdown tab is selected.
    @callback(
        # Graph id as figure output
        Output(ct.ExampleDropDownTab.graph_id, 'figure'),
        Input(ct.ExampleDropDownTab.dropdown_id,
              'value')  # Dropdown id as input
    )
    def update_graph(value: str) -> go.Figure:
        """
        Update the graph displayed in ct.ExampleDropDownTab with the selected value from the dropdown.

        Args:
            value (str): The selected value from the dropdown.

        Returns:
            plotly.graph_objs._figure.Figure: A Plotly figure object representing the updated graph.
        """
        cls = ct.ExampleDropDownTab
        return cls.update_graph(cls, value)


