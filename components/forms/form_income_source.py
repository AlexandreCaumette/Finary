import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from data.cube import Cube
import data.constants as cst

from components.forms.form_inputs import number_input, patch_button

cube = Cube()

def reset_toggle():
    if cube.read_state('income_source_type_selection') != 'Salaire':
        cube.write_state('income_source_social_toggle', False)

def income_source_form(parent: DeltaGenerator):    
    parent.selectbox(label='Sélectionner un type de source de revenu',
                options=cst.INCOME_SOURCES_LIST,
                key='income_source_type_selection',
                on_change=reset_toggle,
                index=None)
    
    toggle = parent.toggle(label="Je connais mes taux de cotisation sociale",
                    key='income_source_social_toggle',
                  value=False,
                  disabled=cube.read_state('income_source_type_selection') != 'Salaire')
    
    columns = parent.columns([1, 1] if toggle else [1], border=toggle)
    
    columns[0].text_input('Le label de la source', key='input_income_source_label')
    
    number_input(parent=columns[0],
                 label='Salaire annuel brut',
                 key='input_annual_gross_salary')
    
    number_input(parent=columns[0],
                 label='Salaire annuel net',
                 key='input_annual_net_salary')
    
    number_input(parent=columns[0],
                 label='Salaire annuel net après impôt',
                 key='input_annual_net_salary_after_tax')
    
    number_input(parent=columns[0],
                 label='Augmentation moyenne annuelle (en %)',
                 key='input_average_annual_increase')
    
    if cube.read_state('income_source_social_toggle'):
        columns[1].text("La liste des contributions sociales mentionnées sur votre fichie de paie.")
        
        df_input_social_contributions = columns[1].data_editor(data=cube.get_social_contributions_df(),
                               num_rows='dynamic',
                               column_config={
                                   'Taux': st.column_config.NumberColumn(
                                       help="Le taux de cotisation salariale en pourcentage.",
                                       min_value=0.,
                                       step=0.5,
                                       format="%.2f %%"
                                   )
                               },
                               width=600,
                               key='input_social_contributions')
    
    def patch_income_source():
        source = {
            'Catégorie': cube.read_state('income_source_type_selection'),
            'Label': cube.read_state('input_income_source_label'),
            'Montant annuel brut': cube.read_state('input_annual_gross_salary'),
            'Montant annuel net': cube.read_state('input_annual_net_salary'),
            'Montant annuel net après impôt': cube.read_state('input_annual_net_salary_after_tax'),
            'Augmentation moyenne annuelle': cube.read_state('input_average_annual_increase')
        }
        
        if cube.read_state('income_source_social_toggle'):
            print(df_input_social_contributions)
            source['Cotisations sociales'] = df_input_social_contributions.to_dicts()
        
        cube.patch_source(type='income', source=source)
        
        parent.success("La nouvelle source de revenu a bien été ajoutée !", icon="💸")
        
    columns = parent.columns([1, 1, 5])
    
    patch_button(parent=columns[0], on_click=patch_income_source, key='index_income_source_selected')
    
    def delete_income_source():
        cube.delete_income_source()
        parent.success("La source de revenu a bien été supprimée")
    
    if cube.read_state('index_income_source_selected') is not None:
        columns[1].button(label='Supprimer la source',
                help="Retire cette source de la liste des sources de revenu",
                icon=':material/clear:',
                type='secondary',
                on_click=delete_income_source)