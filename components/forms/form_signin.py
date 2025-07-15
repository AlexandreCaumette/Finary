import streamlit as st
from stores import store_utilisateur
from stores import store_patrimoine
from stores import store_revenu


def signin():
    store_utilisateur.signin()

    if st.session_state["is_user_logged"]:
        store_patrimoine.fetch_patrimoine()
        store_revenu.fetch_revenu()


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
                on_click=store_utilisateur.reset_password,
                use_container_width=True,
                help="Vous devez saisir votre email dans le champ de saisi de texte pour débloquer ce bouton",
            )
