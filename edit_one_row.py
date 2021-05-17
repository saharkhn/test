import spacy_udpipe
import argparse
import sqlite3

def run(conn):

    c= conn.cursor()
    c.execute("SELECT * FROM Document")
    column_names = [description[0] for description in c.description]
    document_names = [d[1] for d in c.fetchall()]

    parser = argparse.ArgumentParser("Subprogram - edit one row in database")
    parser.add_argument("action")
    parser.add_argument("document_name", choices= document_names)
    parser.add_argument("column_name", choices= column_names)
    parser.add_argument("new_data")

    args = parser.parse_args()

    try:
        c = conn.cursor()
        c.execute("UPDATE Document SET " + args.column_name + " = ? WHERE name = ?", (args.new_data, args.document_name))
        conn.commit()
        c.close()
        conn.close()

    except sqlite3.OperationalError:
        print("Column doesn't exist ... ")
    except sqlite3.IntegrityError:
        print("The new data is duplicate ...")