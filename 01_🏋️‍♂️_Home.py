import pandas as pd
import streamlit as st
from utils.utils import *

if __name__ == "__main__":
    st.set_page_config(
        page_title="Dashboard palestra",
        layout="wide",
        page_icon="images/favicon.png",
        initial_sidebar_state="collapsed",
    )

    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()

    st.title(":red[Presentazione]")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Il :red[quaderno]")
        st.markdown(":red[**Quaderno 4**] del corso di *:red[Basi] di :red[dati]*, a.a *2024/2025*. L'obiettivo del quaderno è creare un’applicazione web in Python (:red[Streamlit]) in grado di interagire con un database *MySQL* in modo da eseguire interrogazioni in base alle interazioni dell’utente. Realizzato da :red[**Matteo Cionini**], matricola **321458**, studente di Ingegneria Informatica.")

    with col2:
        st.image("images/polito_white.png")

    st.subheader("Panoramica :red[lezioni]")

    tab1, tab2 = st.tabs(["Lezioni per slot orario", "Lezioni per giorno della settimana"])

    with tab1:
        query = "SELECT OraInizio AS Slot, COUNT(*) AS 'Numero lezioni' FROM Programma GROUP BY OraInizio ORDER BY OraInizio ASC"

        try:
            res = execute_query(st.session_state["connection"], query)
            df_lessPerSlot = pd.DataFrame(res)

            st.area_chart(df_lessPerSlot, x="Slot", y="Numero lezioni")
        except:
            st.error("Recupero dati fallito")

    with tab2:
        query = "SELECT Giorno, COUNT(*) AS 'Numero lezioni' FROM Programma GROUP BY Giorno ORDER BY FIELD(Giorno, 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica')"

        try:
            res = execute_query(st.session_state["connection"], query)
            df_lessPerDay = pd.DataFrame(res)

            st.bar_chart(df_lessPerDay, x="Giorno", y="Numero lezioni")
        except:
            st.error("Recupero dati fallito")