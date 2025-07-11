import streamlit as st

from components.forms.form_signin import signin_form
from components.forms.signup import signup_form


st.header("Authentification à votre compte")

column_signin, column_signup = st.columns(2)

with column_signin:
    signin_form()

with column_signup:
    signup_form()
