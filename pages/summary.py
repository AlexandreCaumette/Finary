import streamlit as st
import polars as pl
import altair as alt
from components.metrics import render_metric_estate, render_metric_income

st.header("Analyse et évolution du patrimoine")

st.subheader("Indicateurs clés du patrimoine actuel")

metric_columns = st.columns([1, 1, 1], border=True)

patrimoine_actuel = st.session_state["df_patrimoine"].select(pl.sum("amount")).item()

with metric_columns[0]:
    st.metric(
        label="Patrimoine actuel",
        value=f"{patrimoine_actuel:,.2f} €",
        help="""
        Somme du montant à date de tous les produits d'épargne renseignés.
        """,
    )

nombre_sources_patrimoine = (
    st.session_state["df_patrimoine"].select(pl.count("id_patrimoine")).item()
)

with metric_columns[1]:
    st.metric(
        label="Nombre de sources de patrimoine",
        value=f"{nombre_sources_patrimoine} produits",
        help="""
        Nombre de produits d'épargne renseignés.
        """,
    )

"""
with metric_columns[2]:
    st.metric(
        label="Taux d'épargne actuel",
        value=f"{cube.compute_saving_rate():.2%}",
        help=f"Une explication détaillée du taux d'épargne est disponible dans l'onglet **{cst.st_ANALYSE}**.",
    )
"""

chart_columns = st.columns([2, 3, 2], border=True)

chart_current_estate = (
    alt.Chart(st.session_state["df_patrimoine"])
    .mark_arc()
    .encode(theta="amount", color="label")
)

chart_current_apport = (
    alt.Chart(st.session_state["df_patrimoine"])
    .mark_arc()
    .encode(theta="deposit", color="label")
)

chart_columns[0].text("Répartition du patrimoine actuel par sources")
chart_columns[0].altair_chart(chart_current_estate)

chart_columns[1].text("Classement des sources par rendement annuel")
chart_columns[1].bar_chart(
    data=st.session_state["df_patrimoine"],
    x="label",
    y="return",
    horizontal=True,
    color="label",
)

chart_columns[2].text("Répartition des investissements par sources")
chart_columns[2].altair_chart(chart_current_apport)

st.divider()

st.subheader("Evolution prévue du patrimoine")

prevision_columns = st.columns([2, 1, 2], border=True)

years = prevision_columns[0].slider(
    label="Echéance de la projection en années",
    min_value=0,
    value=5,
    max_value=40,
    step=1,
    format="%d ans",
)

render_metric_estate(parent=prevision_columns[1], years=years)

render_metric_income(parent=prevision_columns[2], years=years)

prevision_columns = st.columns([1, 1], border=True)

prevision_columns[0].text(f"Projection du patrimoine par source dans {years} ans")
prevision_columns[0].area_chart(
    data=cube.get_estate_projection(years),
    x="date",
    x_label="Année",
    y="estate_amount",
    y_label="Montant du patrimoine (€)",
    color="estate_source",
    stack=True,
    height=600,
)

prevision_columns[1].text(f"Projection du revenu brut et net dans {years} ans")
prevision_columns[1].area_chart(
    data=cube.compute_income_projection(years),
    x="date",
    x_label="Année",
    y=["Montant annuel brut", "Montant annuel net", "Montant annuel net après impôt"],
    y_label="Montant du revenu (€)",
    stack=False,
    height=600,
)

st.divider()

expander = st.expander("WORK IN PROGRESS")

deposit_columns = expander.columns([1, 1], border=True)

deposit_columns[0].area_chart(
    data=cube.compute_left_income(years),
    x="date",
    y=["Investissement annuel", "Revenu restant après investissement"],
    stack=True,
)

deposit_columns[1].line_chart(
    data=cube.compute_left_income(years),
    x="date",
    y="saving_rate",
    y_label="Taux d'épargne",
)
