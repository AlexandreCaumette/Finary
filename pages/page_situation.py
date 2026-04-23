import streamlit as st
from loguru import logger

import data.constants as cst
from components.forms.form_estate_source import formulaire_patrimoine
from models.modele_patrimoine import Patrimoine


def vue_patrimoine():
    st.subheader("Mes sources de patrimoine et d'investissement")

    st.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de patrimoine créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)

    patrimoine: Patrimoine = st.session_state["patrimoine"]

    column_form, column_dataframe = st.columns([1, 2], border=True)

    with column_form:
        formulaire_patrimoine()

    with column_dataframe:
        if patrimoine.df_patrimoine.height > 0:
            st.dataframe(
                data=patrimoine.df_patrimoine,
                key="estate_sources_dataframe",
                width=900,
                selection_mode="single-row",
                # on_select=cube.on_select_estate_source,
                column_config={
                    "Montant à date": st.column_config.NumberColumn(format="%.2f €"),
                    "Apport annuel": st.column_config.NumberColumn(format="%.2f €"),
                    "Plafond": st.column_config.NumberColumn(format="%.2f €"),
                    "Rendement": st.column_config.NumberColumn(format="%.2f %%"),
                },
            )

        else:
            st.info(
                "Vous devez ajouter un premier élément de votre patrimoine.",
                icon=":material/info:",
            )


def vue_revenus():
    st.subheader("Mes sources de revenus")

    st.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de revenu créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)

    # st.dataframe(
    #     data=cube.get_df_income_sources(),
    #     key="income_sources_dataframe",
    #     width=1000,
    #     selection_mode="single-row",
    #     on_select=cube.on_select_income_source,
    #     column_config={
    #         "Montant annuel brut": st.column_config.NumberColumn(format="%.2f €"),
    #         "Montant annuel net": st.column_config.NumberColumn(format="%.2f €"),
    #         "Montant annuel net après impôt": st.column_config.NumberColumn(
    #             format="%.2f €"
    #         ),
    #         "Augmentation moyenne annuelle": st.column_config.NumberColumn(
    #             format="%.2f %%"
    #         ),
    #         "Cotisations sociales": None,
    #     },
    # )

    # st.subheader(
    #     f"{'Modifier une' if cube.is_income_source_selected() else 'Ajouter une nouvelle'} source de revenu"
    # )

    # income_source_form()


def main_situation():
    with st.expander("Configuration de vos sources de patrimoine et de revenus"):
        st.markdown("""
        Dans cet onglet, vous pouvez configurer vos sources de patrimoine et vos sources de revenu.

        Il n'est pas obligé et impératif de configurer toutes ses informations dès la première utilisation, il est possible de ne renseigner qu'une partie de ses sources
        pour pouvoir rapidement jeter un oeil aux onglets de "Mon tableau de bord" et "Analyse de ma situation", pour jouer avec les projections et comprendre le fonctionnement
        de l'application.
        """)

    if not st.session_state["is_user_logged"]:
        logger.debug(
            "L'utilisateur est redirigé vers la page login car il n'est pas connecté."
        )

        st.switch_page(page="pages/page_me_connecter.py")

    tab_patrimoine, tab_revenus = st.tabs(
        ["Sources de patrimoine 🏘️", "Sources de revenu 💶"]
    )

    if "situation_configuration_mode" not in st.session_state:
        st.session_state["situation_configuration_mode"] = "add"

    with tab_patrimoine:
        vue_patrimoine()

    with tab_revenus:
        vue_revenus()


if __name__ == "__main__":
    main_situation()
