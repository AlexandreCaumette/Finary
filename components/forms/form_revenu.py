import streamlit as st

import data.constants as cst

import stores.store_revenu as store_revenu


def render_form_revenu():
    with st.form(
        key="income_sources_form",
        clear_on_submit=True,
        width="content",
        enter_to_submit=False,
    ):
        st.subheader(body="Formulaire d'édition de revenu")

        st.selectbox(
            label="Sélectionner un type de source de revenu",
            options=cst.INCOME_SOURCES_LIST,
            key="input_type_revenu",
            placeholder=", ".join(cst.INCOME_SOURCES_LIST[:2]),
            index=None,
        )

        if "toggle_cotisations_sociales" not in st.session_state:
            st.session_state["toggle_cotisations_sociales"] = False

        if st.session_state["input_type_revenu"] == "Salaire":
            st.toggle(
                label="Je connais mes taux de cotisation sociale",
                key="toggle_cotisations_sociales",
                value=False,
            )

            columns = st.columns([1, 1], border=True)

        else:
            columns = st.columns([1])

        with columns[0]:
            st.text_input(
                label="Le label de la source",
                key="input_label_revenu",
                placeholder="Mon employeur, Héritage, ...",
                help="""
                Le libellé de la source de revenu.
                """,
            )

            st.number_input(
                label="Revenu annuel disponible",
                key="input_montant_revenu",
                min_value=0.0,
                step=500.0,
                help="""
                Le montant annuel de la source de revenu, disponible après les prélévements obligatoires.
                \nExemple :
                \nPour un salaire, il s'agit du revenu annuel net après impôt.
                """,
            )

            st.number_input(
                label="Augmentation annuelle (en %)",
                key="input_pourcentage_augmentation",
                min_value=0.0,
                format="%.2f",
                step=0.5,
                help="""
                Pourcentage d'augmentation annuel moyen à utiliser pour les projections.
                """,
            )

        if st.session_state["toggle_cotisations_sociales"]:
            with columns[1]:
                st.text(
                    "La liste des contributions sociales mentionnées sur votre fichie de paie."
                )

                st.data_editor(
                    data=cst.DF_COTISATIONS_SOCIALES,
                    num_rows="dynamic",
                    column_config={
                        "Taux": st.column_config.NumberColumn(
                            help="Le taux de cotisation salariale en pourcentage.",
                            min_value=0.0,
                            step=0.5,
                            format="%.2f %%",
                        )
                    },
                    width=600,
                    key="input_social_contributions",
                )

        column_add, column_remove = st.columns(2)

        with column_add:
            st.form_submit_button(
                label="Ajouter"
                if st.session_state["situation_configuration_mode"] == "add"
                else "Modifier",
                on_click=store_revenu.insert_revenu
                if st.session_state["situation_configuration_mode"] == "add"
                else store_revenu.update_revenu,
                icon=":material/add:"
                if st.session_state["situation_configuration_mode"] == "add"
                else ":material/edit:",
                type="primary",
                use_container_width=True,
            )

        with column_remove:
            if st.session_state["situation_configuration_mode"] != "add":
                st.form_submit_button(
                    label="Supprimer",
                    help="Retire cette source de la liste des sources de revenu",
                    icon=":material/clear:",
                    on_click=store_revenu.delete_revenu,
                    use_container_width=True,
                )
