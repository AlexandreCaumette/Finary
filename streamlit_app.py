#################################
###   Import des librairies   ###
#################################


import streamlit as st
from st_supabase_connection import SupabaseConnection
from data.cube import Cube
import data.constants as cst

cube = Cube()


####################################
###   Configuration de la page   ###
####################################


st.set_page_config(page_title="Finary", page_icon="🪙", layout="wide")

if "is_user_logged" not in st.session_state:
    st.session_state["is_user_logged"] = False

st.title("Application de gestion de patrimoine")

columns = st.columns(spec=len(cst.PAGES_CONFIG))


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


for index_col, page_config in enumerate(cst.PAGES_CONFIG):
    with columns[index_col]:
        st.button(
            label=page_config["label"],
            icon=page_config["icon"],
            disabled=page_config["disabled"],
            help=page_config.get("help", None),
            use_container_width=True,
            type="primary"
            if page_config["name"] == st.session_state["active_container"]
            else "secondary",
            on_click=select_page,
            kwargs={"name": page_config["name"]},
        )
