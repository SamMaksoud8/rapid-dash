""" This module contains the base classes for creating dashboards."""
from dash import Dash, html, dcc, callback, Output, Input, State
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import custom_tabs as ct
import dash_tabs as dt
import datetime
from typing import Any, Type, Dict, List, Union


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Dashboard:
    """
    A base class for creating dashboards with multiple tabs.

    Attributes:
    -----------
    h1_title : str or None
        The title of the dashboard, displayed as an <h1> tag.
    tabs_value : str or None
        The ID of the dash `Tabs` component. This attribute is set in the subclass and is used to identify which tab is currently active.
    tabs : List[dt.CallbackTab]
        A list of the `dt.CallbackTab` subclasses that make up the content of the dashboard.
    starting_tab : str or None
        The value of the starting tab. If None, the first tab in the `tabs` attribute will be selected by default.
    div_id : str or None
        The ID of the <div> tag where the content of the selected tab is rendered.
    resync_interval_minutes : int
        The interval, in minutes, at which dynamic tabs should be reloaded.
    n_intervals : int
        The number of times the `Interval` component has triggered since the app started.
    interval_id : str
        The ID of the `Interval` component.
    store_id : str
        The ID of the `Store` component that stores the content of dynamic tabs.
    init_store_data : dict
        The initial data for the `Store` component.
    """
    
    h1_title: Union[str, None] = None
    tabs_value: Union[str, None] = None
    tabs: List[dt.CallbackTab] = []
    starting_tab: Union[str, None] = None
    div_id: Union[str, None] = None
    resync_interval_minutes: int = 15
    n_intervals: int = 0
    interval_id: str = 'interval-component'
    store_id: str = 'tab-data'
    init_store_data: dict = {'n_intervals': 0}
    
    
    def __init__(self) -> None:
        """
        Initialize the `Dashboard` class. Sets up the `Store` component, the update interval, and the layout of the dashboard.
        """
        self.init_store()
        self.set_update_interval()
        self.init_layout()

    def init_store(self) -> None:
        """
        Initialize the Dash store component with an ID and initial data.
        """
        self.store = dcc.Store(id=self.store_id, data=self.init_store_data)

    @staticmethod
    def get_dynamic_tab_content(cls: Type["Dashboard"], active_tab: str) -> html.Div:
        """
        Retrieve the dynamic content of a tab specified by active_tab.

        Args:
            cls (Type["Dashboard"]): The class of the dashboard.
            active_tab (str): The value of the active tab.

        Returns:
            html.Div: The dynamic content of the active tab.

        Raises:
            ValueError: If the active tab is not found.
        """
        for tab in cls.tabs:
            if tab.value == active_tab:
                assert tab.sync_type == 'dynamic'
                return tab().tab
        raise ValueError(f'Tab not found: {active_tab}')

    @staticmethod
    def minutes_to_milliseconds(minutes: int) -> int:
        """
        Convert minutes to milliseconds.

        Args:
            minutes (int): The number of minutes to convert.

        Returns:
            int: The equivalent number of milliseconds.
        """
        return minutes*60*1000

    def set_update_interval(self) -> None:
        """
        Sets the update interval for the dashboard based on the `resync_interval_minutes` attribute.
        The update interval is set in milliseconds and includes the number of intervals the component has been active.
        """
        minutes = self.resync_interval_minutes
        self.interval = dcc.Interval(id=self.interval_id,
                                     interval=self.minutes_to_milliseconds(
                                         minutes),
                                     n_intervals=self.n_intervals)

    def get_layout(self) -> html.Div:
        """
        Returns the layout of the dashboard, containing the header, tabs, interval component, store, and div.

        Returns:
            dash.html.Div: A Dash HTML div object representing the dashboard layout.
        """
        self.init_layout()
        return self.layout

    def init_layout(self) -> None:
        """
        Initialize the layout of the dashboard with tabs and intervals.
        """
        self.set_update_interval()
        children = self.get_tabs()
        self.layout = html.Div([
            html.H1(self.h1_title),
            dcc.Tabs(id=self.tabs_value, value=children[0].value,
                     children=children),
            self.interval,
            self.store,
            html.Div(id=self.div_id)
        ])

    @staticmethod
    def check_if_tab_dynamic(cls: Type['Dashboard'], active_tab: str) -> bool:
        """
        Check if the given tab is dynamic or not.

        Args:
            cls: The class object.
            active_tab: The tab to check.

        Returns:
            bool: True if the tab is dynamic, False otherwise.
        """
        for tab in cls.tabs:
            if tab.sync_type == 'dynamic':
                if active_tab == tab.value:
                    return True
        return False

    def get_tabs(self) -> List[dcc.Tab]:
        """
        Returns a list of dcc.Tab objects based on the `tabs` attribute of the Dashboard class.

        Returns:
            A list of dcc.Tab objects, each representing a tab in the dashboard.
        """
        children = []
        for tab in self.tabs:
            children.append(dcc.Tab(label=tab.label, value=tab.value))
        return children

    def get_tab_cls(self, tab: str) -> Type["dt.CallbackTab"]:
        """
        Get the class of the sync tab for the specified tab value.

        Args:
            tab (str): The value of the tab.

        Returns:
            Type["dt.CallbackTab"]: The class of the sync tab.
        """
        for cls in self.tabs:
            if tab == cls.value:
                return cls
        raise ValueError(f"Tab not found: {tab}")

    def update_store(self, tab: str, store: Dict[str, Union[int, str]], interval: int) -> Dict[str, Union[int, str]]:
        """
        Update the contents of a tab in the store with a new version if the specified interval has passed.

        Args:
            tab (str): The name of the tab to update in the store.
            store (dict): The current state of the store to update.
            interval (int): The current interval of the application.

        Returns:
            dict: The updated store after updating the specified tab.

        """
        if tab not in store.keys():
            tab_cls = self.get_tab_cls(tab)
            store[tab] = tab_cls().tab
        else:
            print('Saved time:', tab)

        if interval > store['n_intervals']:
            tab_cls = self.get_tab_cls(tab)
            store[tab] = tab_cls().tab
            store['n_intervals'] = interval

        return store

    def run(self, debug: bool = False, port: int = 8080) -> None:
        """
        Start the dashboard application.

        Parameters:
        -----------
        debug : bool, optional
            If True, enable debug mode, which will display error messages in the browser. Default is False.
        port : int, optional
            The port number to run the server on. Default is 8080.

        Returns:
        --------
        None
        """
        app = Dash(__name__,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
        
        app.layout = self.get_layout

        @app.callback(Output(self.interval_id, 'disabled'),
                    [Input(self.tabs_value, 'value')])
        def update_interval(tab: str) -> bool:
            """
            Update the `disabled` property of the `Interval` component.

            Parameters:
            -----------
            tab : str
                The ID of the currently active tab.

            Returns:
            --------
            bool
                True if the tab is dynamic, False otherwise.
            """
            return not self.check_if_tab_dynamic(self, tab)

        @app.callback([Output(self.div_id, 'children'),
                    Output(self.store_id, 'data')],
                    [Input(self.tabs_value, 'value')],
                    [State(self.store_id, 'data')],
                    [Input(self.interval_id, 'n_intervals')])
        def render_content(tab: str, store: dict, interval: int) -> tuple:
            """
            Update the data store and render the content of the selected tab.

            Parameters:
            -----------
            tab : str
                The ID of the currently active tab.
            store : dict
                The current data stored in the `Store` component.
            interval : int
                The number of times the `Interval` component has triggered since the app started.

            Returns:
            --------
            tuple
                A tuple containing the rendered content and the updated data for the `Store` component.
            """
            store = self.update_store(tab, store, interval)
            return store[tab], store

        app.run_server(debug=debug, port=port)

