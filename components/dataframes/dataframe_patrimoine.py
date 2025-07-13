import streamlit as st
import polars as pl


def render_dataframe_patrimoine(dataframe: pl.DataFrame):
    selection = st.dataframe(
        data=dataframe,
        key="estate_sources_dataframe",
        width=900,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "id_patrimoine": None,
            "type": st.column_config.Column(label="Type"),
            "label": st.column_config.Column(label="Nom"),
            "amount": st.column_config.NumberColumn(label="Montant", format="%.2f €"),
            "deposit": st.column_config.NumberColumn(
                label="Apport annuel", format="%.2f €"
            ),
            "limit": st.column_config.NumberColumn(label="Plafond", format="%.2f €"),
            "return": st.column_config.NumberColumn(
                label="Rendement annuel", format="%.2f %%"
            ),
            "date_ouverture_patrimoine": st.column_config.DateColumn(
                label="Date d'ouverture du produit"
            ),
        },
    )

    selected_rows = selection.get("selection", {}).get("rows", [])

    if len(selected_rows) > 0:
        st.session_state["situation_configuration_mode"] = "edit"

        row_index = selected_rows[0]
        row = dataframe.row(index=row_index, named=True)

        st.session_state["input_estate_source_type"] = row["type"]
        st.session_state["input_estate_source_label"] = row["label"]
        st.session_state["input_estate_source_amount"] = row["amount"]
        st.session_state["input_estate_source_deposit"] = row["deposit"]
        st.session_state["input_estate_source_limit"] = row["limit"]
        st.session_state["input_estate_source_return"] = row["return"]
        st.session_state["input_date_ouverture_patrimoine"] = row[
            "date_ouverture_patrimoine"
        ]
        st.session_state["selected_estate_source_id"] = row["id_patrimoine"]

    else:
        st.session_state["situation_configuration_mode"] = "add"

        st.session_state["input_estate_source_type"] = None
        st.session_state["input_estate_source_label"] = None
        st.session_state["input_estate_source_amount"] = 0.0
        st.session_state["input_estate_source_deposit"] = 0.0
        st.session_state["input_estate_source_limit"] = None
        st.session_state["input_estate_source_return"] = 0.0
        st.session_state["input_date_ouverture_patrimoine"] = None
        st.session_state["selected_estate_source_id"] = None
