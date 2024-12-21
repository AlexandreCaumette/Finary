from streamlit.delta_generator import DeltaGenerator

from data.cube import Cube
import data.constants as cst

from components.forms.form_inputs import number_input

cube = Cube()

def income_source_form(parent: DeltaGenerator):
    parent.selectbox(label='Sélectionner un type de source de revenu',
                options=cst.INCOME_SOURCES_LIST,
                key='income_source_type_selection',
                index=None)
    
    parent.text_input('Le label de la source', key='input_income_source_label')
    
    number_input(parent=parent,
                 label='Salaire annuel brut',
                 key='input_annual_gross_salary')
    
    number_input(parent=parent,
                 label='Salaire annuel net',
                 key='input_annual_net_salary')
    
    number_input(parent=parent,
                 label='Salaire annuel net après impôt',
                 key='input_annual_net_salary_after_tax')
    
    number_input(parent=parent,
                 label='Augmentation moyenne annuelle (en %)',
                 key='input_average_annual_increase')
        
    def add_income_source():
        source = {
            'Catégorie': cube.read_state('income_source_type_selection'),
            'Label': cube.read_state('input_income_source_label'),
            'Montant annuel brut': cube.read_state('input_annual_gross_salary'),
            'Montant annuel net': cube.read_state('input_annual_net_salary'),
            'Montant annuel net après impôt': cube.read_state('input_annual_net_salary_after_tax'),
            'Augmentation moyenne annuelle': cube.read_state('input_average_annual_increase')
        }
        
        cube.add_source(type='income', source=source)
        
        parent.success("La nouvelle source de revenu a bien été ajoutée !", icon="💸")
        
    columns = parent.columns([1, 1, 7])
        
    columns[0].button(label='Ajouter la source',
            help="Permet de créer et d'ajouter une source de revenu à l'étude",
            icon=':material/add:',
            on_click=add_income_source)
    
    def delete_income_source():
        cube.delete_income_source()
        parent.success("La source de revenu a bien été supprimée")
    
    if cube.read_state('index_income_source_selected') is not None:
        columns[1].button(label='Supprimer la source',
                help="Retire cette source de la liste des sources de revenu",
                icon=':material/clear:',
                on_click=delete_income_source)