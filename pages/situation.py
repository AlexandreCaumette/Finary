import streamlit as st
from st_supabase_connection import SupabaseConnection
import polars as pl

from data.cube import Cube
import data.constants as cst

from components.forms.form_estate_source import estate_source_form
from components.forms.form_income_source import income_source_form

cube = Cube()


def estate_section():
    st.subheader("Mes sources de patrimoine et d'investissement")

    st.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de patrimoine créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)

    conn = st.connection("supabase", type=SupabaseConnection)

    response = (
        conn.table("PATRIMOINE")
        .select("*")
        .eq("id_user", st.session_state["user_data"].id)
        .execute()
    )

    dataframe = pl.from_records(response.data)

    column_form, column_dataframe = st.columns([1, 2])

    with column_form:
        estate_source_form()

    with column_dataframe:
        if dataframe.height > 0:
            st.dataframe(
                data=dataframe,
                key="estate_sources_dataframe",
                width=900,
                selection_mode="single-row",
                on_select=cube.on_select_estate_source,
                column_config={
                    "Montant à date": st.column_config.NumberColumn(format="%.2f €"),
                    "Apport annuel": st.column_config.NumberColumn(format="%.2f €"),
                    "Plafond": st.column_config.NumberColumn(format="%.2f €"),
                    "Rendement": st.column_config.NumberColumn(format="%.2f %%"),
                },
            )
        else:
            st.text("Vous pouvez ajouter une première source de patrimoine")


def income_section():
    st.subheader("Mes sources de revenus")

    st.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de revenu créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)

    st.dataframe(
        data=cube.get_df_income_sources(),
        key="income_sources_dataframe",
        width=1000,
        selection_mode="single-row",
        on_select=cube.on_select_income_source,
        column_config={
            "Montant annuel brut": st.column_config.NumberColumn(format="%.2f €"),
            "Montant annuel net": st.column_config.NumberColumn(format="%.2f €"),
            "Montant annuel net après impôt": st.column_config.NumberColumn(
                format="%.2f €"
            ),
            "Augmentation moyenne annuelle": st.column_config.NumberColumn(
                format="%.2f %%"
            ),
            "Cotisations sociales": None,
        },
    )

    st.subheader(
        f"{'Modifier une' if cube.is_income_source_selected() else 'Ajouter une nouvelle'} source de revenu"
    )

    income_source_form()


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
    estate_section()

with tab_income:
    income_section()
