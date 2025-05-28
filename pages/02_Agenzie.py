import streamlit as st
from utils.utils import *
import pandas as pd

if __name__ == "__main__":
    st.title("Agenzie")

    col1, col2, col3 = st.columns(3)

    check_connection()

    with col1:
        query1 = "SELECT COUNT(DISTINCT CodA) AS Conto FROM AGENZIA"
        result = execute_query(st.session_state["connection"], query1)
        conv_result = [dict(zip(result.keys(), dato)) for dato in result]

        st.metric("Numero agenzie", conv_result[0]["Conto"])
    
    with col2:
        query2 = "SELECT COUNT(DISTINCT Nome) AS Conto FROM CITTA"
        result = execute_query(st.session_state["connection"], query2)
        conv_result = [dict(zip(result.keys(), dato)) for dato in result]

        st.metric("Numero città", conv_result[0]["Conto"])

    with col3:
        query3 = "WITH NUM_AGENZIE AS(SELECT Citta_Indirizzo, COUNT(*) AS Numero_Agenzie FROM AGENZIA GROUP BY Citta_Indirizzo) SELECT Citta_Indirizzo FROM NUM_AGENZIE WHERE Numero_Agenzie = (SELECT MAX(Numero_Agenzie) FROM NUM_AGENZIE)"
        result = execute_query(st.session_state["connection"], query3)
        conv_result = [dict(zip(result.keys(), dato)) for dato in result]

        st.metric("Città con più agenzie", conv_result[0]["Citta_Indirizzo"])

    query4 = "SELECT DISTINCT C.Latitudine AS lat, C.Longitudine AS lon FROM CITTA C, AGENZIA A WHERE C.Nome = A.Citta_Indirizzo"
    lat_lon = execute_query(st.session_state["connection"], query4)
    df_lat_lon = pd.DataFrame(lat_lon)

    st.map(df_lat_lon)

    citta = st.text_input("Selezionare una città", placeholder="Milano")

    if citta == "":
        citta = "%"
    else:
        citta = citta + "%"

    query5 = f"SELECT CodA, Citta_Indirizzo, CONCAT(Via_Indirizzo, ', ', Numero_Indirizzo, ', ', CAP_Indirizzo) AS Indirizzo FROM AGENZIA WHERE Citta_Indirizzo LIKE \"{citta}\""
    agency_info = execute_query(st.session_state["connection"], query5)
    df_agency_info = pd.DataFrame(agency_info)

    if df_agency_info.empty:
        st.error("Nessuna agenzia disponibile")
    else:
        st.dataframe(df_agency_info, use_container_width=True)
    
