import requests
import polars as pl
import streamlit as st
from datetime import datetime
import json
from typing import Literal

class Cube:
    def __init__(self):
        if 'sources' not in st.session_state or self.read_state('sources') is None:
            st.session_state['sources'] = {
                'income': [],
                'estate': []
            }
            
        if 'dataframe' not in st.session_state or self.get_df_estate_sources() is None:
            st.session_state['dataframe'] = pl.DataFrame()
            
        if 'df_income_sources' not in st.session_state or self.get_df_income_sources() is None:
            st.session_state['df_income_sources'] = pl.DataFrame()
            
        if 'index_estate_source_selected' not in st.session_state:
            self.write_state(key='index_estate_source_selected', value=None)
            
        if 'index_income_source_selected' not in st.session_state:
            self.write_state(key='index_income_source_selected', value=None)
            
        if 'income_source_social_toggle' not in st.session_state:
            self.write_state(key='income_source_social_toggle', value=False)
    
    ###   Setters pour écrire des données sur le cube   ###
    
    def load_sources_file(self):
        uploaded_file = self.read_state('sources_file_uploader')
        
        try:
            string_to_eval = uploaded_file.getvalue().decode("utf-8")
            value = json.loads(string_to_eval)
            
        except ValueError as err:
            raise Exception(f"Le fichier source n'a pas pu être lu :\n{string_to_eval}")
        
        self.write_state(key='sources',
                         value=value)
        
        self.update_df_sources()
        
    def update_df_sources(self):        
        self.write_state(key='dataframe',
                         value=pl.from_records(self.read_state('sources')['estate']))
        
        self.write_state(key='df_income_sources',
                         value=pl.from_records(self.read_state('sources')['income']))
    
    def patch_source(self, type: Literal['estate', 'income'], source: dict):
        """Ajoute une source de revenu ou de patrimoine au cube de données.

        Args:
            type (Literal['estate', 'income']): Le type de source à ajouter au cube.
            source (dict): La source avec toutes ses propriétés.
        """
        value = self.read_state('sources')
        
        if self.read_state(f'index_{type}_source_selected') is None:
            value[type].append(source)
        else:
            value[type][self.read_state(f'index_{type}_source_selected')] = source        
        
        self.write_state(key='sources',
                         value=value)
        
        self.update_df_sources()

    def save_sources(self):
        timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%s")
        file_path = f'./data/personal_sources_{timestamp}.json'

        with open(file_path, 'w') as file:
            json.dump(self.read_state('sources'), file)
        
    def read_state(self, key: str = None):
        if key is None:
            return st.session_state
        
        if key not in st.session_state:
            raise Exception(f"La clé '{key}' n'existe pas dans le state")
        
        return st.session_state[key]
    
    def write_state(self, key: str, value):        
        st.session_state[key] = value
            
    def is_dataframe_initialized(self):
        return self.get_df_estate_sources().shape[0] > 0
        
    def on_select_estate_source(self):
        selected_rows_index = self.read_state('estate_sources_dataframe')['selection']['rows']
        
        if len(selected_rows_index) == 0:
            self.write_state(key='index_estate_source_selected', value=None)
            
            self.write_state(key='input_estate_source_type',
                         value=None)
        
            self.write_state(key='input_estate_source_label',
                            value=None)
            
            self.write_state(key='input_estate_source_amount',
                            value=0.)
            
            self.write_state(key='input_estate_source_deposit',
                            value=0.)
            
            self.write_state(key='input_estate_source_limit',
                            value=None)
            
            self.write_state(key='input_estate_source_return',
                            value=0.)
        else:
            index_source = selected_rows_index[0]
            
            self.write_state(key='index_estate_source_selected', value=index_source)
            
            estate_source_row = self.get_df_estate_sources().row(index=index_source, named=True)
            
            self.write_state(key='input_estate_source_type',
                            value=estate_source_row['Catégorie'])
            
            self.write_state(key='input_estate_source_label',
                            value=estate_source_row['Label'])
            
            self.write_state(key='input_estate_source_amount',
                            value=estate_source_row['Montant à date'])
            
            self.write_state(key='input_estate_source_deposit',
                            value=estate_source_row['Apport annuel'])
            
            self.write_state(key='input_estate_source_limit',
                            value=estate_source_row['Plafond'])
        
            self.write_state(key='input_estate_source_return',
                            value=estate_source_row['Rendement'])
         
    def is_income_source_selected(self) -> bool:
        selected_rows_index = self.read_state('income_sources_dataframe')['selection']['rows']
        
        return len(selected_rows_index) > 0
            
    def on_select_income_source(self):
        selected_rows_index = self.read_state('income_sources_dataframe')['selection']['rows']
        
        if len(selected_rows_index) == 0:
            self.write_state(key='income_source_type_selection', value=None)
            
            self.write_state(key='input_income_source_label',
                         value=None)
        
            self.write_state(key='input_annual_gross_salary',
                            value=None)
            
            self.write_state(key='input_annual_net_salary',
                            value=0.)
            
            self.write_state(key='input_annual_net_salary_after_tax',
                            value=0.)
            
            self.write_state(key='input_average_annual_increase',
                            value=None)
        else:
            index_source = selected_rows_index[0]
            
            self.write_state(key='index_income_source_selected', value=index_source)
            
            income_source_row = self.get_df_income_sources().row(index=index_source, named=True)
            
            self.write_state(key='income_source_type_selection',
                            value=income_source_row['Catégorie'])
            
            self.write_state(key='input_income_source_label',
                            value=income_source_row['Label'])
                        
            self.write_state(key='input_annual_gross_salary',
                            value=income_source_row['Montant annuel brut'])
            
            self.write_state(key='input_annual_net_salary',
                            value=income_source_row['Montant annuel net'])
            
            self.write_state(key='input_annual_net_salary_after_tax',
                            value=income_source_row['Montant annuel net après impôt'])
            
            self.write_state(key='input_average_annual_increase',
                            value=income_source_row['Augmentation moyenne annuelle'])
    
    def delete_source(self, type: Literal['estate', 'income']):
        value = self.read_state('sources')
        value['type'].pop(self.read_state(f'index_{type}_source_selected'))
        
        self.write_state(key='sources', value=value)
        
        self.update_df_sources()
    
    def delete_estate_source(self):
        self.delete_source(type='estate')
        
    def delete_income_source(self):
        self.delete_source(type='income')
            
    ###   Getters pour lire des données du cube   ###
    
    def get_bitcoin_price(self):
        # CoinDesk API endpoint for Bitcoin price
        url = 'https://api.coindesk.com/v1/bpi/currentprice.json'

        # Make the API request
        response = requests.get(url)

        # Parse the JSON response
        data = response.json()

        # Extract the Bitcoin price in USD
        bitcoin_price = data['bpi']['EUR']['rate_float']

        return bitcoin_price
    
    def get_estate_sources(self):
        df = self.get_df_estate_sources()
        return df.unique(subset='Label')
        
    def get_estate_projection(self, years: int = 10) -> pl.DataFrame:
        results = []
        
        current_year = datetime.now().year
        
        def compute_future_amounts(montant_initial, estate_source_part, rendement, years): 
            montants = [montant_initial]
            
            for year in range(years):
                annual_deposit = estate_source_part * self.compute_total_income(years=year)[2]
                montants.append(montants[-1] * (1 + rendement / 100) + annual_deposit) 
            
            return montants
        
        for row in self.get_df_estate_sources().iter_rows():
            future_amounts = compute_future_amounts(montant_initial=row[2],
                                                    estate_source_part=self.compute_estate_source_part(source_label=row[1]),
                                                    rendement=row[5],
                                                    years=years) 
            
            for year, amount in enumerate(future_amounts): 
                results.append({
                    'estate_source': row[1],
                    'date': datetime(year=current_year + year, month=1, day=1),
                    'estate_amount': amount
                }) 
                # Convert the results to a Polars DataFrame 
            
        results_df = pl.DataFrame(results)
        
        return results_df
        
    def get_df_estate_sources(self) -> pl.DataFrame:
        """Renvoie le DataFrame stocké dans le state de l'application, et avec lui toutes les informations concernant
        les sources de patrimoine.

        Returns:
            pl.DataFrame: Le DataFrame contenant les sources de patrimoine.
        """
        return self.read_state('dataframe')
    
    def get_df_income_sources(self) -> pl.DataFrame:
        """Renvoie le DataFrame stocké dans le state de l'application, et avec lui toutes les informations concernant
        les sources de revenu.

        Returns:
            pl.DataFrame: Le DataFrame contenant les sources de revenu.
        """
        return self.read_state('df_income_sources')
    
    ###   Fonctions pour le calcul de valeur   ###
    
    def compute_monthly_saved_amount(self) -> float:
        """Calcule le montant total épargné chaque mois, en divisant le total des apports annuels de toutes les sources de données par 12.

        Returns:
            float: Le montant total épargné chaque mois.
        """
        return self.get_df_estate_sources().select('Apport annuel').sum().item() / 12
    
    def compute_monthly_available_income(self) -> float:
        """Calcule le revenu disponible chaque mois, en divisant le salaire annuel net après impôt par 12.

        Returns:
            float: Le revenu disponible mensuel.
        """
        gross_salary = self.get_df_income_sources().select('Montant annuel brut').sum().item()
        _, _, net_salary_after_tax = self.compute_net_income(gross_salary=gross_salary)
        return net_salary_after_tax / 12
    
    def compute_saving_rate(self) -> float:
        """Calcule le taux d'épargne mensuel, en divisant le montant total épargné chaque mois par le revenu disponible de chaque mois.

        Returns:
            float: Le taux d'épargne mensuel.
        """
        return self.compute_monthly_saved_amount() / self.compute_monthly_available_income()
    
    def compute_total_estate(self, years: int = 0) -> float:
        """Calcule la projection du montant total du patrimoine à l'échéance demandée en nombre d'années.

        Args:
            years (int, optional): L'échéance en nombre d'années. Defaults to 0.

        Returns:
            float: Le montant total du patrimoine à l'échéance.
        """
        df = self.get_estate_projection(years=years)
        
        max_date = df.select(pl.col('date').max()).item()
        
        return df.filter(pl.col('date') == max_date).select(pl.col('estate_amount').sum()).item()
    
    def compute_total_income(self, years: int = 0) -> float:
        """Calcule la projection du montant total du revenu à l'échéance demandée en nombre d'années.

        Args:
            years (int, optional): L'échéance en nombre d'années. Defaults to 0.

        Returns:
            tuple: (Le revenu annuel brut, le revenu annuel net, le revenu annuel net après impôt sur le revenu).
        """
        df = self.compute_income_projection(years=years)
        
        max_date = df.select(pl.col('date').max()).item()
        
        df = df.filter(pl.col('date') == max_date)
        
        return (
            df.select(pl.col('Montant annuel brut').sum()).item(),
            df.select(pl.col('Montant annuel net').sum()).item(),
            df.select(pl.col('Montant annuel net après impôt').sum()).item()
        )
    
    def compute_income_projection(self, years: int = 0) -> pl.DataFrame:
        results = []
                
        for row in self.get_df_income_sources().iter_rows():
            for year in range(years + 1):
                gross_salary_after_increase = row[2] * ((1 + row[5] / 100) ** year)
                
                gross_salary, net_salary_before_tax, net_salary_after_tax = self.compute_net_income(gross_salary=gross_salary_after_increase)
                
                results.append({
                    'income_source': row[1],
                    'date': datetime(year=self.get_current_year() + year, month=1, day=1),
                    'Montant annuel brut': gross_salary,
                    'Montant annuel net': net_salary_before_tax,
                    'Montant annuel net après impôt': net_salary_after_tax
                }) 
            
        return pl.DataFrame(results)
    
    def get_social_contributions_df(self) -> pl.DataFrame:
        return pl.DataFrame(data=[
            # ('Nom de la contribution', taux salarial)
            ('complementaire_sante', 1.22),
            ("securite_sociale_plafonnee", 6.90),
            ("securite_sociale_deplafonnee", 0.4),
            ("complementaire_tu1", 4.364),
            ("apec", 0.024),
            ("csg_crds", 2.9),
            ("csg", 6.8)
        ],
                     schema={'Cotisations sociales': pl.String, 'Taux': pl.Float32},
                     orient='row')
    
    def is_column_in_df(self, df: pl.DataFrame, column: str) -> bool:
        try:
            df.get_column(name=column)
            return True
        except pl.exceptions.ColumnNotFoundError:
            return False
        except Exception as err:
            raise err
    
    def compute_net_income(self, gross_salary: float):
        if self.is_column_in_df(df=self.get_df_income_sources(), column='Cotisations sociales'):
            # Liste des contributions sociales
            social_contributions = self.get_df_income_sources().select('Cotisations sociales').to_dicts()['Cotisations sociales']
            social_contributions = [(c[0]['Cotisations sociales'], c[1]['Taux'] / 100) for c in social_contributions]
        else:
            social_contributions = self.get_social_contributions_df().to_dicts()
            social_contributions = [(c['Cotisations sociales'], c['Taux'] / 100) for c in social_contributions]
            
        # Autres éléments de paie
        other_salary_elements = [
            ('indemnite_teletravail', 20),
            ('tickets_restaurants', -86),
            ('indemnite_transport', 14.85)
        ]
        
        all_social_contributions = sum([contribution[1] for contribution in social_contributions])
        
        social_net_income = gross_salary * (1 - all_social_contributions)
                
        net_salary_before_tax =  social_net_income + sum([element[1] * 12 for element in other_salary_elements])
        
        taxable_social_contributions = sum(contribution[1] for contribution in social_contributions if contribution[0] != 'csg')
        
        net_salary_taxable = gross_salary * (1 - taxable_social_contributions)
        
        # Tax brackets and rates for 2024
        tax_brackets = [
            # (Salaire brut, taux d'imposition)
            (0, 0.00),
            (11295, 0.11),
            (28798, 0.30),
            (82342, 0.41),
            (177107, 0.45)
        ]
        
        # Calculate income tax
        tax = 0
        
        for bracket in tax_brackets:
            if net_salary_taxable >= bracket[0]:
                taxable_income = net_salary_taxable - bracket[0]
                tax += taxable_income * bracket[1]
        
        net_salary_after_tax = net_salary_before_tax - tax
        
        return [gross_salary, net_salary_before_tax, net_salary_after_tax]
    
    def compute_estate_source_part(self, source_label: str) -> float:
        annual_deposit = self.get_df_estate_sources().filter(pl.col('Label') == source_label).select(pl.col('Apport annuel').sum()).item()
        annual_available_income = self.compute_total_income()[2]
        
        return annual_deposit / annual_available_income
    
    def compute_left_income(self, years: int = 0) -> pl.DataFrame:
        results = []
        
        for year in range(years + 1):
            annual_net_income_after_tax = self.compute_total_income(years=year)[2]
            annual_total_deposit = self.compute_annual_deposit(years=year)
            
            results.append({
                'date': datetime(year=self.get_current_year() + year, month=1, day=1),
                'Montant annuel net après impôt': annual_net_income_after_tax,
                'Investissement annuel': annual_total_deposit,
                "Revenu restant après investissement": annual_net_income_after_tax - annual_total_deposit,
                "saving_rate": annual_total_deposit / annual_net_income_after_tax
            })
        
        return pl.DataFrame(results)
    
    def compute_annual_deposit(self, years: int) -> float:
        result = 0
        
        for row in self.get_df_estate_sources().iter_rows():
            result += self.compute_estate_source_part(source_label=row[1]) * self.compute_total_income(years=years)[2]
        
        return result
    
    def get_current_year(self) -> int:
        return datetime.now().year