import streamlit as st
from st_supabase_connection import SupabaseConnection
from postgrest import APIError


def insert_patrimoine():
    try:
        payload = {
            "type": st.session_state["input_estate_source_type"],
            "label": st.session_state["input_estate_source_label"],
            "amount": st.session_state["input_estate_source_amount"],
            "deposit": st.session_state["input_estate_source_deposit"],
            "limit": st.session_state["input_estate_source_limit"],
            "return": st.session_state["input_estate_source_return"],
            "date_ouverture_patrimoine": st.session_state[
                "input_date_ouverture_patrimoine"
            ],
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
            "date_ouverture_patrimoine": st.session_state[
                "input_date_ouverture_patrimoine"
            ],
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
