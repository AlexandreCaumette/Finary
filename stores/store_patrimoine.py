import streamlit as st
from st_supabase_connection import SupabaseConnection
from postgrest import APIError
import polars as pl


def fetch_patrimoine():
    try:
        conn = st.connection("supabase", type=SupabaseConnection)

        response = (
            conn.table("PATRIMOINE")
            .select(
                "id_patrimoine",
                "type, label, amount, deposit, limit, return, date_ouverture_patrimoine",
            )
            .eq("id_user", st.session_state["user_data"].id)
            .execute()
        )

        dataframe = pl.from_records(response.data)

        dataframe = dataframe.with_columns(
            pl.col("date_ouverture_patrimoine").str.to_date(format="%Y-%m-%d")
        )

        st.session_state["df_patrimoine"] = dataframe

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


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

        if st.session_state["input_date_ouverture_patrimoine"] is not None:
            payload["date_ouverture_patrimoine"] = st.session_state[
                "input_date_ouverture_patrimoine"
            ].isoformat()

        conn = st.connection("supabase", type=SupabaseConnection)

        (conn.table("PATRIMOINE").insert(json=payload, default_to_null=False).execute())

        fetch_patrimoine()

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

        if st.session_state["input_date_ouverture_patrimoine"] is not None:
            payload["date_ouverture_patrimoine"] = st.session_state[
                "input_date_ouverture_patrimoine"
            ].isoformat()

        conn = st.connection("supabase", type=SupabaseConnection)

        (
            conn.table("PATRIMOINE")
            .update(json=payload)
            .eq("id_patrimoine", st.session_state["selected_estate_source_id"])
            .execute()
        )

        fetch_patrimoine()

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

        fetch_patrimoine()

        st.success("La source a été supprimée avec succès", icon="💸")
        st.session_state["situation_configuration_mode"] = "add"

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


def get_df_patrimoine() -> pl.DataFrame:
    if "df_patrimoine" in st.session_state:
        return st.session_state["df_patrimoine"]

    return pl.DataFrame()
