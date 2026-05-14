import pandas as pd
import plotly.graph_objects as go



def create_chart(df, column_x, column_y, color_line, legend_name, currency):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[column_x],
            y=df[column_y],
            mode="lines",
            name=legend_name,
            line=dict(
                color=color_line,
                width=2.5,
                shape="spline"
            ),
            hovertemplate=
                f"%{{y:.2f}} {currency}<extra></extra>"
        )
    )

    # last point
    fig.add_trace(
        go.Scatter(
            x=[df[column_x].iloc[-1]],
            y=[df[column_y].iloc[-1]],
            mode="markers",
            marker=dict(
                color=color_line,
                size=7
            ),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    fig.update_layout(
        height=360,
        margin=dict(l=0, r=0, t=10, b=0),

        paper_bgcolor="white",
        plot_bgcolor="white",

        hovermode="x",

        xaxis=dict(
            title="",
            showgrid=False,
            showline=False,
            zeroline=False,
            tickfont=dict(color="#888"),
        ),

        yaxis=dict(
            title="",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False,
            tickfont=dict(color="#888"),
        )
    )

    return fig