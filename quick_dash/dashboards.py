from dash import Dash, html, dcc, callback, Output, Input, State
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import custom_tabs as ct
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
        self.init_store()
        self.set_update_interval()
        self.init_layout()
    
    def init_store(self):
        self.store = dcc.Store(id=self.store_id,data={'n_intervals':0})

    @staticmethod
    def get_dynamic_tab_content(cls, active_tab):
        for tab in cls.tabs:
            if tab.value == active_tab:
                assert tab.sync_type == 'dynamic'
                return tab().tab
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
    def check_if_tab_dynamic(cls,active_tab):
        for tab in cls.tabs:
            if tab.sync_type == 'dynamic':
                if active_tab == tab.value:
                    return True
        return False

    def get_tabs(self):
        children = []
        for tab in self.tabs:
            children.append(dcc.Tab(label=tab.label, value=tab.value))
        return children

    
    def get_tab_cls(self,tab):
        for cls in self.tabs:
            if tab == cls.value:
                return cls
    
    def update_store(self,tab,store,interval):
        if tab not in store.keys():
            print(store.keys())
            tab_cls = self.get_tab_cls(tab)
            store[tab]=tab_cls().tab
        else:
            print('saved time',tab)
        if interval>store['n_intervals']:
            tab_cls = self.get_tab_cls(tab)
            store[tab]=tab_cls().tab
            store['n_intervals']=interval
        return store


class ExampleDashboard(Dashboard):
    h1_title = 'Dash Tabs component demo'
    tabs_value = "tabs-example-dash"
    div_id = 'tabs-content-example-dash'
    tabs = [ct.ExampleMultiTab,
            ct.ExampleDropDownTab,
            ct.ExampleTableTab,
            ct.ExampleScatterTab]

    def __init__(self):
        Dashboard.__init__(self)

    @callback(
    Output(ct.ExampleDropDownTab.graph_id, 'figure'), #Graph id as figure output
    Input(ct.ExampleDropDownTab.dropdown_id, 'value') #Dropdown id as input
    )
    def update_graph(value):
        cls=ct.ExampleDropDownTab
        return cls.update_graph(cls, value)
    