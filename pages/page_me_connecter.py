import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import AuthApiError

from models import modele_patrimoine, modele_produits, modele_utilisateur


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


def main_me_connecter():
    st.header("Me connecter à mon compte Finary")

    st.space()

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

    st.space()

    column_submit, column_forgotten = st.columns(2)

    with column_submit:
        if st.button(
            label="Me connecter",
            type="primary",
            help="S'authentifier avec les identifiants renseignés",
            use_container_width=True,
            icon=":material/login:",
        ):
            with st.spinner(show_time=True, text="Connexion en cours..."):
                utilisateur = modele_utilisateur.Utilisateur()

                utilisateur.connecter(
                    email=st.session_state["input_signin_email"],
                    password=st.session_state["input_password"],
                )

                st.session_state["utilisateur"] = utilisateur

                patrimoine = modele_patrimoine.Patrimoine()

                st.session_state["patrimoine"] = patrimoine

                produits = modele_produits.Produits()

                st.session_state["produits"] = produits

                st.switch_page(page="pages/page_accueil.py")

    with column_forgotten:
        st.button(
            label="Réinitialiser mon mot de passe",
            type="secondary",
            on_click=reset_password,
            use_container_width=True,
            icon=":material/lock_reset:",
            help="Vous devez saisir votre email dans le champ de saisi de texte pour débloquer ce bouton",
        )


if __name__ == "__main__":
    main_me_connecter()
