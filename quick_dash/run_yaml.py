""" A module for running a dashboard application. """

from dash import Dash, dcc
from dash.dependencies import Input, Output,State
from dashboards import AutoDash
from typing import Type
import yaml



def start_dashboard(yaml_path: str) -> None:
    dashboard = AutoDash.from_yaml(yaml_path)
    #dashboard=dashboard_cls()
    dashboard.run(debug=True, port=8080)

        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run a custom dashboard')
    
    parser.add_argument('--yaml-path',
                        help='The path to the yaml config for a dashboard.')
    args = parser.parse_args()
    start_dashboard(args.yaml_path)