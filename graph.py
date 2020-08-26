"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from _plotly_future_ import v4_subplots
import plotly as py
from plotly import graph_objs as go
from plotly.subplots import make_subplots

from const import x_str, y_str, combined_graph_opacity


def generate_line_graph(data, data2=None):
    """
    Generate line graph using Plotly with input data
    :param data: data used to generate graph
    :param data2: another set of data used to compare different metrics (optional)
    :return: plot div
    """
    if data2 is None:
        data = go.Scatter(x=data[x_str], y=data[y_str], name='bitrate')
        plot = py.offline.plot([data], output_type='div', auto_open=False)
    else:
        data = go.Scatter(x=data[x_str], y=data[y_str], name='bitrate', opacity=combined_graph_opacity)
        data2 = go.Scatter(x=data2[x_str], y=data2[y_str], name='qp', opacity=combined_graph_opacity)
        fig = make_subplots(specs=[[{'secondary_y': True}]])
        fig.add_trace(data, secondary_y=False)
        fig.add_trace(data2, secondary_y=True)
        fig.update_yaxes(title_text='bitrate', secondary_y=False)
        fig.update_yaxes(title_text='qp', secondary_y=True)
        plot = py.offline.plot(fig, output_type='div', auto_open=False)
    return plot
