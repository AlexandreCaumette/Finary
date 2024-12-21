from streamlit.delta_generator import DeltaGenerator

def number_input(parent: DeltaGenerator, label: str, key: str, value: float = 0., help: str = None):
    parent.number_input(label=label,
                        key=key,
                        min_value=0.,
                        value=value,
                        format="%.2f",
                        step=500.,
                        help=help)