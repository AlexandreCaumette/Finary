#################################
###   Import des librairies   ###
#################################


import streamlit as st
from st_supabase_connection import SupabaseConnection
import data.constants as cst
import os


####################################
###   Configuration de la page   ###
####################################


st.set_page_config(page_title="Finary", page_icon="🪙", layout="wide")

if "is_user_logged" not in st.session_state:
    st.session_state["is_user_logged"] = False

st.title("Application de gestion de patrimoine")

pages = [
    st.Page(
        page=f"pages/{page_config['name']}.py",
    )
    for page_config in cst.PAGES_CONFIG
]

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
        st.button(
            label="Me déconnecter",
            icon=":material/logout:",
        )

    else:
        login_button = st.button(
            label="Me connecter",
            icon=":material/login:",
        )

        if login_button:
            print(os.path.exists("pages/login.py"))
            st.switch_page(page=r"pages/login.py")

current_page = st.navigation(pages=pages, position="hidden")

current_page.run()


def select_page(name: str):
    if name == "home":
        st.switch_page(f"pages/{name}.py")

    elif st.session_state["is_user_logged"]:
        st.switch_page(f"pages/{name}.py")

    else:
        conn = st.connection("supabase", type=SupabaseConnection)

        session = conn.auth.get_session()

        if session is None:
            st.warning("Aucune session n'a été trouvée, veuillez vous connecter.")
            st.switch_page("pages/loggin.py")

        else:
            st.info("Une session a été récupérée...")

            user = conn.auth.get_user(jwt=session.access_token)

            if user is None:
                st.warning("Aucun utilisateur n'a été trouvé, veuillez vous connecter.")
                st.switch_page("pages/loggin.py")

            else:
                st.info("Un utilisateur a été récupéré...")
                st.session_state["is_user_logged"] = True
                st.session_state["user_data"] = user
                st.switch_page(f"pages/{name}.py")
