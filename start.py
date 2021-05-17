import add_to_database
import edit_one_row
import clean_text
import delete_from_database
import add_label_to_exist_document
import count_document_by_domain
import count_document_by_category
import find_all_ratios
import find_ratio_by_name
import find_ratio_by_domain
import find_ratio_by_category
import argparse
import sqlite3

def main():

    conn = sqlite3.connect("prozess.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = 1")
    conn.commit()
    
    action_dict = {'clean_text' : clean_text, 'add_to_database' : add_to_database, 'delete_from_database' : delete_from_database,
                    'edit_one_row' : edit_one_row, 'add_label_to_exist_document' : add_label_to_exist_document,
                    'count_document_by_domain' : count_document_by_domain, 'count_document_by_category' : count_document_by_category,
                    'find_all_ratios':find_all_ratios, 'find_ratio_by_name':find_ratio_by_name, 
                    'find_ratio_by_domain':find_ratio_by_domain, 'find_ratio_by_category':find_ratio_by_category}

    parser = argparse.ArgumentParser('Main program to choose a subprogram')
    parser.add_argument("action", choices= action_dict.keys())
    namespace, extra = parser.parse_known_args()

    for action in action_dict.keys():
        if namespace.action == action:
            action_dict[action].run(conn)
       

if __name__ == '__main__':
    main()