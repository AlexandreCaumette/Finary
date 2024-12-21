#################################
###   Import des librairies   ###
#################################


import streamlit as st
from components.tabs.tab_home import render_tab_home
from components.tabs.tab_sources import render_tab_sources
from components.tabs.tab_analyze import render_tab_analyze
from components.tabs.tab_explanation import render_tab_explanation
from data.cube import Cube

cube = Cube()


####################################
###   Configuration de la page   ###
####################################


st.set_page_config(page_title='Finary',
                   page_icon='🪙',
                   layout='wide')

st.title('Application de gestion de patrimoine')

tab_home, tab_data, tab_analyze, tab_explanation = st.tabs([
    '🏠 Accueil',
    '💾 Données',
    '📊 Pilotage',
    '👨🏻‍🏫 Analyse'
])

render_tab_home(tab_home)
render_tab_sources(tab_data)

if cube.is_dataframe_initialized():
    render_tab_analyze(tab_analyze)
    render_tab_explanation(tab_explanation)