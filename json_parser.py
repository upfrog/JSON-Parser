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

To expand to new types, I must add new methods for matching and parsing
the types, and I must checks for those types to parse_value functions

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
        if content[i] == " " or content[i] == "\n": #Ignore spaces and newlines
            i += 1
        elif is_divider(content[i]): #Atomically add seperators
            tokenized.append(content[i])
            i += 1
        else: #Content should be added as a range of indices
            j = i + find_end(content[i:])
            tokenized.append(content[i:j])
            i = j

    return tokenized

'''
==========================================================
==================PARSING=================================
==========================================================
'''

'''
Matching and Parsing

The basic structure of my code is classify a token by it's data type, and then to
process it according to that classification.

Match functions are preceded by the match_ prefix, and return a boolean; True if the
input token matches the given type, and False if it does not.

Parse functions are more complicated, and handle the (often recursive) process of 
turning a token into a properly typed object, which can be added to the final dictionary.

Matching is mostly simple, and in many cases could in principle be handled by a 
single-line comparison, but I often find it more readable to give a given match
it's own dedicated method, even if it's just a wrapper for match_generic(), which is
itself a wrapper for a single line of code.

Unlike matching, parsing sometimes operates on more than a single token. This means that
parsing must keep track of it's index across many different levels of recurions. I 
solve this by having some parse methods return tuples, consisting of the parsed value, 
and the index of the next token to be parsed. Not all parse functions return a tuple;
this is inconsistent, but the tuple unpacking clutters up code.

Parsing methods are also where exceptions are thrown in case of malformed input.
'''


'''
A flexible matching tool for doing simple checks.
'''
def match_generic(token: str, target: str) -> bool:
    return token == target

'''
Checks that a name is correctly formatted: that it is surrounded by quotation  marks,
and that it is not an empty string.
'''
def match_name(token: str) -> str:
    return token[0] == "\"" and token[-1] == "\"" and len(token) > 2


def parse_name(token: str) -> str:
    if token[0] == "\"" and token[-1] == "\"" and len(token) > 2:
        return token[1:-1]
    else:
        raise Exception("Key " + token + " is incorrectly formatted")
    

def match_dict(token: str) -> bool:
    return match_generic(token, "{")

'''
Given the index of the first content token in a dictionary, parses that dictionary
and it's contents.
'''
def parse_dict(tokenized: list, i: int) -> tuple:
    
    new_dict = {}

    parsed_result = parse_entries(tokenized, (new_dict, i))
    new_dict = parsed_result[0]
    i = parsed_result[1]
    if match_generic(tokenized[i], "}"):
        i += 1

    return (new_dict, i)


def match_comma(token: str) -> bool:
    return match_generic(token, ",")


'''
Any content wrapped in quotation marks can be a String
'''
def match_string(token: str) -> bool:
    if token[0] == "\"" and token[-1] == "\"":
        return True
    

def parse_string(token: str) -> str:
    if token == "\"\"":
        return ""
    else:
        return token[1:-1]
    

def match_list(token) -> list:
    return match_generic(token, "[")
    

'''
Given the index of the first content token in a list, parses that list and it's contents.
'''
def parse_list(tokenized: list, i: int) -> tuple:
    new_list = []

    #if the list is empty
    if tokenized[i] == "]":
        return new_list

    #Given that the list has at least one entry, it can only be closed after an entry.
    while i < len(tokenized):
        parse_result = parse_value(tokenized, i)
        new_list.append(parse_result[0])
        i = parse_result[1]

        #Paired conditionals cover list ending, whether or not there is a trailing comma.
        if match_comma(tokenized[i]):
            i += 1
        if match_generic(tokenized[i], "]"):
            return (new_list, i+1)
        
    raise Exception("Error: list is not closed with a \"]\".") 


def match_bool(token: str) -> bool:
    return (token == "true" or token == "false")


def parse_bool(token: str) -> bool:
    if token == "true":
        return True
    elif token == "false":
        return False

'''
Initially I wanted to independently code this, but I decided that I was better off 
relying on Python's in-built type compatibility checking, rather than jury-rigging 
my own. Besides - isn't "ask forgiveness, not permission" a think in Pyhon style?
'''
def match_num(token: str) -> bool:
    try:
        int(token)
        return True
    except:
        try:
            float(token)
            return True
        except:
            return False
    
'''
Takes a string number as input, and returns it as an into or a float.

Can be handled through string analysis, but this seemed more reliable.
'''
def parse_num(token: str):
    try:
        return int(token) 
    except:
        try:
            return float(token)
        except:
            raise Exception(token + " cannot be parsed as a number")
    
'''
Takes a given value (not key) token, formed as a string, as input, and returns
it it's proper data type.

The order of the if-statements could be important, since a boolean "true" or "false"
could be read as a string - as could any number. This shouldn't matter, since my string
matching relies on the presence of quoation marks, which shouldn't be present in numbers
or booleans.
'''
def parse_value(tokenized: list, i: int):
    token = tokenized[i]
    value = None

    if match_num(token):
        value = parse_num(token)
        i += 1
    elif match_bool(token):
        value = parse_bool(token)
        i += 1     
    elif match_string(token):
        value = parse_string(token)
        i += 1
    #Lists and dicts involve parsing multiple values, so we pass the list of tokens
    elif match_list(token):
        parse_result = parse_list(tokenized, i+1)
        value = parse_result[0]
        i = parse_result[1]
    elif match_dict(token):
        parse_result = parse_dict(tokenized, i+1)
        value = parse_result[0]
        i = parse_result[1]
    else:
        raise Exception("Error: value associated with key \"" 
                        + token +"\" is invalid.")
    
    return (value, i)



'''
Parses all the entries at a given level of dictionary
'''
def parse_entries(tokenized: list, parsed: tuple) -> tuple:
    parsed_dict = parsed[0]
    i = parsed[1]
    
    while tokenized[i] != "}":
        #Checks for a name and ":"
        key = parse_name(tokenized[i])
        if not (match_generic(tokenized[i+1], ":")):
            raise Exception("Input is missing \":\" sepperating key and value.")
        i += 2 

        value_result = parse_value(tokenized, i)

        value = value_result[0]
        i = value_result[1]

        parsed_dict[key] = value

        #Paired conditionals cover dict ending, whether or not there is a trailing comma.
        if match_comma(tokenized[i]):
            i += 1
        if i >= len(tokenized):
            raise Exception("Dictionary is not closed with a \"}\".")
        
    return (parsed_dict, i)


def parse(tokenized: list) -> dict:
    if match_generic(tokenized[0], "{") == True:
        parsed = ({}, 1)
        return parse_entries(tokenized, parsed)
        

def parse_file(file_name: str) -> dict:
    #access the file and get contents

    with open(file_name) as file:
        content = file.read()

    tokenized = tokenize(content)
    print(tokenized)

    parsed = parse(tokenized)
    return(parsed[0])


def main():
    ap = argparse.ArgumentParser(description=(DESCRIPTION + f"\nBy: {YOUR_NAME_HERE}"))
    ap.add_argument('file_name', action='store', help='Name of the JSON file to read.')
    args = ap.parse_args()
    

    file_name = args.file_name
    local_dir = os.path.dirname(__file__)
    file_path = os.path.join(local_dir, file_name)

    dictionary = parse_file(file_path)

    #dictionary = parse_file("test_data/medium_test.json")

    print('DICTIONARY:')
    print(dictionary)


if __name__ == '__main__':
    main()