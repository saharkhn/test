
import spacy_udpipe
import argparse
import json
import sqlite3
from typing import Tuple, List, Union


def data_entry(conn, name: str, link: str, domain: str, category: str, raw_text: str, clean_text: str, number_of_sentences: int, number_of_words: int) -> int:
    try:
        c = conn.cursor()
        c.execute("INSERT INTO Document(Name, Link, Domain, Category, Raw_text, Clean_text, Number_of_sentences, Number_of_words) VALUES(?,?,?,?,?,?,?,?)", (name, link, domain, category, raw_text, clean_text, number_of_sentences, number_of_words))
        conn.commit()
        print("Document was added to database . ")
        return c.lastrowid
    except:
        print("Data exist ... ")
        return -1


def label_entry(conn, completions_information: List[List[List[Union[int, str]]]], CompletionIDs: List[int]) -> None:
    
    c = conn.cursor()

    for i, completion in enumerate(CompletionIDs):
        for label in completions_information[i]:
            c.execute("INSERT INTO Label(CompletionID, Start, End, Label_name, Label_text) VALUES (?,?,?,?,?)", (completion, label[0], label[1], label[2], label[3]))
            conn.commit()
    print("Labels were added to Database . ")


def completion_entry(conn, number_of_completion: int, DocumentID: int) -> List[int]:

    c = conn.cursor()
    CompletionIDs = []
    for i in range(number_of_completion):
        c.execute("INSERT INTO Completion(DocumentID) VALUES (?)", (DocumentID,))
        conn.commit()
        CompletionIDs.append(c.lastrowid)
    
    return CompletionIDs


def count_sentences_words(clean_text: str) -> Tuple[int, int]:
    
    nlp = spacy_udpipe.load_from_path(lang='en', path='./english-ewt-ud-2.5-191206.udpipe')
    tokens = nlp(clean_text)  
    
    # Count number of sentences and words
    n_sentences = len(list(tokens.sents))
    n_words = len(list(word for word in tokens if word.pos_ != 'PUNCT'))
    
    return n_sentences, n_words


def find_completion(tasks, name: str) -> List[List[List[Union[int, str]]]]:
    
    completions_information = []
    for task in tasks:
        source = task['data']['source'] if 'data' in task and 'source' in task['data'] else None
        if source == name:
            completions = [c for c in task['completions'] if 'skipped' not in c or not c['skipped']]
            if len(completions) == 0:
                print(f'Skipping document with id {task["id"]}, since it has no completions.')
                break
            
            for i in range (len(completions)):
                completion = completions[i]
                clean_text = task['data']['text']
                completions_information.append([])
                for label_result in completion['result']:
                    for label_clazz in label_result['value']['labels']:
                        completions_information[i].append([label_result['value']['start'], label_result['value']['end'], label_clazz, label_result['value']['text']])
                        # label_name, start, end
            break

    return completions_information


def run(conn):

    parser = argparse.ArgumentParser("Subprogram - add document and labels to database")
    parser.add_argument("action")
    parser.add_argument("raw_text")
    parser.add_argument("clean_text")
    parser.add_argument("json_file")
    parser.add_argument("document_name")
    parser.add_argument("link")
    parser.add_argument("domain")
    parser.add_argument("category")

    args = parser.parse_args()

    with open(args.raw_text, 'r+',encoding='utf8') as file:
        raw_text = file.read()

    with open(args.clean_text, 'r', encoding='utf8') as file:
        clean_text = file.read()

    with open(args.json_file, 'r', encoding='utf8') as file:
        tasks = json.load(file)

    # Count number of sentences and words 
    n_sentences, n_words = count_sentences_words(clean_text)

    # Add (name, link, domain, category, raw_text, clean_text, number_of_sentences, number_of_words) to table 'Document'
    DocumentID = data_entry(conn, args.document_name, args.link, args.domain, args.category, raw_text, clean_text, n_sentences, n_words)
    
    if DocumentID != -1:
        # Find all labels in this document with the name of the document
        completions_information = find_completion(tasks, args.document_name)
        
        # Add label information (start, end, label_name, label_text) into table Label
        if completions_information != []:
            CompletionIDs = completion_entry(conn, len(completions_information), DocumentID)
            label_entry(conn, completions_information, CompletionIDs)
        
            

    




