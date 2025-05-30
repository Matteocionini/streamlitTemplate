import pandas as pd
import streamlit as st
from utils.utils import *

if __name__ == "__main__":
    st.set_page_config(
        page_title="Corsi",
        layout="wide",
        page_icon="images/favicon.png",
        initial_sidebar_state="collapsed",
    )

    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()

    st.title(":red[Corsi]")

    col1, col2 = st.columns(2)

    with col1:
        query = "SELECT COUNT(*) AS NumCorsi FROM Corsi"
        try:
            res = execute_query(st.session_state["connection"], query)
            numCorsiDict = [dict(zip(res.keys(), data)) for data in res]

            st.metric("Numero corsi", numCorsiDict[0]["NumCorsi"])
        except:
            st.error("Recupero dati fallito, controllare la connessione al DB")

    with col2:
        query = "SELECT COUNT(DISTINCT Tipo) AS NumTipi FROM Corsi"

        try:
            res = execute_query(st.session_state["connection"], query)
            numTipiDict = [dict(zip(res.keys(), data)) for data in res]

            st.metric("Tipi diversi di corsi", numTipiDict[0]["NumTipi"])
        except:
            st.error("Recupero dati fallito, controllare la connessione al DB")
    
    with st.expander("Seleziona i programmi da visualizzare"):
        try:
            query = "SELECT DISTINCT Nome FROM Corsi"
            res = execute_query(st.session_state["connection"], query)
            nomiPossibili = [nome[0] for nome in res]
            nomiPossibili.append("Tutti")
            nome = st.selectbox("Nome", nomiPossibili, index=len(nomiPossibili)-1)
            if nome != "Tutti":
                nome = "'" + nome +"'"

            query = "SELECT DISTINCT Tipo FROM Corsi"
            res = execute_query(st.session_state["connection"], query)
            tipiPossibili = [tipo[0] for tipo in res]
            tipiPossibili.append("Tutti")
            tipo = st.radio("Tipo", tipiPossibili, index=len(tipiPossibili)-1)
            if tipo != "Tutti":
                tipo = "'" + tipo + "'"

            query = "SELECT MAX(Livello) AS Massimo, MIN(Livello) AS Minimo FROM Corsi"
            res = execute_query(st.session_state["connection"], query)
            livelli = [dict(zip(res.keys(), liv)) for liv in res]
            rangeLivello = st.slider("Range livello", min_value=livelli[0]["Minimo"], max_value=livelli[0]["Massimo"], value=(livelli[0]["Minimo"], livelli[0]["Massimo"]), step=1)
        except:
            st.error("Recupero dati fallito, controllare la connessione al DB")


    try:
        query = f"SELECT CodC AS 'Codice corso', Nome, Tipo, Livello FROM Corsi WHERE Nome {f'= {nome}' if nome != 'Tutti' else 'IS NOT NULL'} AND Tipo {f'= {tipo}' if tipo != 'Tutti' else 'IS NOT NULL'} AND Livello >= {rangeLivello[0]} AND Livello <= {rangeLivello[1]} ORDER BY CodC ASC"
        res = execute_query(st.session_state["connection"], query)
        df_corsi = pd.DataFrame(res)

        if not df_corsi.empty:
            st.dataframe(df_corsi, use_container_width=True)

            with st.expander("Programma corsi selezionati"):
                serieCorsi = df_corsi["Codice corso"].tolist()
                if len(serieCorsi) == 1:
                    query = f"SELECT P.CodC AS 'Codice corso', C.Nome, P.Giorno, P.OraInizio AS 'Ora Inizio', P.Durata, P.Sala, CONCAT(I.Nome, ' ', I.Cognome) AS 'Istruttore', I.Email AS 'Email istruttore' FROM Programma P, Istruttore I, Corsi C WHERE P.CodFisc = I.CodFisc AND P.CodC = '{serieCorsi[0]}' AND C.CodC = P.CodC ORDER BY P.CodC ASC"
                else:
                    serieCorsi = tuple(serieCorsi)
                    query = f"SELECT P.CodC AS 'Codice corso', C.Nome, P.Giorno, P.OraInizio AS 'Ora Inizio', P.Durata, P.Sala, CONCAT(I.Nome, ' ', I.Cognome) AS 'Istruttore', I.Email AS 'Email istruttore' FROM Programma P, Istruttore I, Corsi C WHERE P.CodFisc = I.CodFisc AND P.CodC IN {serieCorsi} AND C.CodC = P.CodC ORDER BY P.CodC ASC"

                res = execute_query(st.session_state["connection"], query)
                df_programma = pd.DataFrame(res)

                if not df_programma.empty:
                    st.dataframe(df_programma, use_container_width=True)
                else:
                    st.warning("Nessun programma disponibile per i corsi selezionati")
        else:
            st.warning("Nessun corso corrispondente alla selezione effettuata")
    except Exception as e:
        st.error("Recupero dati fallito, controllare la connessione al DB")    