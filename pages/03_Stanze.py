from utils.utils import *
import streamlit as st
import pandas as pd

if __name__ == "__main__":
    check_connection()

    st.title("Stanze")

    with st.expander("Filtri"):
        type = st.radio("Tipo", ["singola", "doppia", "tripla", "tutte"])

        query = "SELECT DISTINCT OPTIONAL_Optional FROM HAS_OPTIONAL"
        res = execute_query(st.session_state["connection"], query)
        availableOptions = [data[0] for data in res]

        optional = st.multiselect("Optional", availableOptions)

        cucina = st.checkbox("Cucina")

    query_base = "SELECT CodS, Piano, Superficie, Type AS Tipo FROM STANZA WHERE "
    
    if type == "tutte":
        query_type = "Type IN ('singola', 'doppia', 'tripla') "
    else:
        query_type = f"Type = \"{type}\" "

    if optional == []:
        query_optional = ""
    else:
        query_optional = ""
        for obj in optional:
            query_optional = query_optional + f"AND CodS IN (SELECT STANZA_CodS FROM HAS_OPTIONAL WHERE OPTIONAL_Optional = \"{obj}\") "

    query_cucina = f"AND CodS {'IN' if cucina else 'NOT IN'} (SELECT STANZA_CodS FROM HAS_SPAZI WHERE SPAZI_Spazi = \"cucina\")"

    query = query_base + query_type + query_optional + query_cucina

    print(query)

    res = execute_query(st.session_state["connection"], query)
    df_room_info = pd.DataFrame(res)

    st.dataframe(df_room_info, use_container_width=True)