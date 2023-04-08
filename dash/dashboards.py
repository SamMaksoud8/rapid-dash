from dash import Dash, html, dcc, callback, Output, Input, State
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_tabs as dt
import datetime

class Dashboard:
    h1_title = None
    tabs_value = None
    tabs = [{}]
    starting_tab = None
    div_id = None
    resync_interval_minutes = 15
    n_intervals = 0
    interval_id = 'interval-component'
    store_id = 'tab-data'

    def __init__(self):
        self.h1_title = self.__class__.h1_title
        self.tabs_value = self.__class__.tabs_value
        self.div_id = self.__class__.div_id
        self.tabs = self.__class__.tabs
        self.starting_tab = self.__class__.starting_tab
        self.resync_interval_minutes = self.__class__.resync_interval_minutes
        self.n_intervals = self.__class__.n_intervals
        self.init_store()
        self.set_update_interval()
        self.init_layout()
    
    def init_store(self):
        self.store = dcc.Store(id=self.store_id,data={'n_intervals':0})

    @staticmethod
    def get_dynamic_tab_content(cls, active_tab):
        for tab in cls.tabs:
            if tab['tab'].value == active_tab:
                assert tab['type'] == 'dynamic'
                return tab['tab']().tab
        raise ValueError(f'Tab not found: {active_tab}')

    @staticmethod
    def minutes_to_milliseconds(minutes):
        return  minutes*60*1000

    def set_update_interval(self):
        assert self.resync_interval_minutes is not None
        minutes = self.resync_interval_minutes
        self.interval = dcc.Interval(id=self.interval_id,
                                     interval=self.minutes_to_milliseconds(
                                         minutes),
                                     n_intervals=self.n_intervals)

    def get_layout(self):
        self.init_layout()
        return self.layout
    
    def init_layout(self):
        self.set_update_interval()
        children=self.get_tabs()
        self.layout = html.Div([
            html.H1(self.h1_title),
            dcc.Tabs(id=self.tabs_value, value=children[0].value,
                     children=children),
            self.interval,
            self.store,
            html.Div(id=self.div_id)
        ])
    @staticmethod
    def get_dynamic_tabs(tabs):
        return [tab for tab in tabs if tab['type'] == 'dynamic']
    
    @staticmethod
    def get_dynamic_tab_values(tabs):
        return [tab['tab'] for tab in tabs if tab['type'] == 'dynamic']
    
    @staticmethod
    def check_if_tab_dynamic(cls,active_tab):
        dynamic_tabs = cls.get_dynamic_tab_values(cls.tabs)
        for dyanmic_tab in dynamic_tabs:
            if active_tab == dyanmic_tab.value:
                return True
        return False

    def get_tabs(self):
        children = []
        for tab_record in self.tabs:
            tab=tab_record['tab']
            children.append(tab.tab_child)
        return children

    
    def get_tab_cls(self,tab):
        for cls in self.tabs:
            if tab == cls['tab'].value:
                return cls['tab']
    
    def update_store(self,tab,store,interval):
        if tab not in store.keys():
            tab_cls = self.get_tab_cls(tab)
            store[tab]=tab_cls().tab
        if interval>store['n_intervals']:
            tab_cls = self.get_tab_cls(tab)
            store[tab]=tab_cls().tab
            store['n_intervals']=interval
        return store


class ExampleDashboard(Dashboard):
    h1_title = 'Dash Tabs component demo'
    tabs_value = "tabs-example-dash"
    div_id = 'tabs-content-example-dash'
    tabs = [
        {'tab': dt.ExampleMultiTab,'type':'static'},
        {'tab': dt.ExampleDropDownTab,'type':'dynamic'},
        {'tab': dt.ExampleTableTab,'type':'static'},
        {'tab': dt.ExampleScatterTab,'type':'static'},
    ]

    def __init__(self):
        Dashboard.__init__(self)

    @callback(
    Output(dt.ExampleDropDownTab.graph_id, 'figure'), #Graph id as figure output
    Input(dt.ExampleDropDownTab.dropdown_id, 'value') #Dropdown id as input
    )
    def update_graph(value):
        cls=dt.ExampleDropDownTab
        return cls.update_graph(cls, value)
    