APP_NAME = "**:orange[Finary] 🪙**"

PAGES_CONFIG = [
    {
        "file": "page_home.py",
        "label": "1. Accueil",
        "name": "home",
        "icon": "🏠",
        "disabled": False,
    },
    {
        "file": "page_situation.py",
        "label": "2. Ma situation",
        "name": "situation",
        "icon": "📝",
        "disabled": False,
        "help": """
        Configurer ma situation financière (revenus, épargne, etc...) pour permettre les analyses et les projections.
        """,
    },
    {
        "file": "page_summary.py",
        "label": "3. Mon tableau de pilotage",
        "name": "summary",
        "icon": "📊",
        "disabled": True,
        "help": """
        (⚠️ Accessible uniquement lorsque sa situation financière est renseignée ⚠️)
        Avoir une vue synthétique de son patrimoine à date, et des perspectives d'évolution dans les années à venir.
        """,
    },
    {
        "file": "page_analysis.py",
        "label": "4. Analyse de ma situation",
        "name": "analysis",
        "icon": "👨🏻‍🏫",
        "disabled": True,
        "help": """
        (⚠️ Accessible uniquement lorsque sa situation financière est renseignée ⚠️)
        Comprendre les détails de mon imposition, de la fiscalité, et des modélisations d'évolution de mon patrimoine.
        """,
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
