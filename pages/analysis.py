import streamlit as st
from data.cube import Cube
from typing import Literal

cube = Cube()


def color(text: str, colour: Literal["red", "blue", "orange", "green"]) -> str:
    return f"**:{colour}[{text}]**"


BRUT = color("salaire brut", "red")
NET = color("salaire net", "red")
NETI = color("salaire net imposable", "red")
NETAI = color("salaire net après impôt", "red")
CS = color("contributions sociales", "green")
ES = color("éléments de salaire", "blue")
ISR = color("impôt sur le revenu", "orange")
PS = color("prélèvement à la source", "orange")
TPS = color("taux de prélèvement à la source", "orange")


st.header("Explication des différents indicateurs")

expander_1 = st.expander("Le taux d'épargne")

expander_1.markdown(f"""
Le **:red[taux d'épargne]** est le ratio entre le :orange[revenu disponible chaque mois] (le salaire net après prélèvement des impôts),
et les :orange[montants épargnés chaque mois] (livrets, actions, cryptomonnaie, ...).

Il est possible de calculer son :orange[salaire net après impôt] sur le site https://www.salaire-brut-en-net.fr/.

Plus le **:red[taux d'épargne]** est important, plus une proportion forte du revenu est investit.

Le :orange[revenu disponible chaque mois] est fixé à **:orange-background[{cube.compute_monthly_available_income():.2f} €]**.

Le :orange[montant épargné chaque mois] est calculé en additionnant les apports annuels de toutes les sources et en le divisant par 12.
On obtient ainsi un :orange[montant épargné chaque mois] de **:orange-background[{cube.compute_monthly_saved_amount():.2f} €]**.

Le **:red[taux d'épargne]** est donc de **:red-background[{cube.compute_saving_rate():.2%}]**.

A titre de comparaison, le **:red[taux d'épargne]** moyen des français était de **:red-background[{0.175:.2%}]** en 2023.
""")

expander_2 = st.expander("Le salaire net")

expander_2.markdown(f"""
Le {NET} est le revenu restant après la soustraction des {CS} et l'ajout des {ES} au {BRUT}.

Les {CS} sont listées sur sa fiche de paie, avec un taux appliqué à une base.

La base est en générale le {BRUT}, sauf dans le cas de la CSG et de la CRDS qui ont une assiette plus large (la base inclut les primes et autres compléments de salaire).

Les {ES} sont tous les compléments de salaire versés par l'employeur :
- indemnités de télétravail
- indemnités de transport
- tickets restaurants
- ...

Le {NET} n'est pas la base sur laquelle le montant d'impôt est calculé, car il faut lui ajouter la part non imposable de la CSG, cf. le {NETI}. 
""")

expander_3 = st.expander("Le salaire net imposable")

expander_3.markdown(f"""
Le {NETI} est le revenu servant de base au calcul de l'{ISR}.

Il est calculé en retirant du {BRUT} les {CS} imposables (tout sauf la part non imposable de la CSG) et en ajoutant les {ES}.
""")

expander_4 = st.expander("Le salaire net après impôt")

expander_4.markdown(f"""
Le {NETAI} est le revenu restant après avoir soustrait au {NET} l'{ISR}.

L'{ISR} est calculé sur la base du {NETI}, avec un système de tranches, cf. l'{ISR}.

En revanche, pour le prélèvement à la source, le calcul de l'{ISR} se fait avec un unique taux d'imposition, et une correction annuelle est effectuée après la période la déclaration d'impôt, cf. {PS}.
""")

expander_5 = st.expander("L'impôt sur le revenu")

expander_5.markdown("""""")

expander_4 = st.expander("Le prélèvement à la source")

expander_4.markdown(f"""
Le {PS} est un prélèvement mensualisé de l'{ISR}, calculé à partir d'un unique taux d'imposition.

On multiplie le taux d'imposition par le {NETI} pour obtenir le montant d'impôt prélevé.

A la suite de la déclaration d'impôt, le montant annuel d'{ISR} est comparé à la somme des {PS} effectués pendant l'année, ce qui conduit à 3 scénarios :
- Si la différence est positive, alors les {PS} n'ont pas suffit à m'acquitter de l'{ISR}, et donc je serai prélevé de la différence (la cause : le {TPS} n'était pas assez élevé)
- Si la différence est négative, alors les {PS} ont dépassé l'{ISR} dû, et donc je serai remboursé de la différence (la cause : le {TPS} était trop élevé)
- Si la différence est nulle, alors les {PS} m'on acquitté exactement du montant d'{ISR} dû
""")
