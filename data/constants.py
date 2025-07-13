import polars as pl

APP_NAME = "**:orange[Finary] 🪙**"

PAGES_CONFIG = [
    {
        "label": "1. Accueil",
        "name": "home",
        "icon": "🏠",
        "visible": True,
    },
    {
        "label": "2. Ma situation",
        "name": "situation",
        "icon": "📝",
        "help": """
        Configurer ma situation financière (revenus, épargne, etc...) pour permettre les analyses et les projections.
        """,
        "visible": True,
    },
    {
        "label": "3. Mon tableau de pilotage",
        "name": "summary",
        "icon": "📊",
        "help": """
        (⚠️ Accessible uniquement lorsque sa situation financière est renseignée ⚠️)
        Avoir une vue synthétique de son patrimoine à date, et des perspectives d'évolution dans les années à venir.
        """,
        "visible": True,
    },
    {
        "label": "4. Analyse de ma situation",
        "name": "analysis",
        "icon": "👨🏻‍🏫",
        "help": """
        (⚠️ Accessible uniquement lorsque sa situation financière est renseignée ⚠️)
        Comprendre les détails de mon imposition, de la fiscalité, et des modélisations d'évolution de mon patrimoine.
        """,
        "visible": True,
    },
    {"label": "Connexion", "name": "login", "disabled": False, "visible": False},
    {
        "label": "Réinitialisation du mot de passe",
        "name": "reset_password",
        "visible": False,
    },
]

ESTATE_SOURCES_LIST = [
    "Livret d'épargne",
    "Cryptomonnaie",
    "Plan d'épargne",
    "Assurance vie",
    "Immobilier",
    "Compte courant",
]
INCOME_SOURCES_LIST = ["Salaire", "Cadeau", "Aides"]


def print_page_title(index_page: int):
    return f"**{PAGES_CONFIG[index_page]['label']}{PAGES_CONFIG[index_page]['icon']}**"


DF_COTISATIONS_SOCIALES = pl.DataFrame(
    data=[
        # ('Nom de la contribution', taux salarial)
        ("complementaire_sante", 1.22),
        ("securite_sociale_plafonnee", 6.90),
        ("securite_sociale_deplafonnee", 0.4),
        ("complementaire_tu1", 4.364),
        ("apec", 0.024),
        ("csg_crds", 2.9),
        ("csg", 6.8),
    ],
    schema={"Cotisations sociales": pl.String, "Taux": pl.Float32},
    orient="row",
)
