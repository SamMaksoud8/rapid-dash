from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


class SubPlot:
    plot_type=None
    mode=None
    marker={'color': 'blue',
                    'size': 5,
                    'opacity': 0.6,
                    'symbol': 'circle'}
    
    line={'color': 'blue'}
    
    def __init__(self,df,x_name,y_name):
        self.df=df
        self.x_name = x_name
        self.y_name = y_name
        self.plot_name = y_name

    
    @property
    def x_values(self):
        return self.df[self.x_name]
      
    @property
    def y_values(self):
        return self.df[self.y_name]
    
    def generic_plot(self):
        """
        https://plotly.com/python/reference/
        """
        self.plot = {
                        'x': self.x_values,
                        'y': self.y_values,
                        'type': self.plot_type,
                        'mode': self.mode,
                        'marker': self.marker,
                        'line': self.line,
                    }


class BarPlot(SubPlot):
    def __init__(self,df,x_name,y_name):
        SubPlot.__init__(self,df,x_name,y_name)
        self.plot_type = "bar"
        self.generic_plot()
  
class ScatterPlot(SubPlot):
    def __init__(self,df,x_name,y_name):
        SubPlot.__init__(self,df,x_name,y_name)
        self.mode="markers"
        self.generic_plot()

class LinePlot(SubPlot):
    def __init__(self,df,x_name,y_name):
        SubPlot.__init__(self,df,x_name,y_name)
        self.mode="lines"
        self.generic_plot()

class ScatterLinePlot(SubPlot):
    def __init__(self,df,x_name,y_name):
        SubPlot.__init__(self,df,x_name,y_name)
        self.mode="lines+markers"
        self.generic_plot()

class DataTable:
    def __init__(self,id,df,columns=[]):
        self.id=id
        self.table=self.construct_table(df,columns)
        
    def filter_df(self,df,cols):
        return df if len(cols)==0 else df[cols]
    
    @property
    def plot(self):
        return self.table

    def construct_table(self,df,cols):
            df = self.filter_df(df,cols)
            return dash_table.DataTable(
                            id=self.id,
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict('records')
                        )
        

class Graph:
    def __init__(self,id,data,title=None,x_title=None,y_title=None,left_margin=60,bottom_margin=60,
                    top_margin=10,right_margin=10,x_legend=0,y_legend=1,hovermode="closest"):
        self.title = id if title is None else title
        self.id=id
        self.x_legend = x_legend
        self.y_legend = y_legend
        self.left_margin=left_margin
        self.bottom_margin=bottom_margin
        self.top_margin=top_margin
        self.right_margin=right_margin
        self.hovermode=hovermode
        self.init_data(data)
        self.init_axis_titles(x_title,y_title)
        self.plot_graph()
        
    def init_axis_titles(self,x_title,y_title):
        if x_title is None:
            try:
                self.x_title=self.data[0].x_name
            except:
                self.x_title="x"
        else:
            self.x_title=x_title
        
        if y_title is None:
            try:
                self.y_title=self.data[0].y_name
            except:
                self.y_title="y"
        else:
            self.y_title = y_title
        
        
    def init_data(self,data):
        if isinstance(data,list):
            data=data
        else:
            data=[data]
        self.data=data
            
    
    def layout(self):
        return go.Layout(
                    title=self.title,
                    xaxis={'title': self.x_title},
                    yaxis={'title': self.y_title},
                    margin={'l': self.left_margin, 'b': self.bottom_margin, 't': self.top_margin, 'r': self.right_margin},
                    legend={'x': self.x_legend, 'y': self.y_legend},
                    hovermode=self.hovermode
                )
        
    def render_data(self):
        data = []
        for i in self.data:
            if isinstance(i,dict):
                data.append(i)
            else:
                data.append(i.plot)
        return data
        
    def plot_graph(self):
        self.plot = dcc.Graph(
            id=self.id,
            figure={
                'data': self.render_data(),
                'layout': self.layout(), 
            }
        )


    