from streamlit.delta_generator import DeltaGenerator

from data.cube import Cube
import data.constants as cst

from components.forms.form_inputs import number_input

cube = Cube() 

def estate_source_form(parent: DeltaGenerator):
    parent.selectbox(label='Sélectionner un type de source de patrimoine',
                options=cst.FORM_NAMES,
                key='input_estate_source_type',
                index=None)
    
    parent.text_input('Le label de la source',
                      key='input_estate_source_label')
    
    number_input(parent=parent,
                 label="Le montant de cette source à date",
                 key="input_estate_source_amount")
    
    number_input(parent=parent,
                 label="L'apport annuel apporté à cette source",
                 key="input_estate_source_deposit")
    
    number_input(parent=parent,
                label="Le plafond de cette source",
                key="input_estate_source_limit",
                help="Le plafond concerne notamment les livrets d'épargne. Si cette source n'a pas de plafond, laissez le champ vide")
        
    number_input(parent=parent,
                 label="Le rendement annuel de cette source (en pourcentage)",
                 key="input_estate_source_return")
        
    def patch_estate_source():
        source = {
            'Catégorie': cube.read_state('input_estate_source_type'),
            'Label': cube.read_state('input_estate_source_label'),
            'Montant à date': cube.read_state('input_estate_source_amount'),
            'Apport annuel': cube.read_state('input_estate_source_deposit'),
            'Plafond': cube.read_state('input_estate_source_limit'),
            'Rendement': cube.read_state('input_estate_source_return')
        }
        
        cube.patch_source(type='estate', source=source)
        
        parent.success("La nouvelle source de patrimoine a bien été ajoutée !", icon="💸")
        
    columns = parent.columns([1, 1, 7])
    
    if cube.read_state('index_estate_source_selected') is not None:
        columns[0].button(label='Modifier la source',
                icon=':material/edit:',
                on_click=patch_estate_source)
    else:
        columns[0].button(label='Ajouter la source',
                help="Permet de créer et d'ajouter une source de patrimoine à l'étude",
                icon=':material/add:',
                on_click=patch_estate_source)
    
    def delete_estate_source():
        cube.delete_estate_source()
        parent.success("La source de patrimoine a bien été supprimée")
    
    if cube.read_state('index_estate_source_selected') is not None:
        columns[1].button(label='Supprimer la source',
                help="Retire cette source de la liste des sources de patrimoine",
                icon=':material/clear:',
                on_click=delete_estate_source)