import polars as pl
import streamlit as st
from loguru import logger
from st_supabase_connection import SupabaseConnection

from models.modele_utilisateur import Utilisateur


class Produits:
    def __init__(self) -> None:
        self.nom_table = "produit"
        self._df_produit = pl.DataFrame()

        self.recuperer_les_produits()

    @property
    def df_produits(self):
        return self._df_produit

    def recuperer_les_produits(self):
        try:
            logger.info("Extraction des produits d'épargne...")

            conn = st.connection("supabase", type=SupabaseConnection)

            response = conn.table(self.nom_table).select("*").execute()

            df = pl.from_records(response.data)

            df = df.with_columns(pl.col("plafond").cast(pl.Float64))

            self._df_produit = df

            logger.success(
                f"Produits extraits avec succès ! {df.height} éléments trouvés."
            )

        except Exception as error:
            logger.error(error)

    def mettre_a_jour_les_produits(self, df_produits: pl.DataFrame):
        try:
            logger.info("Mise à jour des produits d'épargne...")

            utilisateur: Utilisateur = st.session_state["utilisateur"]

            if not utilisateur.est_administrateur:
                raise Exception(
                    "Seul les administrateurs peuvent mettre à jour les produits d'épargne !"
                )

            conn = st.connection("supabase", type=SupabaseConnection)

            response = (
                conn.table(self.nom_table)
                .upsert(json=df_produits.rows(named=True))
                .execute()
            )

            response.data

            logger.success(
                f"Produits mis à jour avec succès ! {len(response.data)} éléments trouvés."
            )

            self.recuperer_les_produits()

        except Exception as error:
            logger.error(error)

            st.error(
                "Une erreur est survenue lors de la mise à jour des produits !",
                icon=":material/error:",
            )
