import add_to_database
import sqlite3
import json
import argparse
from typing import Tuple, List


def find_documentID(conn, name: str) -> int:

    c = conn.cursor()
    c.execute("SELECT DocumentID FROM Document WHERE Name = (?)", (name,))
    DocumentID = c.fetchone()

    return DocumentID


def run(conn):

    c = conn.cursor()
    c.execute("SELECT Name FROM Document")
    document_names = [name[0] for name in c.fetchall()]

    parser = argparse.ArgumentParser('Subprogram - add labels to existing document')
    parser.add_argument("action")
    parser.add_argument("json_file")
    parser.add_argument("document_name", choices= document_names)

    args = parser.parse_args()

    with open(args.json_file, 'r', encoding='utf8') as file:
        tasks = json.load(file)

    DocumentID = find_documentID(conn, args.document_name)
    
    if DocumentID != None:
        # Find all labels in this document with the name of the document
        completions_information = add_to_database.find_completion(tasks, args.document_name)
        print(completions_information)
        
        # Add label information (start, end, label_name) into table Label
        if completions_information != []:
            CompletionID = add_to_database.completion_entry(conn, len(completions_information), DocumentID[0])
            add_to_database.label_entry(conn, completions_information, CompletionID)
    else:
        print("Document doesn't exist !")
