from streamlit.delta_generator import DeltaGenerator
import data.constants as cst

def render_tab_home(tab: DeltaGenerator):
    tab.header('Bienvenu sur votre application de gestion de patrimoine !')
    
    tab.subheader("Qu'est-ce que c'est ?")
    
    tab.markdown(f"""
    L'application {cst.APP_NAME} a pour objectif de synthétiser et visualiser son patrimoine actuel, ainsi que de réaliser des prévisions
    sur l'évolution de son patrimoine.
    
    On pourra ainsi visualiser ses sources de patrimoine, ses investissements, leur évolution sur plusieurs années, et comment son épargne est répartie/diversifiée.
    """)
    
    tab.divider()
    
    tab.subheader("Comment ça marche ?")
    
    tab.markdown(f"""
    Dans {cst.APP_NAME}, vous pourrez configurer vos sources de patrimoine : montant à date, rendement, plafond, apport annuel, ...
    
    Vous pourrez également configurer vos sources de revenus, afin de faire les projections les plus fidèles possibles.
    """)
    
    tab.divider()
    
    tab.subheader("Qu'est-ce que je dois faire ?")
    
    tab.markdown(f"""
    Vous aurez probablement besoin de votre dernière fiche de paie pour configurer votre principale source de revenu (votre salaire).
    """)