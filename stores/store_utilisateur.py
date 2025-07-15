import streamlit as st
from st_supabase_connection import SupabaseConnection
from postgrest import APIError
from supabase import AuthApiError


def signout():
    try:
        conn = st.connection("supabase", type=SupabaseConnection)

        conn.auth.sign_out()

        st.session_state.clear()

        st.success("Vous vous êtes déconnecté avec succès ! A bientôt", icon="👋")

    except APIError as error:
        st.error(
            body=f"{error.code} : {error.message} - {error.details} - {error.hint}"
        )


def signin():
    try:
        conn = st.connection("supabase", type=SupabaseConnection)

        response = conn.auth.sign_in_with_password(
            {
                "email": st.session_state["input_signin_email"],
                "password": st.session_state["input_password"],
            }
        )

        st.session_state["is_user_logged"] = True
        st.session_state["user_data"] = response.user
        st.success(body="Vous êtes connecté à votre compte Finary.")

    except AuthApiError as error:
        st.session_state["is_user_logged"] = False
        st.error(f"{error.name} : {error.code} - {error.message}")


def reset_password():
    if len(st.session_state["input_signin_email"]) == 0:
        st.warning("Vous devez saisir votre email dans le champ de saisi de texte !")
        return

    conn = st.connection("supabase", type=SupabaseConnection)

    try:
        conn.auth.reset_password_for_email(
            st.session_state["input_signin_email"],
            {"redirect_to": "http://localhost:8501/reset_password"},
        )

        st.success(
            body="Un lien de réinitialisation de votre mot de passe vous a été envoyé."
        )

    except AuthApiError as error:
        st.session_state["is_user_logged"] = False
        st.error(f"{error.name} : {error.code} - {error.message}")
