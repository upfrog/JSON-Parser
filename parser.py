#!/usr/bin/python3
DESCRIPTION = '''
A homebrew JSON parser which extends standard JSON with sets and complex numbers.
'''

import argparse
import os.path

YOUR_NAME_HERE = "Stephen Rout" 



'''
GRAMMAR:

DRAFT IV:

Start/dict      S -> {C}
Content         C -> str : D
Data            D -> (L||S||str||num) E
List            L -> [D]
End             E -> (,D)|| , || episol

Not 100% corrent; data within lists has different rules for commas.


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



def parse_s(tokenized: list, parsed: list, i: int) -> dict:
    c = tokenized[i]

    if c == "{":
        match{"{"}

'''
def match(cur_token: str, target: str) -> bool:
    if cur_token == target:
        return True
'''


'''
Checks that a name is correctly formatted.

Do I need to check for additional quotation marks in the name?

'''
def match_name(c: str) -> str:

    #Checks that name is surrounded by "", annd that it has content
    if c[0] == "\"" and c[-1] == "\"" and len(c) > 2:
        return c
    else:
        raise Exception("Error: Key is incorrectly formatted")


def match_generic(c: str, target: str) -> str:
    if c == target:
        return c
    else:
        raise Exception("Error: Expected " + target + ", got " + c + ".")


def add(parsed: list, c: str) -> dict:
    pass


def parse_val(tokenized: list):

    #dostuff
    return (val, 8)


def parse(tokenized: list, parsed: list, i: int) -> dict:
    while i < len(tokenized):
        #If it's a name-value pair
        
        key = match_name(tokenized[i])
        match_generic(tokenized[i+1], ":")
        parse_result = parse_val(tokenized[i+2])
        
        val = parse_result[0]
        i += parse_result[1]

        parsed[key] = val
    
    
    
    
    
    '''c = tokenized[i]

    if is_name(c) == True:
        #add name
        #add colon???
        #add value OR container
    else if is_container(c) == True:
        pass
'''







    return parsed


'''
parse_A = name (string?)
    NAME CONTENT

    CONTENT -> CONTAINER OR STRING OR NUM

    for STRING or NUM, check if the next non-comma char is container closer

parse_b = container (list or dict) OR val 
parse_c = num
parse_d = ","
 

Fundamentally, this is about reading every single character in the input. With each character, we do one of two things: create
predictions about what future characters will be, or confirm past predictions. We must never predict wrong, which is why it's 
important to cover every single input character.

If we come across a colon, we know that the next token should NOT be a close brace, but it can be essentially anything else (can it 
be an a single comma?). So we parse the next piece knowing, knowing that it will be one of a set of things - lets call it data. Data
can take on many forms. We do not know which form it will take on, but we know that it will take on one of these forms. So our data
method must be able to handle any of these forms. It will take the next token, and it will determine the type of data. .

'''


def parse_dict(tokenized: list, parsed: dict, i: int) -> dict:
    dict = {}






def parse_file(file_name: str) -> dict:
    #content = ""
    #access the file and get contents
    with open(file_name) as file:
        content = file.read()

    tokenized = tokenize(content)
    print(tokenized)

    parsed = {}
    parsed = parse(tokenized[1:], parsed, 0)
    print(parsed)






'''
TOOD:
    - Figure out grammar
    - Implement grammar
    - Clean code - be sure to add some more failure handling!

    
need 2-token look-ahead (see attribtue name, look past ":", see folling token)
    -if [       -> list
    -if string, -> string
    -f num      -> num


If the first symbol is:
    -"STRING"   -> (Preapre to) Add string as name
    -

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