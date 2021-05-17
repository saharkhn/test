import spacy_udpipe
import argparse
import sqlite3


def run(conn):

    c = conn.cursor()
    c.execute("SELECT Name FROM Document")
    document_names = [name[0] for name in c.fetchall()]
    
    parser = argparse.ArgumentParser("Subprogram - delete document from database")
    parser.add_argument("action")
    parser.add_argument("document_name", choices= document_names)
    args = parser.parse_args()

    c = conn.cursor()
    c.execute("DELETE FROM Document WHERE Name = ? ",  (args.document_name,))
    conn.commit()
    
    if(conn.total_changes == 0):
        print("Document not found ! ")