import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import AuthApiError, AuthSessionMissingError, AuthWeakPasswordError
from streamlit_url_fragment import get_fragment


def reset_password(query_params: dict):
    if (
        st.session_state["input_signup_confirmation_reset_password"]
        != st.session_state["input_reset_password"]
    ):
        st.warning(
            "La confirmation du mot de passe n'est pas identique au mot de passe !"
        )
        return

    if len(st.session_state["input_signup_confirmation_reset_password"]) <= 6:
        st.warning("Le mot de passe doit faire au minimum 7 caractères !")
        return

    conn = st.connection("supabase", type=SupabaseConnection)

    try:
        conn.auth.set_session(
            access_token=query_params["access_token"],
            refresh_token=query_params["refresh_token"],
        )

        conn.auth.update_user(
            {
                "password": st.session_state["input_reset_password"],
            },
        )

        st.session_state["is_user_logged"] = False
        st.success(body="Votre mot de passe a bien été réinitialisé.")

    except AuthApiError as error:
        st.session_state["is_user_logged"] = False
        st.error(body=f"{error.name} : {error.code} - {error.message}")

    except AuthSessionMissingError as error:
        st.error(body=f"{error.name} : {error.code} - {error.message}")

    except AuthWeakPasswordError as error:
        st.error(body=f"{error.name} : {error.code} - {error.message}")


def reset_password_form():
    fragments_string = get_fragment()

    if fragments_string is None:
        st.warning("Le token n'a pas encore été récupéré depuis l'URL...")
        st.stop()

    fragments = fragments_string[1:].split("&")

    fragments_keys_values = [fragment.split("=") for fragment in fragments]

    query_fragments = dict(fragments_keys_values)

    with st.form(
        clear_on_submit=False,
        enter_to_submit=False,
        border=True,
        key="form_reset_password",
        width="stretch",
    ):
        st.subheader("Réinitialiser mon mot de passe")

        st.text_input(
            label="Mot de passe",
            type="password",
            help="""Votre mot de passe doit contenir au minimum 16 caractères.""",
            placeholder="votre mot de passe",
            icon="🔐",
            key="input_reset_password",
        )

        st.text_input(
            label="Confirmation de mon mot de passe",
            type="password",
            help="""Le même mot de passe que vous venez de renseigner""",
            placeholder="le même mot de passe",
            icon="🔐",
            key="input_signup_confirmation_reset_password",
        )

        st.form_submit_button(
            label="Réinitialiser mon mot de passe",
            type="primary",
            help="S'authentifier avec les identifiants renseignés",
            on_click=reset_password,
            use_container_width=True,
            args=(query_fragments,),
        )
