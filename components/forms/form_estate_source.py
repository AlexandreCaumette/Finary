import polars as pl
import streamlit as st
from st_supabase_connection import SupabaseConnection

from components.components import number_input
from models.modele_patrimoine import Patrimoine
from models.modele_produits import Produits


def insert_patrimoine(id_produit: str):
    data = {
        "id_produit": id_produit,
        "label": st.session_state["input_estate_source_label"],
        "montant": st.session_state["input_estate_source_amount"],
        "plafond": st.session_state["input_estate_source_limit"],
        "rendement": st.session_state["input_estate_source_return"],
    }

    patrimoine: Patrimoine = st.session_state["patrimoine"]

    patrimoine.ajouter_un_element_de_patrimoine(data=data)


def update_patrimoine():
    conn = st.connection("supabase", type=SupabaseConnection)

    response = (
        conn.table("PATRIMOINE")
        .update(
            {
                "type": st.session_state["input_estate_source_type"],
                "label": st.session_state["input_estate_source_label"],
                "amount": st.session_state["input_estate_source_amount"],
                "limit": st.session_state["input_estate_source_limit"],
                "return": st.session_state["input_estate_source_return"],
            }
        )
        .eq("id_patrimoine", st.session_state["select_estate_source_id"])
        .execute()
    )

    if len(response.data) == 0:
        st.error("La source n'a pas pu être modifiée.")

    else:
        st.success("La source a été modifiée avec succès", icon="💸")
        st.session_state["patrimoine_dataframe"] = st.session_state[
            "patrimoine_dataframe"
        ].update(pl.from_records(response.data), on="id_patrimoine")
        st.session_state["situation_configuration_mode"] = "add"


def delete_patrimoine():
    conn = st.connection("supabase", type=SupabaseConnection)

    response = (
        conn.table("PATRIMOINE")
        .delete()
        .eq("id_patrimoine", st.session_state["select_estate_source_id"])
        .execute()
    )

    if len(response.data) == 0:
        st.error("La source n'a pas pu être supprimée.")

    else:
        st.success("La source a été supprimée avec succès", icon="💸")
        st.session_state["patrimoine_dataframe"] = st.session_state[
            "patrimoine_dataframe"
        ].filter(pl.col("id_patrimoine") == response.data[0]["id_patrimoine"])
        st.session_state["situation_configuration_mode"] = "add"


def formulaire_patrimoine():
    st.subheader(body="Formulaire d'édition de source")

    produits: Produits = st.session_state["produits"]

    options_produit_d_epargne = produits.df_produits["label"].sort().to_list()

    label_produit = st.selectbox(
        label="Produit d'épargne",
        options=options_produit_d_epargne,
        key="input_estate_source_type",
        index=None,
    )

    if label_produit is None:
        return

    produit = produits.df_produits.filter(pl.col("label").eq(label_produit)).rows(
        named=True
    )[0]

    st.text_input(
        label="Label",
        value=label_produit,
        key="input_estate_source_label",
        placeholder="PEA, SCPI, Bitcoin, ...",
    )

    number_input(
        label="Montant (€)",
        key="input_estate_source_amount",
    )

    st.number_input(
        label="Plafond (€)",
        key="input_estate_source_limit",
        value=produit["plafond"],
        help="Le plafond concerne notamment les livrets d'épargne. Si cette source n'a pas de plafond, laissez le champ vide",
        step=500.0,
    )

    st.number_input(
        label="Rendement annuel (%)",
        key="input_estate_source_return",
        min_value=0.0,
        value=produit["rendement"] * 100,
        format="%.2f",
        step=1.0,
    )

    column_add, column_remove = st.columns(2)

    with column_add:
        if st.session_state["situation_configuration_mode"] == "add":
            if st.button(
                label="Ajouter",
                icon=":material/add:",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner(
                    show_time=True, text="Ajout de l'élément de patrimoine en cours..."
                ):
                    insert_patrimoine(id_produit=produit["id"])

        elif st.button(
            label="Modifier",
            icon=":material/edit:",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner(
                show_time=True, text="Ajout de l'élément de patrimoine en cours..."
            ):
                update_patrimoine()

    with column_remove:
        if st.session_state["situation_configuration_mode"] != "add":
            st.button(
                label="Supprimer",
                help="Retire cette source de la liste des sources de patrimoine",
                icon=":material/clear:",
                on_click=delete_patrimoine,
                use_container_width=True,
            )
