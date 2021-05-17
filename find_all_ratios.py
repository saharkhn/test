import sqlite3
import json
import spacy_udpipe
import argparse
from typing import Tuple, List


def find_document_id(conn, name: str) -> int:

    c = conn.cursor()
    c.execute("SELECT DocumentID FROM Document where Name = ?", (name,))
    DocumentID = c.fetchone()[0]
    
    return DocumentID


def find_completion_ids(conn, DocumentID: int) -> List[Tuple[int]]:

    c = conn.cursor()
    c.execute("SELECT CompletionID FROM Completion where DocumentID = ?", (DocumentID,))
    CompletionIDs_list = [c[0] for c in c.fetchall()]

    return CompletionIDs_list


def find_tokens_labels_one_document(conn, CompletionIDs_list: List[Tuple[int]]) -> List[List[Tuple[str]]]:
    
    token_label_lists = []
    c = conn.cursor()

    for completion in CompletionIDs_list:
        token_label_list = []
        n_token = 0

        c.execute("SELECT Label_text,Label_name FROM Label WHERE CompletionID = ?", (completion,))
        token_label_list = [c[0:2] for c in c.fetchall()]  # [('admin', 'Role'), ('sends', 'Task'), ('mail', 'Business Object')]
        
        token_label_lists.append(token_label_list)
    
    return token_label_lists
        

def find_ratio_one_document(token_label_lists: List[List[Tuple[str]]]) -> float:
    
    if len(token_label_lists) == 1: # just one completion
        return 1.0

    else: # 2 or more completions

        max_token = max([len(l) for l in token_label_lists])

        reference_list = token_label_lists[0]
        rest_lists = token_label_lists[1:]
        num_identical_tokens = 0

        for ref_token, ref_label in reference_list:
            if(all_completions_contain_labeling(rest_lists, ref_token, ref_label)):
                num_identical_tokens += 1

        return num_identical_tokens / max_token


def completion_contains_labeling(completion: List[Tuple[str]], reference_token: str, reference_label: str) -> bool:
    
    for rest_token, rest_label in completion:
        if rest_token == reference_token and rest_label == reference_label:
            return True
    
    return False


def all_completions_contain_labeling(completions: List[List[Tuple[str]]], reference_token: str, reference_label: str) -> bool:
    
    return all([completion_contains_labeling(completion, reference_token, reference_label) for completion in completions])


def documents_ratios(conn, document_names: List[Tuple[str]]) -> None:

    document_completion_ratio = {}
    
    for doc in document_names:

        DocumentID = find_document_id(conn, doc[0])
        CompletionIDs_list = find_completion_ids(conn, DocumentID)  # output: [(3,), (4,)]

        if(CompletionIDs_list == []):
            document_completion_ratio[doc[0]] = 'No Completion'
            continue

        token_label_lists = find_tokens_labels_one_document(conn, CompletionIDs_list)  
        # [[('admin', 'Role'), ('sends', 'Task'), ('mail', 'Business Object')], [('admin', 'Role'), ('sends', 'Task'), ('mail', 'Business Object')]]

        document_completion_ratio[doc[0]] = find_ratio_one_document(token_label_lists)

    print(document_completion_ratio)


def run(conn):

    c = conn.cursor()
    
    c.execute("SELECT Name FROM Document")
    document_names = c.fetchall()  # output: [('Model_Sahar.txt',), ('indeed_apply_for_job.txt',), ('wiley_peer_review.txt',)]
    
    documents_ratios(conn, document_names)