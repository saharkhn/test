import argparse
import sqlite3

def run(conn):

    c= conn.cursor()
    c.execute("SELECT DISTINCT Domain FROM Document WHERE Domain != (?)", (' ',))
    domain_values= [n[0] for n in c.fetchall()]

    parser = argparse.ArgumentParser("Subprogram - count documents by domain value")
    parser.add_argument("action")
    parser.add_argument("column_value", choices= domain_values)

    args = parser.parse_args()

    c = conn.cursor()
    c.execute("SELECT Name FROM Document WHERE Domain= (?)", (args.column_value,))
    doc_names = [d[0] for d in c.fetchall()]
    print(len(doc_names), "\n", doc_names)