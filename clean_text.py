
import spacy_udpipe
import argparse
import os
# spacy_udpipe.download("en")

    
def cleaning(raw_text: str) -> str:

    # list of deleted character
    del_char_list = ['º', '±', '°', '§', '¦', '¥', '¤', '£', '¢', '¡', '~', '|', 'ª', '©', '¬', 'ª', '®', '¯', '²',
                 '³', 'µ', '¶', '·', '¹', '¸', '†', '‡', 'ˆ', '‰', '•', '˜', '¯', '·', '¸'] 

    # dictionary of characters that need to be changed to another character
    change_char_dict = {'`':'\'', '´':'\'', '¿':'?', '«':'"', '»':'"', "¼":'1/4', "½":'1/2', "¾":'3/4', "×":"*", "÷":"/", '„':'"', '‹':'"', 
                           '‘':'\'', '’':'\'', '“':'"', '”':'"', '–':'-', '—':'-', '¨':'"'}
    
    char_list = list(raw_text)

    for index, char in enumerate(char_list):
        if char in del_char_list:
            char_list[index] = ''
        elif char in change_char_dict.keys():
            char_list[index] = change_char_dict[char]

    clean_text = "".join(char_list)
    
    return clean_text


def run(conn):

    parser = argparse.ArgumentParser("Subprogram - clean the raw text")
    parser.add_argument("action")
    parser.add_argument("raw_text")
    parser.add_argument("clean_text")

    args = parser.parse_args()

    try:
        with open(args.raw_text, 'r+',encoding='utf8') as file:
            raw_text = file.read()
            
        # Process of cleaning text 
        clean_text = cleaning(raw_text)

        # Add to file
        with open(args.clean_text, 'w', encoding='utf8') as file_new:
            file_new.write(clean_text)

    except FileNotFoundError:
        print("File not found !! ")



