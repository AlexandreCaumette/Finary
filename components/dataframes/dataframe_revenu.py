import streamlit as st
import polars as pl


def render_dataframe_revenu(dataframe: pl.DataFrame):
    selection = st.dataframe(
        data=dataframe,
        key="income_sources_dataframe",
        width=1000,
        selection_mode="single-row",
        on_select="rerun",
        column_config={
            "id_revenu": None,
            "montant_revenu": st.column_config.NumberColumn(
                label="Montant", format="%.2f €"
            ),
            "pourcentage_augmentation": st.column_config.NumberColumn(
                label="Augmentation annuelle (%)",
                help="Pourcentage d'augmentation annuel moyen à utiliser pour les projections.",
                format="%.2f %%",
            ),
        },
    )

    selected_rows = selection.get("selection", {}).get("rows", [])

    if len(selected_rows) > 0:
        st.session_state["situation_configuration_mode"] = "edit"

        row_index = selected_rows[0]
        row = dataframe.row(index=row_index, named=True)

        st.session_state["input_type_revenu"] = row["type_revenu"]
        st.session_state["input_label_revenu"] = row["label_revenu"]
        st.session_state["input_montant_revenu"] = row["montant_revenu"]
        st.session_state["input_pourcentage_augmentation"] = row[
            "pourcentage_augmentation"
        ]
        st.session_state["selected_id_revenu"] = row["id_revenu"]

    else:
        st.session_state["situation_configuration_mode"] = "add"

        st.session_state["input_type_revenu"] = None
        st.session_state["input_label_revenu"] = None
        st.session_state["input_montant_revenu"] = 0.0
        st.session_state["input_pourcentage_augmentation"] = 0.0
        st.session_state["selected_id_revenu"] = None
