#################################
###   Import des librairies   ###
#################################


import streamlit as st
from st_supabase_connection import SupabaseConnection
from data.cube import Cube
import data.constants as cst

from components.pages.page_home import page_home
from components.pages.page_404 import page_404

cube = Cube()


####################################
###   Configuration de la page   ###
####################################


st.set_page_config(page_title="Finary", page_icon="🪙", layout="wide")

st.title("Application de gestion de patrimoine")

columns = st.columns(spec=len(cst.PAGES_CONFIG))


def set_active_container(name: str):
    st.session_state["active_container"] = name


if "active_container" not in st.session_state:
    set_active_container(name="home")

if "is_user_logged" not in st.session_state:
    st.session_state["is_user_logged"] = False


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
            on_click=set_active_container,
            args=[page_config["name"]],
        )

st.divider()

with st.container():
    if st.session_state["active_container"] == "home":
        page_home()

    elif st.session_state["active_container"] == "situation":
        if st.session_state["is_user_logged"]:
            st.switch_page("pages/situation.py")
        else:
            conn = st.connection("supabase", type=SupabaseConnection)

            session = conn.auth.get_session()

            if session is not None:
                st.info("Une session a été récupérée...")

                user = conn.auth.get_user(jwt=session.access_token)

                if user is not None:
                    st.info("Un utilisateur a été récupéré...")

                    st.session_state["is_user_logged"] = True
                    st.session_state["user_data"] = user
                    st.switch_page("pages/situation.py")

            st.switch_page("pages/loggin.py")

    elif st.session_state["active_container"] == "summary":
        pass

    elif st.session_state["active_container"] == "analysis":
        pass

    else:
        page_404()
