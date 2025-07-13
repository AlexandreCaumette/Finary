import streamlit as st
from st_supabase_connection import SupabaseConnection
from postgrest import APIError


def insert_revenu():
    try:
        payload = {
            "type_revenu": st.session_state["input_type_revenu"],
            "label_revenu": st.session_state["input_label_revenu"],
            "montant_revenu": st.session_state["input_montant_revenu"],
            "pourcentage_augmentation": st.session_state[
                "input_pourcentage_augmentation"
            ],
            "id_user": st.session_state["user_data"].id,
        }

        conn = st.connection("supabase", type=SupabaseConnection)

        (conn.table("REVENUS").insert(json=payload, default_to_null=False).execute())

        st.success("La nouvelle source a été ajoutée avec succès", icon="💸")

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


def update_revenu():
    try:
        payload = {
            "type_revenu": st.session_state["input_type_revenu"],
            "label_revenu": st.session_state["input_label_revenu"],
            "montant_revenu": st.session_state["input_montant_revenu"],
            "pourcentage_augmentation": st.session_state[
                "input_pourcentage_augmentation"
            ],
            "id_user": st.session_state["user_data"].id,
            "id_revenu": st.session_state["selected_id_revenu"],
        }

        conn = st.connection("supabase", type=SupabaseConnection)

        (
            conn.table("REVENUS")
            .update(json=payload)
            .eq("id_revenu", st.session_state["selected_id_revenu"])
            .execute()
        )

        st.success("La source a été modifiée avec succès", icon="💸")
        st.session_state["situation_configuration_mode"] = "add"

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


def delete_revenu():
    try:
        conn = st.connection("supabase", type=SupabaseConnection)

        (
            conn.table("REVENUS")
            .delete()
            .eq("id_revenu", st.session_state["selected_id_revenu"])
            .execute()
        )

        st.success("La source a été supprimée avec succès", icon="💸")
        st.session_state["situation_configuration_mode"] = "add"

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )
