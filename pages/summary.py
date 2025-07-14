import streamlit as st
import altair as alt
import stores.store_computed as store_computed

st.header("Analyse et évolution du patrimoine")

st.subheader("Indicateurs clés du patrimoine actuel")

# --======================================================
# --= Métriques de l'état actuel de son épargne
# --======================================================

metric_columns = st.columns([1, 1, 1], border=True)

with metric_columns[0]:
    st.metric(
        label="Patrimoine actuel",
        value=f"{store_computed.calcul_patrimoine_actuel():,.2f} €",
        help="""
        Somme du montant à date de tous les produits d'épargne renseignés.
        """,
    )


with metric_columns[1]:
    st.metric(
        label="Nombre de sources de patrimoine",
        value=f"{store_computed.calcul_nombre_sources_patrimoine()} produits",
        help="""
        Nombre de produits d'épargne renseignés.
        """,
    )


with metric_columns[2]:
    st.metric(
        label="Taux d'épargne actuel",
        value=f"{store_computed.calcul_taux_epargne_actuel():.2%}",
        help="Une explication détaillée du taux d'épargne est disponible dans l'onglet d'analyse.",
    )

# --======================================================
# --= Graphiques de répartition de son épargne actuelle
# --======================================================

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

# --======================================================
# --= Projection dans les années à venir
# --======================================================

st.subheader("Evolution prévue du patrimoine")

prevision_columns = st.columns([2, 1, 1], border=True)

with prevision_columns[0]:
    years = st.slider(
        label="Echéance de la projection en années",
        min_value=0,
        value=5,
        max_value=40,
        step=1,
        format="%d ans",
    )

with prevision_columns[1]:
    st.metric(
        label=f"Patrimoine projeté dans {years}",
        value=f"{store_computed.calcul_patrimoine_projete(years):,.2f} €",
        help="""
        Somme du montant à date de tous les produits d'épargne renseignés.
        """,
    )

with prevision_columns[2]:
    st.metric(
        label=f"Revenu projeté dans {years}",
        value=f"{store_computed.calcul_revenu_projete(years):,.2f} €",
        help="""
        Somme du montant à date de tous les produits d'épargne renseignés.
        """,
    )

prevision_columns = st.columns([1, 1], border=True)

prevision_columns[0].text(f"Projection du patrimoine par source dans {years} ans")
prevision_columns[0].area_chart(
    data=store_computed.calcul_df_patrimoine_projete(years),
    x="date",
    x_label="Année",
    y="amount",
    y_label="Montant du patrimoine (€)",
    color="label",
    stack=True,
    height=600,
)

"""
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
"""
st.divider()
