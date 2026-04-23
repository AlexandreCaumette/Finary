import polars as pl
import streamlit as st

from models.modele_produits import Produits


def main_produits():
    st.header("Gérer les produits d'épargne disponibles")

    produits: Produits = st.session_state["produits"]

    st.subheader("Editer la table des produits d'épargne")

    new_df_produits = st.data_editor(
        data=produits.df_produits,
        column_config={"rendement": st.column_config.NumberColumn(format="percent")},
        num_rows="dynamic",
        disabled=[col in ["id", "created_at"] for col in produits.df_produits.columns],
    )

    if not isinstance(new_df_produits, pl.DataFrame):
        return

    if produits.df_produits.equals(new_df_produits):
        return

    # Rows in df_1 but NOT in df_2
    only_in_df1 = produits.df_produits.join(
        new_df_produits, on=produits.df_produits.columns, how="anti"
    )

    # Rows in df_2 but NOT in df_1
    only_in_df2 = new_df_produits.join(
        produits.df_produits, on=new_df_produits.columns, how="anti"
    )

    df_changements = pl.concat([only_in_df1, only_in_df2])

    st.space()

    st.subheader("Contrôle des modifications apportées")

    if not df_changements.filter(pl.col("id").is_null()).is_empty():
        st.text("Nouvelles lignes à insérer")

        st.dataframe(df_changements.filter(pl.col("id").is_null()))

    if not df_changements.filter(pl.col("id").is_not_null()).is_empty():
        st.text("Lignes existantes à modifier")

        st.dataframe(df_changements.filter(pl.col("id").is_not_null()))

    if not df_changements.is_empty():
        st.space()

        if st.button(
            label="Mettre à jour la table des produits",
            type="primary",
            icon=":material/edit:",
        ):
            with st.spinner(
                show_time=True, text="Mise à jour des produits d'épargne..."
            ):
                produits.mettre_a_jour_les_produits(df_produits=df_changements)


if __name__ == "__main__":
    main_produits()
