import polars as pl
import streamlit as st
from loguru import logger
from st_supabase_connection import SupabaseConnection

from models.modele_utilisateur import Utilisateur


class Patrimoine:
    def __init__(self) -> None:
        self._df_patrimoine = pl.DataFrame()
        self.nom_table = "patrimoine"

        self.recuperer_le_patrimoine()

    @property
    def df_patrimoine(self):
        return self._df_patrimoine

    def ajouter_un_element_de_patrimoine(self, data: dict):
        try:
            logger.info("Ajout d'un nouvel élément de patrimoine...")

            conn = st.connection("supabase", type=SupabaseConnection)

            utilisateur: Utilisateur = st.session_state["utilisateur"]

            data["id_user"] = utilisateur.id

            response = conn.table(self.nom_table).insert(json=data).execute()

            if len(response.data) == 0:
                raise Exception("La source n'a pas pu être ajoutée.")

            logger.success("Le nouvel élément a bien été ajouté !")

            self.recuperer_le_patrimoine()

        except Exception as error:
            logger.error(error)

            st.error(
                "Une erreur est survenue et l'élément n'a pas pu être ajouté.",
                icon=":material/error:",
            )

    def supprimer_un_element_de_patrimoine(self):
        pass

    def recuperer_le_patrimoine(self):
        try:
            logger.info("Extraction du patrimoine de l'utilisateur.")

            conn = st.connection("supabase", type=SupabaseConnection)

            utilisateur: Utilisateur = st.session_state["utilisateur"]

            response = (
                conn.table(self.nom_table)
                .select("*")
                .eq("id_user", utilisateur.id)
                .execute()
            )

            df = pl.from_records(response.data)

            df = df.drop("id", "id_user")

            self._df_patrimoine = df

            logger.success(
                f"Patrimoine extrait avec succès ! {df.height} éléments trouvés."
            )

        except Exception as error:
            logger.error(error)

    def modifier_un_element_de_patrimoine(self):
        pass
