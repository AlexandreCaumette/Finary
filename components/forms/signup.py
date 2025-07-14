import streamlit as st
from st_supabase_connection import SupabaseConnection


def signup():
    conn = st.connection("supabase", type=SupabaseConnection)

    response = conn.auth.sign_up(
        {
            "email": st.session_state["input_signup_email"],
            "password": st.session_state["input_signup_password"],
        }
    )

    if response.user.aud == "authenticated":
        st.session_state["is_user_logged"] = True
        st.session_state["user_data"] = response.user
        st.success(body="Vous êtes connecté à votre compte Finary.")

    else:
        st.session_state["is_user_logged"] = False
        st.error(
            body="Aucun utilisateur n'a été retrouvé avec cet email et ce mot de passe."
        )


def signup_form():
    with st.form(
        clear_on_submit=True,
        enter_to_submit=False,
        border=True,
        key="form_signup",
        width="stretch",
    ):
        st.subheader("Me créer un compte")

        st.text_input(
            label="Email",
            help="Votre adresse email sera utilisée comme identifier pour vous authentifier.",
            placeholder="michel.michel@michel.com",
            icon="📧",
            key="input_signup_email",
        )

        st.text_input(
            label="Mot de passe",
            type="password",
            help="""Votre mot de passe doit contenir au minimum 16 caractères.""",
            placeholder="votre mot de passe",
            icon="🔐",
            key="input_signup_password",
        )

        st.text_input(
            label="Confirmation de mon mot de passe",
            type="password",
            help="""Le même mot de passe que vous venez de renseigner""",
            placeholder="le même mot de passe",
            icon="🔐",
            key="input_signup_confirmation_password",
        )

        st.form_submit_button(
            label="Créer mon compte",
            type="primary",
            help="S'authentifier avec les identifiants renseignés",
            on_click=signup,
            use_container_width=True,
        )
