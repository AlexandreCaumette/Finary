import streamlit as st

import stores.store_patrimoine as store_patrimoine
import data.constants as cst

from components.forms.form_inputs import number_input


def render_form_patrimoine():
    with st.form(
        key="estate_sources_form",
        clear_on_submit=True,
        width="content",
        enter_to_submit=False,
    ):
        st.subheader(body="Formulaire d'édition de patrimoine")

        st.selectbox(
            label="Type de patrimoine",
            placeholder=", ".join(cst.ESTATE_SOURCES_LIST[:2]),
            options=cst.ESTATE_SOURCES_LIST,
            key="input_estate_source_type",
            index=None,
        )

        st.text_input(
            "Label",
            key="input_estate_source_label",
            placeholder="PEA, SCPI, Bitcoin, ...",
            value=None,
        )

        number_input(
            label="Montant (€)",
            key="input_estate_source_amount",
        )

        number_input(
            label="Apport annuel (€)",
            help="L'argent que vous apportez à ce placement chaque année",
            key="input_estate_source_deposit",
        )

        number_input(
            label="Plafond (€)",
            key="input_estate_source_limit",
            help="Le plafond concerne notamment les livrets d'épargne. Si cette source n'a pas de plafond, laissez le champ vide",
        )

        number_input(
            label="Rendement annuel (%)",
            key="input_estate_source_return",
        )

        st.date_input(
            label="Date d'ouverture du produit d'épargne",
            format="DD/MM/YYYY",
            key="input_date_ouverture_patrimoine",
            help="La date d'ouverture est utilisée pour calculer la durée d'existence du produit, et ainsi déterminer la fiscalité à appliquer.",
        )

        column_add, column_remove = st.columns(2)

        with column_add:
            st.form_submit_button(
                label="Ajouter"
                if st.session_state["situation_configuration_mode"] == "add"
                else "Modifier",
                on_click=store_patrimoine.insert_patrimoine
                if st.session_state["situation_configuration_mode"] == "add"
                else store_patrimoine.update_patrimoine,
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
                    help="Retire cette source de la liste des sources de patrimoine",
                    icon=":material/clear:",
                    on_click=store_patrimoine.delete_patrimoine,
                    use_container_width=True,
                )
