import streamlit as st


def number_input(label: str, key: str, value: float = 0.0, help: str | None = None):
    st.number_input(
        label=label,
        key=key,
        min_value=0.0,
        value=value,
        format="%.2f",
        step=500.0,
        help=help,
    )
