import pandas as pd
import streamlit as st
from utils.utils import *
import datetime

if __name__ == "__main__":
    st.set_page_config(
        page_title="Inserimento lezioni",
        layout="wide",
        page_icon="images/favicon.png",
        initial_sidebar_state="collapsed",
    )

    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()

    st.title("Inserimento :red[lezioni]")

    try:
        with st.form("form_inserimento_lezioni"):
            query = "SELECT CodFisc FROM Istruttore"
            res = execute_query(st.session_state["connection"], query)
            listCodFisc = [data[0] for data in res]

            codFisc = st.selectbox("Codice fiscale istruttore", listCodFisc)

            giorno = st.selectbox("Giorno", ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"])

            oraInizio = st.time_input("Ora di inizio", value=datetime.time(8, 0))

            durata = st.slider("Durata", value=20, min_value=1, max_value=60)

            sala = st.text_input("Sala", placeholder="Inserire il nome della sala...")

            query = "SELECT CodC FROM Corsi"
            res = execute_query(st.session_state["connection"], query)
            listCodC = [data[0] for data in res]
            codC = st.selectbox("Codice corso", listCodC)

            submitted = st.form_submit_button("Invia")
    
        if submitted:
            query = f"SELECT COUNT(*) FROM Programma WHERE Giorno = '{giorno}' AND CodC = '{codC}'"
            res = execute_query(st.session_state["connection"], query)
            listCnt = [data[0] for data in res]
            cnt = int(listCnt[0])

            print(sala)

            if cnt != 0:
                st.error(f"E' già presente una lezione per il corso {codC} nella giornata di {giorno}")
            else:
                if codFisc != '' and giorno != '' and oraInizio.isoformat() != '' and sala != '' and codC != '':
                    query = f"INSERT INTO Programma (CodFisc, Giorno, OraInizio, Durata, Sala, CodC) VALUES ('{codFisc}', '{giorno}', '{oraInizio.isoformat()}', {durata}, '{sala}', '{codC}')"
                    try:
                        execute_query(st.session_state["connection"], query)
                        st.session_state["connection"].commit()

                        st.success("Inserimento andato a buon fine")
                    except Exception as e:
                        st.error("Errore durante l'inserimento dei dati")
                        print(e)
                else:
                    st.error("Alcuni campi sono incompleti")
    except:
        st.error("Recupero dati fallito, controllare la connessione al DB")