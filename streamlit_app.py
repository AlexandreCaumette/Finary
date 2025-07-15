#################################
###   Import des librairies   ###
#################################


import streamlit as st
import data.constants as cst
import stores.store_utilisateur as store_utilisateur


####################################
###   Configuration de la page   ###
####################################


st.set_page_config(page_title="Finary", page_icon="🪙", layout="wide")

pages = [
    st.Page(
        page=f"pages/{page_config['name']}.py",
    )
    for page_config in cst.PAGES_CONFIG
]

current_page = st.navigation(pages=pages, position="hidden")

if "is_user_logged" not in st.session_state:
    st.session_state["is_user_logged"] = False

st.title("Application de gestion de patrimoine")

st.divider()

with st.sidebar:
    for page_config in cst.PAGES_CONFIG:
        if page_config["visible"]:
            st.page_link(
                page=f"pages/{page_config['name']}.py",
                label=page_config.get("label", None),
                icon=page_config["icon"],
                help=page_config.get("help", None),
                disabled=page_config["name"] != "home"
                and not st.session_state["is_user_logged"],
            )

    st.divider()

    if st.session_state["is_user_logged"]:
        logout_button = st.button(
            label="Me déconnecter",
            icon=":material/logout:",
            on_click=store_utilisateur.signout,
        )

        if logout_button:
            st.switch_page("pages/home.py")

    else:
        login_button = st.button(
            label="Me connecter",
            icon=":material/login:",
        )

        if login_button:
            st.switch_page(page=r"pages/login.py")

current_page.run()
