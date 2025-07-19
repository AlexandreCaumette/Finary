import streamlit as st
from typing import Literal
from stores import store_computed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def color(text: str, colour: Literal["red", "blue", "orange", "green"]) -> str:
    return f"**:{colour}[{text}]**"


mots_cles = {
    "BRUT": color("salaire brut", "red"),
    "NET": color("salaire net", "red"),
    "NETI": color("salaire net imposable", "red"),
    "NETAI": color("salaire net après impôt", "red"),
    "CS": color("contributions sociales", "green"),
    "ES": color("éléments de salaire", "blue"),
    "ISR": color("impôt sur le revenu", "orange"),
    "PS": color("prélèvement à la source", "orange"),
    "TPS": color("taux de prélèvement à la source", "orange"),
}


sujets_analyse = [
    # {"label": "Le taux d'épargne", "text": "taux_epargne.md"},
    {"label": "Le salaire net", "text": "salaire_net.md"},
    {"label": "Le salaire net imposable", "text": "salaire_net_imposable.md"},
    {"label": "Le salaire net après impôt", "text": "salaire_net_apres_impot.md"},
    {"label": "L'impôt sur le revenu", "text": "impot_sur_le_revenu.md"},
    {"label": "Le prélèvement à la source", "text": "prelevement_a_la_source.md"},
]

st.header("Explication des différents indicateurs")

input_column, button_column = st.columns([2, 1], vertical_alignment="bottom")

with input_column:
    searched_topic = st.text_input(
        label="Question ou sujet ou mots-clés",
        help="Ce champ permet de mettre en valeur les éléments d'analyse en lien avec votre recherche.",
        placeholder="Quel est mon taux d'épargne ?",
        key="input_search_analysis_topic",
    )


def reset_search_topic():
    st.session_state["input_search_analysis_topic"] = None


with button_column:
    st.button(
        label="Vider la saisie",
        type="primary",
        icon=":material/cancel:",
        on_click=reset_search_topic,
    )

st.divider()

if searched_topic is None or len(searched_topic) == 0:
    sujets_analyse_filtres = sujets_analyse

else:
    vectoriseur = TfidfVectorizer()

    sujets = [sujet["label"] for sujet in sujets_analyse]

    tfidf_matrix = vectoriseur.fit_transform(sujets + [searched_topic])

    similarites = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    sujets_analyse_filtres = []

    for index_sujet, similarite in enumerate(similarites[0]):
        if similarite > 0.5:
            sujets_analyse_filtres.append(sujets_analyse[index_sujet])

for expander_config in sujets_analyse_filtres:
    with st.expander(label=expander_config["label"]):
        with open(f"assets/texts/{expander_config['text']}", encoding="utf-8") as file:
            content = file.read()

            for key, value in mots_cles.items():
                content = content.replace(f"<{key}>", value)

            st.markdown(content)

expander_1 = st.expander("Le taux d'épargne")

expander_1.markdown(f"""
Le **:red[taux d'épargne]** est le ratio entre le :orange[revenu disponible chaque mois] (le salaire net après prélèvement des impôts),
et les :orange[montants épargnés chaque mois] (livrets, actions, cryptomonnaie, ...).

Il est possible de calculer son :orange[salaire net après impôt] sur le site https://www.salaire-brut-en-net.fr/.

Plus le **:red[taux d'épargne]** est important, plus une proportion forte du revenu est investi.

Mon :orange[revenu disponible chaque mois] est fixé à **:orange-background[{store_computed.calcul_revenu_mensuelle_actuel():.2f} €]**.

Le :orange[montant épargné chaque mois] est calculé en additionnant les apports annuels de toutes les sources et en le divisant par 12.
On obtient ainsi un :orange[montant épargné chaque mois] de **:orange-background[{store_computed.calcul_epargne_mensuelle_actuelle():.2f} €]**.

Le **:red[taux d'épargne]** est donc de **:red-background[{store_computed.calcul_taux_epargne_actuel():.2%}]**.

A titre de comparaison, le **:red[taux d'épargne]** moyen des français était de :
- **:red-background[{0.182:.2%}]** en 2024
- **:red-background[{0.175:.2%}]** en 2023

Voir https://www.insee.fr/fr/outil-interactif/5367857/details/10_ECC/11_ECO/11E_Figure5#:~:text=Lecture-,En%202024%2C%20le%20taux%20d'%C3%A9pargne%20des%20m%C3%A9nages%20est%20%C3%A9gal,financi%C3%A8re%20%C3%A0%209%2C0%20%25.&text=France%2C%20m%C3%A9nages%20y%20compris%20entrepreneurs%20individuels.,-Source&text=Insee%2C%20comptes%20nationaux%20%2D%20base%202020.,-%C3%80%20d%C3%A9couvrir
""")
