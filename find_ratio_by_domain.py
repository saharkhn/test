import argparse
import find_all_ratios

def run(conn):

    c = conn.cursor()
    c.execute("SELECT DISTINCT Domain FROM Document WHERE Domain != (?)", (' ',))

    parser= argparse.ArgumentParser("Subprogram - find ratios with domain value")
    parser.add_argument("action")
    parser.add_argument("domain_value", choices= [d[0] for d in c.fetchall()])

    args = parser.parse_args()
    
    c.execute("SELECT Name FROM Document WHERE Domain = ?", (args.domain_value,))
    document_names = c.fetchall()
    find_all_ratios.documents_ratios(conn, document_names)