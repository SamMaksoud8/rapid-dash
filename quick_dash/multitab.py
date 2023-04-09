""" A module for running a dashboard application. """

from dash import Dash, dcc
from dash.dependencies import Input, Output,State
import dashboards as db
from typing import Type

def main(cls: Type[db.Dashboard]) -> None:
    """
    Runs a Dash application based on the provided `dashboard_cls`.

    Parameters:
    -----------
    cls : Type[Dashboard]
        A subclass of `Dashboard` that defines the layout and callbacks for the Dash application.

    Returns:
    --------
    None
    """
    dashboard=cls()
    dashboard.run(debug=True, port=8080)

if __name__ == '__main__':
    main(db.ExampleDashboard)
