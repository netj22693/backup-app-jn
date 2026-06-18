import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "branch_type": ["Branch", "Headquarters", "Truck hub", "Rail hub", "Air hub"],
    "r": [67, 247, 63, 64, 6],
    "g": [166, 166, 94, 64, 187],
    "b": [82, 13, 219, 64, 204],
})


def color_name(row):
    color = f"background-color: rgb({row.r},{row.g},{row.b})"
    return [
        color,  # branch_type
        "",
        "",
        ""
    ]


styled = df.style.apply(
    color_name,
    axis=1
)

st.dataframe(styled)
