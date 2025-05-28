from utils.utils import *
import streamlit as st
import pandas as pd

if __name__ == "__main__":
    check_connection()

    st.title("Prenotazioni")

    col1, col2 = st.columns(2)

    with col1:
        query = "WITH COSTO_MENSILE_STANZA AS (SELECT MONTH(DataInizio) AS Mese, STANZA_CodS, AVG(Costo / (DATEDIFF(DataFine, DataInizio) + 1)) AS Costo FROM PRENOTAZIONE GROUP BY MONTH(DataInizio), STANZA_CodS) SELECT CM.Mese, CM.Costo AS 'Costo giornaliero medio massimo', S.CodS, S.Piano, S.Superficie, S.Type AS Tipo FROM STANZA S, COSTO_MENSILE_STANZA CM WHERE CM.STANZA_CodS = S.CodS AND CM.Costo = (SELECT MAX(CM2.Costo) FROM COSTO_MENSILE_STANZA CM2 WHERE CM2.Mese = CM.Mese) ORDER BY CM.Mese ASC"
        result = execute_query(st.session_state["connection"], query)
        df_bookings = pd.DataFrame(result)

        st.dataframe(df_bookings, use_container_width=True)

    with col2:
        query = "WITH COSTO_MENSILE_STANZA AS (SELECT MONTH(DataInizio) AS Mese, STANZA_CodS, AVG(Costo / (DATEDIFF(DataFine, DataInizio) + 1)) AS Costo FROM PRENOTAZIONE GROUP BY MONTH(DataInizio), STANZA_CodS) SELECT CM.Mese, AVG(Costo) AS 'Costo giornaliero medio' FROM COSTO_MENSILE_STANZA CM GROUP BY CM.Mese"
        result = execute_query(st.session_state["connection"], query)
        df_month_cost = pd.DataFrame(result)

        st.line_chart(df_month_cost, x="Mese", y="Costo giornaliero medio", use_container_width=True)