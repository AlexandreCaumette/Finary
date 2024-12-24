import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import polars as pl

import json

from data.cube import Cube
import data.constants as cst

from components.forms.form_estate_source import estate_source_form
from components.forms.form_income_source import income_source_form

cube = Cube()

def estate_section(parent: DeltaGenerator):
    parent.subheader("Mes sources de patrimoine et d'investissement")
    
    parent.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de patrimoine créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)
    
    parent.dataframe(data=cube.get_df_estate_sources(),
                  key='estate_sources_dataframe',
                  width=900,
                  selection_mode='single-row',
                  on_select=cube.on_select_estate_source,
                  column_config={
                      "Montant à date": st.column_config.NumberColumn(
                          format='%.2f €'
                      ),
                      "Apport annuel": st.column_config.NumberColumn(
                          format='%.2f €'
                      ),
                      "Plafond": st.column_config.NumberColumn(
                          format='%.2f €'
                      ),
                      "Rendement": st.column_config.NumberColumn(
                          format='%.2f %%'
                      )
                  })
    
    parent.divider()
    
    parent.subheader('Ajouter une nouvelle source de patrimoine')
    
    estate_source_form(parent)
    
def income_section(parent: DeltaGenerator):
    parent.subheader("Mes sources de revenus")
    
    parent.markdown(f"""
    Le visuel ci-dessous est un tableau récapitulatif de toutes les sources de revenu créées grâce au formulaire plus bas.
    Le tableau est ainsi vide lors de la première utilisation de {cst.APP_NAME}, et se met à jour automatiquement à chaque soumission du formulaire.                
    """)
        
    parent.dataframe(data=cube.get_df_income_sources(),
                  key='income_sources_dataframe',
                  width=1000,
                  selection_mode='single-row',
                  on_select=cube.on_select_income_source,
                  column_config={
                      "Montant annuel brut": st.column_config.NumberColumn(
                          format='%.2f €'
                      ),
                      "Montant annuel net": st.column_config.NumberColumn(
                          format='%.2f €'
                      ),
                      "Montant annuel net après impôt": st.column_config.NumberColumn(
                          format='%.2f €'
                      ),
                      "Augmentation moyenne annuelle": st.column_config.NumberColumn(
                          format='%.2f %%'
                      ),
                      "Cotisations sociales": None
                  })
    
    parent.subheader(f'{"Modifier une" if cube.is_income_source_selected() else "Ajouter une nouvelle"} source de revenu')
    
    income_source_form(parent)
    
def config_section(parent: DeltaGenerator):
    parent.markdown(f"""
    Dans cet onglet, vous pouvez configurer vos sources de patrimoine et vos sources de revenu.
    
    Pour n'avoir qu'à renseigner ses informations qu'une seule fois, il est possible de cliquer sur le bouton **"💾 Télécharger ses sources"**
    pour obtenir une sauvegarde de ces sources.
    
    Cette sauvegarde pourra être chargée directement lors de la prochaine utilisation, être modifiée, et être de nouveau téléchargée.
    
    Il n'est pas obligé et impératif de configurer toutes ses informations dès la première utilisation, il est possible de ne renseigner qu'une partie de ses sources
    pour pouvoir rapidement jeter un oeil aux onglets de **{cst.TAB_PILOTAGE}** et **{cst.TAB_ANALYSE}**, pour jouer avec les projections et comprendre le fonctionnement
    de l'application.
    """)
    
    def load_sources_file():
        cube.load_sources_file()
        parent.success('Mes sources ont bien été chargées !', icon='🍾')
        
    def save_sources():
        parent.success('Vos sources de patrimoine ont bien été enregistrées !', icon='🍾')
        
    columns = parent.columns([1, 1], vertical_alignment='center')
    
    columns[0].file_uploader(label='Sélectionner le fichier de sauvegarde de ses sources',
                      type='json',
                      on_change=load_sources_file,
                      key='sources_file_uploader',
                      help=f"Un fichier `personal_sources_<...>.json` téléchargé depuis {cst.APP_NAME}")
        
    columns[1].download_button(label='Télécharger ses sources',
                           data=json.dumps(cube.read_state('sources')),
                           file_name='finary_sources.json',
                           on_click=save_sources,
                            help="Permet d'enregistrer dans un fichier `personal_sources_<...>.json` les sources configurées et de les retrouver la prochaine fois.",
                           icon='💾')

def render_tab_sources(tab: DeltaGenerator):
    tab.header('Configuration de vos sources de patrimoine et de revenus')
    
    config_section(tab)
    
    estate_expander = tab.expander(label='Sources de patrimoine', icon='🏘️')
    
    estate_section(estate_expander)
    
    income_expander = tab.expander(label='Sources de revenu', icon='💶')
    
    income_section(income_expander)