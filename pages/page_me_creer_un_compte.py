import streamlit as st

from models.modele_patrimoine import Patrimoine
from models.modele_produits import Produits
from models.modele_utilisateur import Utilisateur


def main_me_creer_un_compte():
    st.header("Me créer un compte Finary")

    st.space()

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

    st.space()

    if st.button(
        label="Créer mon compte",
        type="primary",
        help="S'authentifier avec les identifiants renseignés",
    ):
        with st.spinner(show_time=True, text="Création du compte en cours..."):
            utilisateur = Utilisateur()

            utilisateur.creer_un_compte(
                email=st.session_state["input_signin_email"],
                password=st.session_state["input_password"],
            )

            st.session_state["utilisateur"] = utilisateur

            patrimoine = Patrimoine()

            st.session_state["patrimoine"] = patrimoine

            produits = Produits()

            st.session_state["produits"] = produits

            st.switch_page(page="pages/page_accueil.py")


if __name__ == "__main__":
    main_me_creer_un_compte()
