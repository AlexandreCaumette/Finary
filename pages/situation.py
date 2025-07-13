import streamlit as st
from st_supabase_connection import SupabaseConnection
import polars as pl

import data.constants as cst

from components.forms.form_patrimoine import render_form_patrimoine
from components.forms.form_revenu import render_form_revenu
from components.dataframes.dataframe_patrimoine import render_dataframe_patrimoine
from components.dataframes.dataframe_revenu import render_dataframe_revenu


if not st.session_state["is_user_logged"]:
    st.warning("Aucun utilisateur n'a été trouvé, veuillez vous connecter.")
    st.switch_page("pages/login.py")

conn = st.connection("supabase", type=SupabaseConnection)

st.header("Configuration de vos sources de patrimoine et de revenus")

st.markdown(f"""
Dans cet onglet, vous pouvez configurer vos sources de patrimoine et vos sources de revenu.

Il n'est pas obligé et impératif de configurer toutes ses informations dès la première utilisation, il est possible de ne renseigner qu'une partie de ses sources
pour pouvoir rapidement jeter un oeil aux onglets de "{cst.print_page_title(2)}" et "{cst.print_page_title(3)}", pour jouer avec les projections et comprendre le fonctionnement
de l'application.
""")

st.divider()

tab_estate, tab_income = st.tabs(["Sources de patrimoine 🏘️", "Sources de revenu 💶"])

if "situation_configuration_mode" not in st.session_state:
    st.session_state["situation_configuration_mode"] = "add"

with tab_estate:
    st.subheader("Mes sources de patrimoine et d'investissement")

    st.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de patrimoine créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)

    with st.spinner("Chargement des données de patrimoine...", show_time=True):
        response_patrimoine = (
            conn.table("PATRIMOINE")
            .select(
                "id_patrimoine",
                "type, label, amount, deposit, limit, return, date_ouverture_patrimoine",
            )
            .eq("id_user", st.session_state["user_data"].id)
            .execute()
        )

    dataframe = pl.from_records(response_patrimoine.data)
    st.session_state["df_patrimoine"] = dataframe

    column_form, column_dataframe = st.columns([1, 2])

    with column_dataframe:
        if dataframe.height > 0:
            render_dataframe_patrimoine(dataframe=dataframe)

        else:
            st.text("Vous pouvez ajouter une première source de patrimoine")

    with column_form:
        render_form_patrimoine()

with tab_income:
    st.subheader("Mes sources de revenus")

    st.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de revenu créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)

    with st.spinner("Chargement des données de revenus...", show_time=True):
        response_revenu = (
            conn.table("REVENUS")
            .select(
                "id_revenu, type_revenu, label_revenu, montant_revenu, pourcentage_augmentation"
            )
            .eq("id_user", st.session_state["user_data"].id)
            .execute()
        )

    dataframe = pl.from_records(response_revenu.data)
    st.session_state["df_revenu"] = dataframe

    column_form, column_dataframe = st.columns([1, 2])

    with column_dataframe:
        if dataframe.height > 0:
            render_dataframe_revenu(dataframe=dataframe)

        else:
            st.text("Vous pouvez ajouter une première source de revenu")

    with column_form:
        render_form_revenu()
