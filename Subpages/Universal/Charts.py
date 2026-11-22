import plotly.express as px
import pandas as pd

'''
- Functions for creation of BASIC charts
'''


def create_pie_chart(df_input: pd.DataFrame, x_column: str , y_column: str):
    
    chart = px.pie(
    df_input, 
    names = df_input[f"{x_column}"],
    values = df_input[f"{y_column}"]
    )

    # To display 2 decimals in the chart
    chart.update_traces(texttemplate="%{percent:.2%}")

    return chart