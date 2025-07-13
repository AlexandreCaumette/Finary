import streamlit as st
from data.cube import Cube
import data.module_state_management as state

cube = Cube()


def number_input(label: str, key: str, help: str = None):
    st.number_input(
        label=label,
        key=key,
        min_value=0.0,
        format="%.2f",
        step=500.0,
        help=help,
    )


def patch_button(on_click, key: str):
    if state.read_state(key) is not None:
        st.button(
            label="Modifier la source",
            icon=":material/edit:",
            key=f"{key}_add_button",
            type="primary",
            on_click=on_click,
        )
    else:
        st.button(
            label="Ajouter la source",
            help="Permet de créer et d'ajouter une source à l'étude",
            icon=":material/add:",
            type="primary",
            key=f"{key}_edit_button",
            on_click=on_click,
        )
