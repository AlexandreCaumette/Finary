from streamlit.delta_generator import DeltaGenerator
from data.cube import Cube
import data.constants as cst

import altair as alt
from components.metrics import render_metric_estate, render_metric_income

cube = Cube()

def render_tab_analyze(tab: DeltaGenerator):
    tab.header('Analyse et évolution du patrimoine')
    
    tab.subheader('Indicateurs clés du patrimoine actuel')
    
    metric_columns = tab.columns([1, 1, 1], border=True)
    
    render_metric_estate(parent=metric_columns[0],
                         years=0)
    
    metric_columns[1].metric(label='Nombre de sources de patrimoine',
               value=len(cube.get_estate_sources()))
    
    metric_columns[2].metric(label="Taux d'épargne actuel",
               value=f"{cube.compute_saving_rate():.2%}",
               help=f"Une explication détaillée du taux d'épargne est disponible dans l'onglet **{cst.TAB_ANALYSE}**.")
    
    chart_columns = tab.columns([2, 3, 2], border=True)
    
    chart_current_estate = (
        alt.Chart(cube.get_df_estate_sources())
        .mark_arc()
        .encode(
            theta='Montant à date',
            color='Label'
        )
    )
    
    chart_current_apport = (
        alt.Chart(cube.get_df_estate_sources())
        .mark_arc()
        .encode(
            theta='Apport annuel',
            color='Label'
        )
    )
    
    chart_columns[0].text("Répartition du patrimoine actuel par sources")
    chart_columns[0].altair_chart(chart_current_estate)
    
    chart_columns[1].text("Classement des sources par rendement annuel")
    chart_columns[1].bar_chart(data=cube.get_df_estate_sources(),
                               x='Label',
                               y='Rendement',
                               horizontal=True,
                               color='Label')
    
    chart_columns[2].text("Répartition des investissements par sources")
    chart_columns[2].altair_chart(chart_current_apport)
    
    tab.divider()
    
    tab.subheader('Evolution prévue du patrimoine')
    
    prevision_columns = tab.columns([2, 1, 2], border=True)
    
    years = prevision_columns[0].slider(label="Echéance de la projection en années",
               min_value=0,
               value=5,
               max_value=40,
               step=1,
               format='%d ans')
    
    render_metric_estate(parent=prevision_columns[1],
                         years=years)
    
    render_metric_income(parent=prevision_columns[2],
                         years=years)
    
    prevision_columns = tab.columns([1, 1], border=True)

    prevision_columns[0].text(f"Projection du patrimoine par source dans {years} ans")
    prevision_columns[0].area_chart(data=cube.get_estate_projection(years),
                   x="date",
                   x_label='Année',
                   y='estate_amount',
                   y_label='Montant du patrimoine (€)',
                   color='estate_source',
                   stack=True,
                   height=600)
    
    prevision_columns[1].text(f"Projection du revenu brut et net dans {years} ans")
    prevision_columns[1].area_chart(data=cube.compute_income_projection(years),
                   x="date",
                   x_label='Année',
                   y=["Montant annuel brut", "Montant annuel net", "Montant annuel net après impôt"],
                   y_label='Montant du revenu (€)',
                   stack=False,
                   height=600)
    
    tab.divider()
    
    expander = tab.expander('WORK IN PROGRESS')
    
    deposit_columns = expander.columns([1, 1], border=True)
    
    deposit_columns[0].area_chart(data=cube.compute_left_income(years),
                   x='date',
                   y=['Investissement annuel', "Revenu restant après investissement"],
                   stack=True)
    
    deposit_columns[1].line_chart(data=cube.compute_left_income(years),
                   x='date',
                   y="saving_rate",
                   y_label="Taux d'épargne")