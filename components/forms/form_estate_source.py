import streamlit as st
from st_supabase_connection import SupabaseConnection
from postgrest import APIError
import polars as pl

import data.constants as cst

from components.forms.form_inputs import number_input


def insert_patrimoine():
    try:
        payload = {
            "type": st.session_state["input_estate_source_type"],
            "label": st.session_state["input_estate_source_label"],
            "amount": st.session_state["input_estate_source_amount"],
            "deposit": st.session_state["input_estate_source_deposit"],
            "limit": st.session_state["input_estate_source_limit"],
            "return": st.session_state["input_estate_source_return"],
            "id_user": st.session_state["user_data"].id,
        }

        conn = st.connection("supabase", type=SupabaseConnection)

        (conn.table("PATRIMOINE").insert(json=payload, default_to_null=False).execute())

        st.success("La nouvelle source a été ajoutée avec succès", icon="💸")

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


def update_patrimoine():
    try:
        payload = {
            "type": st.session_state["input_estate_source_type"],
            "label": st.session_state["input_estate_source_label"],
            "amount": st.session_state["input_estate_source_amount"],
            "deposit": st.session_state["input_estate_source_deposit"],
            "limit": st.session_state["input_estate_source_limit"],
            "return": st.session_state["input_estate_source_return"],
            "id_user": st.session_state["user_data"].id,
            "id_patrimoine": st.session_state["selected_estate_source_id"],
        }

        conn = st.connection("supabase", type=SupabaseConnection)

        (
            conn.table("PATRIMOINE")
            .update(json=payload)
            .eq("id_patrimoine", st.session_state["selected_estate_source_id"])
            .execute()
        )

        st.success("La source a été modifiée avec succès", icon="💸")
        st.session_state["situation_configuration_mode"] = "add"

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


def delete_patrimoine():
    try:
        conn = st.connection("supabase", type=SupabaseConnection)

        (
            conn.table("PATRIMOINE")
            .delete()
            .eq("id_patrimoine", st.session_state["select_estate_source_id"])
            .execute()
        )

        st.success("La source a été supprimée avec succès", icon="💸")
        st.session_state["situation_configuration_mode"] = "add"

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


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
            value=None,
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
