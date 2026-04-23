import streamlit as st
from loguru import logger
from st_supabase_connection import SupabaseConnection


class Utilisateur:
    def __init__(self) -> None:
        self._donnees_utilisateur = None
        self._id = ""
        self._role = "utilisateur"

    @property
    def donnees_utilisateur(self):
        return self._donnees_utilisateur

    @property
    def id(self) -> str:
        return self._id

    @property
    def est_administrateur(self) -> bool:
        return self._role == "administrateur"

    def deconnecter(self):
        try:
            logger.info("Déconnexion de l'utilisateur...")

            conn = st.connection("supabase", type=SupabaseConnection)

            conn.auth.sign_out()

            for key in st.session_state.keys():
                del st.session_state[key]

            logger.success("L'utilisateur a bien été déconnecté !")

        except Exception as error:
            logger.error(error)

    def connecter(self, email: str, password: str):
        try:
            logger.info("Connexion de l'utilisateur...")

            conn = st.connection("supabase", type=SupabaseConnection)

            response = conn.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            st.session_state["is_user_logged"] = True

            if response.user is not None:
                self._donnees_utilisateur = response.user
                self._id = response.user.id

                self.recuperer_le_role()

            logger.success("L'utilisateur a bien été connecté !")

        except Exception as error:
            st.session_state["is_user_logged"] = False

            logger.error(error)

    def creer_un_compte(self, email: str, password: str):
        try:
            logger.info("Création du compte...")

            conn = st.connection("supabase", type=SupabaseConnection)

            response = conn.auth.sign_up({"email": email, "password": password})

            if response.user is not None and response.user.aud == "authenticated":
                st.session_state["is_user_logged"] = True
                self._donnees_utilisateur = response.user
                self._id = response.user.id

                conn.table("profile").insert(json={"id_user": self.id}).execute()

                self.recuperer_le_role()

            logger.success("L'utilisateur a bien été créé !")

        except Exception as error:
            st.session_state["is_user_logged"] = False

            logger.error(error)

    def recuperer_le_role(self):
        try:
            logger.info("Récupération du rôle...")

            conn = st.connection("supabase", type=SupabaseConnection)

            response = (
                conn.table("profile").select("*").eq("id_user", self.id).execute()
            )

            if len(response.data) > 0:
                self._role = response.data[0]["role"]  # type: ignore

                logger.success(
                    f"Le rôle a bien été récupéré ! {len(response.data)} éléments trouvés."
                )

            else:
                self._role = "utilisateur"

                logger.warning(
                    f"Le rôle n'a pas pu être récupéré et sera donc 'utilisateur' ! {len(response.data)} éléments trouvés."
                )

        except Exception as error:
            st.session_state["is_user_logged"] = False

            logger.error(error)
