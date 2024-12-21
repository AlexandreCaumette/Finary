import streamlit as st
from streamlit.delta_generator import DeltaGenerator

import json

from data.cube import Cube
import data.constants as cst

from components.forms.form_estate_source import estate_source_form
from components.forms.form_income_source import income_source_form

cube = Cube()

def estate_section(parent: DeltaGenerator):
    parent.divider()
      
    parent.subheader("Mes sources de patrimoine et d'investissement")
        
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
    parent.divider()
      
    parent.subheader("Mes sources de revenus")
    
    parent.dataframe(data=cube.get_df_income_sources(),
                  key='income_sources_dataframe',
                  width=900,
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
                      )
                  })
    
    parent.subheader('Ajouter une nouvelle source de revenu')
    
    income_source_form(parent)
    
def config_section(parent: DeltaGenerator):
    parent.divider()
    
    parent.markdown(f"""
    Je peux enregistrer mes sources de patrimoine et de revenus afin de pouvoir les réutiliser la prochaine fois, et ainsi
    ne pas les configurer à nouveau.
    
    Une fois mes sources configurées pour la première fois, je pourrai cliquer sur le bouton "Enregistrer mes sources", ce déclenchera l'export
    de mes sources dans un fichier au format .json : `personal_sources.json`.
     
    Lors de ma prochaine utilisation de {cst.APP_NAME}, je pourrai directement charger ce fichier de sauvegarde, et retrouver mes sources.
    """)
    
    parent.divider()
    
    def load_sources_file():
        cube.load_sources_file()
        parent.success('Mes sources ont bien été chargées !', icon='🍾')
    
    parent.file_uploader(label='Sélectionner le fichier de sauvegarde de mes sources',
                      type='json',
                      on_change=load_sources_file,
                      key='sources_file_uploader',
                      help=f"Un fichier .json issu de {cst.APP_NAME}")
    
    parent.divider()
    
    def save_sources():
        parent.success('Vos sources de patrimoine ont bien été enregistrées !', icon='🍾')
        
    parent.download_button(label='Enregistrer mes sources',
                           data=json.dumps(cube.read_state('sources')),
                           file_name='finary_sources.json',
                           on_click=save_sources,
                            help="Permet d'enregistrer dans un fichier .json les sources configurées et de les retrouver la prochaine fois.",
                           icon=':material/save:')

def render_tab_sources(tab: DeltaGenerator):
    tab.header('Configuration de vos sources de patrimoine et de revenus')
    
    config_expander = tab.expander(label='Chargement et sauvegarde de mes sources', icon='⚙️')
    
    config_section(config_expander)
    
    estate_expander = tab.expander(label='Mes sources de patrimoine', icon='🏘️')
    
    estate_section(estate_expander)
    
    income_expander = tab.expander(label='Mes sources de revenu', icon='💶')
    
    income_section(income_expander)