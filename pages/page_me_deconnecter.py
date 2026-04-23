import streamlit as st

from models.modele_utilisateur import Utilisateur


def main_me_deconnecter():
    utilisateur: Utilisateur = st.session_state["utilisateur"]

    utilisateur.deconnecter()

    st.switch_page(page="pages/page_accueil.py")


if __name__ == "__main__":
    main_me_deconnecter()
