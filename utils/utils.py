import streamlit as st
from sqlalchemy import create_engine,text

"""Raccoglie le principali funzioni condivise dalle varie pagine"""

def connect_db(dialect, username, password, host, dbname):
    engine = create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}')
    
    try:
        conn = engine.connect().execution_options(autocommit=True)
        return conn
    except:
        return False
    
def execute_query(conn, query):
    return conn.execute(text(query))

def compact_format(num):
    num=float(num)
    if abs(num) >= 1e9:
        return "{:.2f}B".format(num / 1e9)
    elif abs(num) >= 1e6:
        return "{:.2f}M".format(num / 1e6)
    elif abs(num) >= 1e3:
        return "{:.2f}K".format(num / 1e3)
    else:
        return "{:.0f}".format(num)
    
def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    if st.sidebar.button("Connetti al DB"):
        my_connection = connect_db(dialect="mysql+pymysql",username="root",password="mypassword",host="localhost",dbname="palestra")
        if my_connection is not False:
            st.session_state["connection"] = my_connection
        else:
            st.session_state["connection"] = False
            st.sidebar.error("Errore nella connessione")

    if st.session_state["connection"]:
        st.sidebar.success("Connesso al DB")
        return True
    else:
        return False