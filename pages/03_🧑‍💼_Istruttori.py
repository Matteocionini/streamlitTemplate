import pandas as pd
import streamlit as st
from utils.utils import *
import datetime

if __name__ == "__main__":
    st.set_page_config(
        page_title="Istruttori",
        layout="wide",
        page_icon="images/favicon.png",
        initial_sidebar_state="collapsed",
    )

    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()

    st.title(":red[Istruttori]")

    st.markdown("#### Filtri")

    col1, col2 = st.columns(2)

    with col1:
        surname = st.text_input("Cognome")

    with col2:
        try:
            query = "SELECT MIN(DataNascita) AS MinDate, MAX(DataNascita) AS MaxDate FROM Istruttore"
            res = execute_query(st.session_state["connection"], query)
            date = [dict(zip(res.keys(), data)) for data in res]
            date_range = st.date_input("Data di nascita", min_value=date[0]["MinDate"], max_value=date[0]["MaxDate"], value = (date[0]["MinDate"], date[0]["MaxDate"]))
        except:
            st.error("Recupero dati fallito, controllare la connesione al DB")

    try:
        date_start = date_range[0].isoformat()
        date_end = date_range[1].isoformat()
        try:
            query = f"SELECT * FROM Istruttore WHERE Cognome LIKE '{surname}%' AND DataNascita >= '{date_start}' AND DataNascita <= '{date_end}'"
            res = execute_query(st.session_state["connection"], query)
            df_istruttori = pd.DataFrame(res)

            if df_istruttori.empty:
                st.warning("Nessun istruttore trovato")
            else:
                st.divider()

                col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
                with col1:
                    st.subheader("Codice fiscale")
                with col2:
                    st.subheader("Nome")
                with col3:
                    st.subheader("Cognome")
                with col4:
                    st.subheader("Data di nascita")
                with col5:
                    st.subheader("Email")
                with col6:
                    st.subheader("Telefono")

                st.divider()

                for (index, data) in df_istruttori.iterrows():
                    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
                    with col1:
                        st.write(data["CodFisc"])
                    with col2:
                        st.write(data["Nome"])
                    with col3:
                        st.write(data["Cognome"])
                    with col4:
                        st.write(data["DataNascita"].isoformat())
                    with col5:
                        st.write(data["Email"])
                    with col6:
                        if data["Telefono"] != None:
                            st.write(data["Telefono"])
                        else:
                            st.write("Non disponibile")
                    with col7:
                        st.image("images/placeholder.png")

                    st.divider()
        except:
            st.error("Recupero dati fallito, controllare la connesione al DB")
    except:
        st.warning("Completare la scelta del range di date")


        