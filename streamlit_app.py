import pathlib

import streamlit as st

from models.modele_utilisateur import Utilisateur


def main():
    st.set_page_config(page_title="Finary", page_icon="🪙", layout="wide")

    st.title("Application de gestion de patrimoine")

    st.divider()

    if "is_user_logged" not in st.session_state:
        st.session_state["is_user_logged"] = False

    pages = {
        "Navigation": [
            st.Page(
                page=pathlib.Path("pages") / "page_accueil.py",
                title="Accueil",
                icon="🏠",
                default=True,
            ),
            st.Page(
                page=pathlib.Path("pages") / "page_situation.py",
                title="Ma situation",
                icon="📝",
            ),
            st.Page(
                page=pathlib.Path("pages") / "page_summary.py",
                title="Ma tableau de bord",
                icon="📊",
                visibility="visible"
                if st.session_state["is_user_logged"]
                else "hidden",
            ),
            st.Page(
                page=pathlib.Path("pages") / "page_analysis.py",
                title="Analyse de ma situation",
                icon="👨🏻‍🏫",
                visibility="visible"
                if st.session_state["is_user_logged"]
                else "hidden",
            ),
        ],
        "Mon compte": [
            st.Page(
                page=pathlib.Path("pages") / "page_me_creer_un_compte.py",
                title="Me créer un compte",
                icon=":material/accessibility_new:",
                url_path="me-creer-un-compte",
            )
        ],
    }

    page_me_connecter = st.Page(
        page=pathlib.Path("pages") / "page_me_connecter.py",
        title="Me connecter",
        icon=":material/login:",
        url_path="me-connecter",
    )

    page_me_deconnecter = st.Page(
        page=pathlib.Path("pages") / "page_me_deconnecter.py",
        title="Me déconnecter",
        icon=":material/logout:",
        url_path="me-deconnecter",
    )

    if st.session_state["is_user_logged"]:
        pages["Mon compte"].append(page_me_deconnecter)

        utilisateur: Utilisateur = st.session_state["utilisateur"]

        if utilisateur.est_administrateur:
            pages["Admin"] = [
                st.Page(
                    page=pathlib.Path("pages") / "page_produits.py",
                    title="Gérer les produits",
                    icon=":material/wallet:",
                    url_path="gerer-produits",
                )
            ]

    else:
        pages["Mon compte"].append(page_me_connecter)

    current_page = st.navigation(pages=pages)

    current_page.run()


if __name__ == "__main__":
    main()
