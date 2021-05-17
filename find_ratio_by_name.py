import argparse
import find_all_ratios

def run(conn):

    c = conn.cursor()
    c.execute("SELECT Name FROM Document")

    parser= argparse.ArgumentParser("Subprogram - find ratio with document name")
    parser.add_argument("action")
    parser.add_argument("document_name", choices= [d[0] for d in c.fetchall()])

    args = parser.parse_args()
    
    c.execute("SELECT Name FROM Document WHERE Name = ? ", (args.document_name,))
    document_names = c.fetchall()
    find_all_ratios.documents_ratios(conn, document_names)