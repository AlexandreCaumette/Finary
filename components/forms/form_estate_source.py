import streamlit as st
from st_supabase_connection import SupabaseConnection
import polars as pl

import data.constants as cst

from components.forms.form_inputs import number_input


def insert_patrimoine():
    conn = st.connection("supabase", type=SupabaseConnection)

    response = (
        conn.table("PATRIMOINE")
        .insert(
            {
                "type": st.session_state("input_estate_source_type"),
                "label": st.session_state("input_estate_source_label"),
                "amount": st.session_state("input_estate_source_amount"),
                "deposit": st.session_state("input_estate_source_deposit"),
                "limit": st.session_state("input_estate_source_limit"),
                "return": st.session_state("input_estate_source_return"),
                "user_id": st.session_state["user_data"]["id"],
            }
        )
        .execute()
    )

    if len(response.data) == 0:
        st.error("La source n'a pas pu être ajoutée.")

    else:
        st.success("La nouvelle source a été ajoutée avec succès", icon="💸")
        st.session_state["patrimoine_dataframe"] = pl.concat(
            st.session_state["patrimoine_dataframe"], pl.from_records(response.data)
        )


def update_patrimoine():
    conn = st.connection("supabase", type=SupabaseConnection)

    response = (
        conn.table("PATRIMOINE")
        .update(
            {
                "type": st.session_state["input_estate_source_type"],
                "label": st.session_state["input_estate_source_label"],
                "amount": st.session_state["input_estate_source_amount"],
                "deposit": st.session_state["input_estate_source_deposit"],
                "limit": st.session_state["input_estate_source_limit"],
                "return": st.session_state["input_estate_source_return"],
            }
        )
        .eq("id_patrimoine", st.session_state["select_estate_source_id"])
        .execute()
    )

    if len(response.data) == 0:
        st.error("La source n'a pas pu être modifiée.")

    else:
        st.success("La source a été modifiée avec succès", icon="💸")
        st.session_state["patrimoine_dataframe"] = st.session_state[
            "patrimoine_dataframe"
        ].update(pl.from_records(response.data), on="id_patrimoine")
        st.session_state["situation_configuration_mode"] = "add"


def delete_patrimoine():
    conn = st.connection("supabase", type=SupabaseConnection)

    response = (
        conn.table("PATRIMOINE")
        .delete()
        .eq("id_patrimoine", st.session_state["select_estate_source_id"])
        .execute()
    )

    if len(response.data) == 0:
        st.error("La source n'a pas pu être supprimée.")

    else:
        st.success("La source a été supprimée avec succès", icon="💸")
        st.session_state["patrimoine_dataframe"] = st.session_state[
            "patrimoine_dataframe"
        ].filter(pl.col("id_patrimoine") == response.data[0]["id_patrimoine"])
        st.session_state["situation_configuration_mode"] = "add"


def estate_source_form():
    with st.form(
        key="estate_sources_form",
        clear_on_submit=True,
        width="content",
        enter_to_submit=False,
    ):
        st.subheader(body="Formulaire d'édition de source")

        st.selectbox(
            label="Type de patrimoine",
            placeholder=", ".join(cst.ESTATE_SOURCES_LIST[:2]),
            options=cst.ESTATE_SOURCES_LIST,
            key="input_estate_source_type",
            index=None,
        )

        st.text_input(
            "Label",
            key="input_estate_source_label",
            placeholder="PEA, SCPI, Bitcoin, ...",
        )

        number_input(
            label="Montant (€)",
            key="input_estate_source_amount",
        )

        number_input(
            label="Apport annuel (€)",
            help="L'argent que vous apportez à ce placement chaque année",
            key="input_estate_source_deposit",
        )

        number_input(
            label="Plafond (€)",
            key="input_estate_source_limit",
            help="Le plafond concerne notamment les livrets d'épargne. Si cette source n'a pas de plafond, laissez le champ vide",
        )

        number_input(
            label="Rendement annuel (%)",
            key="input_estate_source_return",
        )

        column_add, column_remove = st.columns(2)

        with column_add:
            st.form_submit_button(
                label="Ajouter"
                if st.session_state["situation_configuration_mode"] == "add"
                else "Modifier",
                on_click=insert_patrimoine
                if st.session_state["situation_configuration_mode"] == "add"
                else update_patrimoine,
                icon=":material/add:"
                if st.session_state["situation_configuration_mode"] == "add"
                else ":material/edit:",
                type="primary",
                use_container_width=True,
            )

        with column_remove:
            if st.session_state["situation_configuration_mode"] != "add":
                st.form_submit_button(
                    label="Supprimer",
                    help="Retire cette source de la liste des sources de patrimoine",
                    icon=":material/clear:",
                    on_click=delete_patrimoine,
                    use_container_width=True,
                )
