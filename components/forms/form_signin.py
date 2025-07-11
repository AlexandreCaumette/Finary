import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import AuthApiError


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


def signin_form():
    with st.form(
        clear_on_submit=False,
        enter_to_submit=False,
        border=True,
        key="form_signin",
        width="stretch",
    ):
        st.subheader("Me connecter à mon compte")

        st.text_input(
            label="Email",
            help="Votre adresse email sera utilisée comme identifier pour vous authentifier.",
            placeholder="michel.michel@michel.com",
            icon="📧",
            autocomplete="email",
            key="input_signin_email",
        )

        st.text_input(
            label="Mot de passe",
            type="password",
            help="""Votre mot de passe doit contenir au minimum 16 caractères.""",
            placeholder="votre mot de passe",
            icon="🔐",
            key="input_password",
        )

        column_submit, column_forgotten = st.columns(2)

        with column_submit:
            st.form_submit_button(
                label="Me connecter",
                type="primary",
                help="S'authentifier avec les identifiants renseignés",
                on_click=signin,
                use_container_width=True,
            )

        with column_forgotten:
            st.form_submit_button(
                label="Réinitialiser mon mot de passe",
                type="secondary",
                on_click=reset_password,
                use_container_width=True,
                help="Vous devez saisir votre email dans le champ de saisi de texte pour débloquer ce bouton",
            )
