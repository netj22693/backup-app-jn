import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure

'''
- Functions for creation of BASIC charts
'''

def create_pie_chart(
        df: pd.DataFrame,
        names: str,
        values: str,
        title: str | None = None, 
        drop_zero: bool = False, 
        drop_from: str | None = None
        ) -> Figure:


    # Drop rows with 0 costs to do not appear in the chart
    if drop_zero:
        index = df[(df[drop_from] == 0)].index
        df.drop(index, inplace=True)

    chart = px.pie(
        df, 
        names = names,
        values = values,
        title = title
    )

    # To display 2 decimals in the chart
    chart.update_traces(texttemplate="%{percent:.2%}")

    return chart


def create_bar_chart(
        df: pd.DataFrame,
        x_values:str | list,
        y_values:str | list,
        title: str = None
        ) -> Figure:

    fig_bar = px.bar(
        df, 
        x= x_values,
        y= y_values,
        title= title,
        )

    return fig_bar