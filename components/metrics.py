from streamlit.delta_generator import DeltaGenerator
from data.cube import Cube

cube = Cube()

def money_metric(parent: DeltaGenerator, label: str = '', amount: float = 0):
    parent.metric(label=label, value=f"{amount:,.2f} €")

def render_metric_estate(parent: DeltaGenerator, years: int = 0):
    money_metric(parent=parent,
                 label=f"Patrimoine dans {years} ans" if years != 0 else 'Patrimoine actuel',
                 amount=cube.compute_total_estate(years=years))
    
def render_metric_income(parent: DeltaGenerator, years: int = 0):
    income = cube.compute_total_income(years=years)
    
    columns = parent.columns([1, 1, 1])
    
    money_metric(parent=columns[0],
                 label=f"Revenu brut dans {years} ans" if years != 0 else 'Revenu brut actuel',
                 amount=income[0])
    
    money_metric(parent=columns[1],
                 label=f"Revenu net dans {years} ans" if years != 0 else 'Revenu net actuel',
                 amount=income[1])
    
    money_metric(parent=columns[2],
                 label=f"Revenu net après impôt dans {years} ans" if years != 0 else 'Revenu après impôt actuel',
                 amount=income[2])