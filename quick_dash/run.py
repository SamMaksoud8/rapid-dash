""" A module for running a dashboard application. """

from dash import Dash, dcc
from dash.dependencies import Input, Output,State
import dashboards as db
from typing import Type
import custom_dashboards as cd
import yaml



def start_dashboard(cls_name: str) -> None:
    dashboard = getattr(cd, cls_name)()
    #dashboard=dashboard_cls()
    dashboard.run(debug=True, port=8080)

        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run a custom dashboard')
    parser.add_argument('--dashboard',
                        help='The name of the dashboard to run',
                        choices=[name for name, obj in vars(cd).items() if (isinstance(obj, type) and issubclass(obj, cd.Dashboard))])
    args = parser.parse_args()
    start_dashboard(args.dashboard)