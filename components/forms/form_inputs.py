import streamlit as st


def number_input(label: str, key: str, help: str = None):
    st.number_input(
        label=label,
        key=key,
        min_value=0.0,
        format="%.2f",
        step=500.0,
        help=help,
    )
