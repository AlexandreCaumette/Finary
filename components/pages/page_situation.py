import streamlit as st
from st_supabase_connection import SupabaseConnection
import json
import polars as pl

from data.cube import Cube
import data.module_state_management as state
import data.constants as cst

from components.forms.form_estate_source import estate_source_form
from components.forms.form_income_source import income_source_form

from datetime import datetime

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
        .eq("id_user", st.session_state["user_data"]["id"])
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


def page_situation():
    st.header("Configuration de vos sources de patrimoine et de revenus")

    st.markdown(f"""
    Dans cet onglet, vous pouvez configurer vos sources de patrimoine et vos sources de revenu.
    
    Pour n'avoir qu'à renseigner ses informations qu'une seule fois, il est possible de cliquer sur le bouton **"💾 Télécharger ses sources"**
    pour obtenir une sauvegarde de ces sources.
    
    Cette sauvegarde pourra être chargée directement lors de la prochaine utilisation, être modifiée, et être de nouveau téléchargée.
    
    Il n'est pas obligé et impératif de configurer toutes ses informations dès la première utilisation, il est possible de ne renseigner qu'une partie de ses sources
    pour pouvoir rapidement jeter un oeil aux onglets de "{cst.print_page_title(2)}" et "{cst.print_page_title(3)}", pour jouer avec les projections et comprendre le fonctionnement
    de l'application.
    """)

    def load_sources_file():
        cube.load_sources_file()
        st.success("Mes sources ont bien été chargées !", icon="🍾")

    def save_sources():
        st.success("Vos sources de patrimoine ont bien été enregistrées !", icon="🍾")

    columns = st.columns([1, 1], vertical_alignment="center")

    columns[0].file_uploader(
        label="Sélectionner le fichier de sauvegarde de ses sources",
        type="json",
        on_change=load_sources_file,
        key="sources_file_uploader",
        help=f"Un fichier `personal_sources_<...>.json` téléchargé depuis {cst.APP_NAME}",
    )

    file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_configuration_finary.json"

    columns[1].download_button(
        label="Télécharger ses sources",
        data=json.dumps(state.read_state("sources")),
        file_name=file_name,
        on_click=save_sources,
        help="Permet d'enregistrer dans un fichier `personal_sources_<...>.json` les sources configurées et de les retrouver la prochaine fois.",
        icon="💾",
    )

    st.divider()

    tab_estate, tab_income = st.tabs(
        ["Sources de patrimoine 🏘️", "Sources de revenu 💶"]
    )

    if "situation_configuration_mode" not in st.session_state:
        st.session_state["situation_configuration_mode"] = "add"

    with tab_estate:
        estate_section()

    with tab_income:
        income_section()
