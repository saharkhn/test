import argparse
import find_all_ratios

def run(conn):

    c = conn.cursor()
    c.execute("SELECT DISTINCT Category FROM Document WHERE Category != (?)", (' ',))

    parser= argparse.ArgumentParser("Subprogram - find ratios with category value")
    parser.add_argument("action")
    parser.add_argument("category_value", choices= [d[0] for d in c.fetchall()])

    args = parser.parse_args()
    
    c.execute("SELECT Name FROM Document WHERE Category = ?", (args.category_value,))
    document_names = c.fetchall()
    find_all_ratios.documents_ratios(conn, document_names)