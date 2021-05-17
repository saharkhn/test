import argparse
import sqlite3

def run(conn):

    c= conn.cursor()
    c.execute("SELECT DISTINCT Category FROM Document WHERE Category != (?)", (' ',))
    category_values= [n[0] for n in c.fetchall()]

    parser = argparse.ArgumentParser("Subprogram - count documents by category value")
    parser.add_argument("action")
    parser.add_argument("column_value", choices= category_values)

    args = parser.parse_args()

    c = conn.cursor()
    c.execute("SELECT Name FROM Document WHERE Category= (?)", (args.column_value,))
    doc_names = [d[0] for d in c.fetchall()]
    print(len(doc_names), "\n", doc_names)