from streamlit.delta_generator import DeltaGenerator
import data.constants as cst

def render_tab_home(tab: DeltaGenerator):
    tab.header('Bienvenue sur votre application de gestion de patrimoine !')
    
    tab.subheader("Qu'est-ce que c'est ?")
    
    tab.markdown(f"""
    L'application {cst.APP_NAME} a pour objectif de synthétiser et visualiser son patrimoine actuel, ainsi que de réaliser des prévisions
    sur l'évolution de son patrimoine.
    
    Il est ainsi possible de visualiser ses sources de patrimoine, ses investissements, leur évolution sur plusieurs années.
    
    Il est également possible de visualiser la répartition et la diversification de son épargne.
    
    Enfin, il est possible de projeter son revenu (salarial principalement) et de voir son évolution.
    """)
    
    tab.divider()
    
    tab.subheader("Comment ça marche ?")
    
    tab.markdown(f"""
    Dans {cst.APP_NAME}, il faut configurer ses sources de patrimoine : montant à date, rendement, plafond, apport annuel, ...
    
    Il faut également configurer ses sources de revenus, afin de faire les projections les plus fidèles possibles.
    
    Une fois ces deux informations configurées, l'application fait la synthèse à date de la situation, et calcule des projections grâce à des hypothèses sur les rendements annuels, les apports annuels, et les augmentations de salaire annuelles.
    """)
    
    tab.divider()
    
    tab.subheader("Qu'est-ce que je dois faire ?")
    
    tab.markdown(f"""
    Voici la marche à suivre pour utiliser {cst.APP_NAME} :
    
    1. Configurer ses sources de patrimoine et revenu
    - Il faut se rendre dans l'onglet **{cst.TAB_SOURCE}**.
    - Il faut suivre les indications pour ajouter manuellement ses sources de patrimoine, ainsi que ses sources de revenu.
    
    2. Prendre connaissance de son tableau de pilotage
    - Il faut se rendre dans l'onglet **{cst.TAB_PILOTAGE}**.
    - Il faut parcourir chaque visuel et indicateur, et prendre le temps de lire les notes visibles en survolant certains éléments.
    - Il faut jouer avec le nombre d'années pour les projections.
    
    3. Analyser tranquillement les détails de sa situation
    - Il faut se rendre dans l'onglet **'👨🏻‍🏫 Analyse'**.
    - Il faut prendre le temps de lire chaque panneau déroulant, pour prendre connaissance de chaque détail de sa situation financière.
    """)