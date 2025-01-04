import streamlit as st

def read_state(key: str = None):
        if key is None:
            return st.session_state
        
        if key not in st.session_state:
            raise Exception(f"La clé '{key}' n'existe pas dans le state")
        
        return st.session_state[key]
    
def write_state(key: str, value):        
    st.session_state[key] = value