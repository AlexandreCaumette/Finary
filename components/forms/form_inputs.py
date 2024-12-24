from streamlit.delta_generator import DeltaGenerator
from data.cube import Cube

cube = Cube()

def number_input(parent: DeltaGenerator, label: str, key: str, value: float = 0., help: str = None):
    parent.number_input(label=label,
                        key=key,
                        min_value=0.,
                        value=value,
                        format="%.2f",
                        step=500.,
                        help=help)
    
def patch_button(parent: DeltaGenerator, on_click, key: str):
    if cube.read_state(key) is not None:
        parent.button(label='Modifier la source',
                icon=':material/edit:',
                key=f'{key}_add_button',
                type='primary',
                on_click=on_click)
    else:
        parent.button(label='Ajouter la source',
                help="Permet de créer et d'ajouter une source à l'étude",
                icon=':material/add:',
                type='primary',
                key=f'{key}_edit_button',
                on_click=on_click)