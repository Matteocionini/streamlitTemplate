import pandas as pd
import streamlit as st
from utils.utils import *
import re

if __name__ == "__main__":
    st.set_page_config(
        page_title="Inserimento corsi",
        layout="wide",
        page_icon="images/favicon.png",
        initial_sidebar_state="collapsed",
    )

    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()

    st.title("Inserimento :red[corsi]")

    with st.form("form_inserimento_corsi"):
        codC = st.text_input("Codice corso", placeholder="CTxxx")
        nome = st.text_input("Nome corso")
        tipo = st.text_input("Tipo")
        livello = st.number_input("Livello", value=1, min_value=1)

        submitted = st.form_submit_button("Invia")

    if submitted:
        pattern = r'^CT1\d{2}$'
        regex = re.compile(pattern)

        if not regex.fullmatch(codC):
            st.error("Formato del codice corso errato")
        elif codC == '' or nome == '' or tipo == '':
            st.error("Alcuni campi sono incompleti")
        else:
            if st.session_state["connection"] is not False:
                try:
                    query = f"INSERT INTO Corsi (CodC, Nome, Tipo, Livello) VALUES ('{codC}', '{nome}', '{tipo}', {livello})"
                    print(query)
                    execute_query(st.session_state["connection"], query)
                    st.session_state["connection"].commit()

                    st.success("Inserimento andato a buon fine")
                except:
                    st.error("Errore durante l'inserimento")
            else:
                st.error("Connessione al DB fallita")
    
