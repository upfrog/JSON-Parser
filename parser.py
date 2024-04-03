#!/usr/bin/python3
DESCRIPTION = '''
A homebrew JSON parser which extends standard JSON with sets and complex numbers.
'''

import argparse
import os.path

YOUR_NAME_HERE = "Stephen Rout" 



'''
GRAMMAR:



'''


'''
A function to check if a given character should be tokenized individually.

This uses a dictionary for O(1) lookup speed.
'''
def is_divider(char: str) -> bool:
    single_char_dict = {
        "{" : True,
        "}" : True,
        "(" : True,
        ")" : True,
        "[" : True,
        "]" : True,
        ":" : True,
        "," : True
    }

    if char in single_char_dict:
        return True
    else:
        return False
    
'''
A function to check if a given entry is a number.

This uses a dictionary for O(1) lookup speed.

The relevance of ".", "-", and "+" prevent this from being a simple type check.
'''
def is_number(char: str) -> bool:
    num_dict = {
        "1" : True,
        "2" : True,
        "3" : True,
        "4" : True,
        "4" : True,
        "5" : True,
        "6" : True,
        "7" : True,
        "8" : True,
        "9" : True,
        "0" : True,
        "." : True,
        "-" : True,
        "+" : True
    }

    if char in num_dict:
        return True
    else:
        return False

    

'''
Returns the index which tokenize should split to.

This only checks for numbers, strings, and booleans.

For quotation marks we know the end of the split once we reach it, but for
the other types, we only know the end index once we have passed it.
'''
def find_end(content: str) -> int:
    if (content[0] == "\""):
        return content[1:].find("\"") + 2 #split should include the quote
    elif is_number(content[0]):
        j = 0
        while j < len(content):
            if content[j]  == "," or content[j] == "}" or content[j] == "]" or content[j] == "\n":
                return j
            else:
                j += 1
        #If we reach here, then the input is ill-formed
    elif content[0] == "t": #True
        return 4
    elif content[0] == "f": #False
        return 5
    else:
        raise RuntimeError
        
        
        

'''

3 cases
-true/false
-quotation marks
number
'''


def tokenize(content: str) -> list:
    i = 0
    tokenized = []
    while (i < len(content)):
        #print(i)
        #print(tokenized)
        if content[i] == " " or content[i] == "\n": #Ignore spaces and newlines
            i += 1
            #print(1)
        elif is_divider(content[i]): #Atomically add seperators
            tokenized.append(content[i])
            i += 1
            #print(2)
        else: #Content should be added as a range of indices
            j = i + find_end(content[i:])
            tokenized.append(content[i:j])
            i = j
            #print(3)

    return tokenized


def parse_file(file_name: str) -> dict:
    #content = ""
    #access the file and get contents
    with open(file_name) as file:
        content = file.read()

    print(tokenize(content))


    



    #print(content)
    #pass
        



'''
Tokenization methods:
    - have a single index variable to act as a pointer. It will either point to something that 
    is a single-character token, or it will point to an indicator that we must tokenize a range of
    characters. If the latter, get a second pointer, and explore from there to find the end
    -Aggressively use methods strip and split

'''






#py parser.py test_data/$TEST_FILE_NAME.json

def main():
    ap = argparse.ArgumentParser(description=(DESCRIPTION + f"\nBy: {YOUR_NAME_HERE}"))
    ap.add_argument('file_name', action='store', help='Name of the JSON file to read.')
    args = ap.parse_args()

    file_name = args.file_name
    local_dir = os.path.dirname(__file__)
    file_path = os.path.join(local_dir, file_name)

    dictionary = parse_file(file_path)

    print('DICTIONARY:')
    print(dictionary)


if __name__ == '__main__':
    main()