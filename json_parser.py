#!/usr/bin/python3
import copy

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

'''
Checks that a name is correctly formatted.

Do I need to check for additional quotation marks in the name?

'''
def match_name(c: str) -> str:
    #Checks that name is surrounded by "", annd that it has content
    if c[0] == "\"" and c[-1] == "\"" and len(c) > 2:
        return c[1:-1]
    else:
        raise Exception("Error: Key " + c + " is incorrectly formatted")

'''
A more flexible matching tool for doing simple checks.
'''
def match_generic(c: str, target: str) -> bool:
    if c == target:
        return True
    else:
        return False


'''
Some of these matching functions are technically unnecesary, but I think they
are clearer than directly using match_generic() in all cases.
'''
def match_dict(token: str) -> bool:
    return match_generic(token, "{")


def match_comma(token: str) -> bool:
    return match_generic(token, ",")


'''
Any content wrapped in quotation marks can be a String
'''
def match_string(token: str) -> str:
    if token[0] == "\"" and token[-1] == "\"":
        return True
    

def match_list(token) -> list:
    if match_generic(token, "["):
        return True
    

def match_bool(token: str) -> bool:
    return (token == "true" or token == "false")


def parse_bool(token: str) -> bool:
    if token == "true":
        return True
    elif token == "false":
        return False
    

def parse_list(tokenized: list, i: int) -> list:
    new_list = []

    #if the list is empty
    if tokenized[i] == "]":
        return new_list

    #Given that the list has at least one entry, it can only be closed after an entry.
    while i < len(tokenized):
        parse_result = parse_value(tokenized, i)
        new_list.append(parse_result[0])
        i = parse_result[1]

        if match_comma(tokenized[i]):
            i += 1
        #Paired conditionals cover list ending, whether or not there is a trailing comma.
        if match_generic(tokenized[i], "]"):
            return (new_list, i+1)
        

            
    
    raise Exception("Error: list is not closed with a \"]\".") 

'''
Takes in the list of tokens, and a start location, then parses to the end of the dictionary.

'''
def parse_dict(tokenized: list, i: int) -> tuple:
    
    new_dict = {}
    print("First dict key: " + tokenized[i])
    print("in parse_dict, i = " + str(i))
    print("in parse_dict, tokenized[i] = " + tokenized[i])

    parsed_result = parse_entries(tokenized, (new_dict, i))
    new_dict = parsed_result[0]
    i = parsed_result[1]
    if match_generic(tokenized[i], "}"):
        i += 1

    return (new_dict, i)

'''
Takes a string number as input, and returns it as an into or a float.

Might be better handled by try-catching conversions - I understand that 
"ask forgiveness, not permission" is pythonic.
'''
def parse_num(token: str):
    num = token #num[1:-1] #strip quotation marks
    parsed_num = None

    try:
        if num.find(".") != -1:
            parsed_num = float(num)
        else:
            parsed_num = int(num)
    except:
        raise Exception("Not a valid number.")
    else:
        return parsed_num

'''
Relies on parse_num().

Initially I wanted to independently code this, to reduce my constraints for ordering
functions, but I decided that it was better to rely on Python's in-built type
compatibility checking, than jury-rigging my own.
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
    

def parse_value(tokenized: list, i: int):
    token = tokenized[i]
    value = None

    #print(type(int(token)))
    if match_num(token):
        value = parse_num(token)
        i += 1
    #Check this after num; any number can be a string, but not vice versa
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
Not much to do here, but the wrapper keeps consistency
'''
def parse_string(token: str) -> str:
    if token == "\"\"":
        return "1"
    else:
        return token[1:-1]

'''
Parses all the entries at a given level of dictionary
'''
def parse_entries(tokenized: list, parsed: tuple) -> tuple:
    print("===============")
    parsed_dict = parsed[0]
    i = copy.deepcopy(parsed[1])
    print("in parse_entries, i = " + str(i))
    
    while tokenized[i] != "}":
        print(parsed_dict)
        print("In While: " + str(i))
        print("Token: " + tokenized[i])
        key = match_name(tokenized[i])
        match_generic(tokenized[i+1], ":")
        i += 2 #sets i to the index of the key's value
        value = None

        value_result = parse_value(tokenized, i)

        value = value_result[0]
        i = value_result[1]
        parsed_dict[key] = value

        if match_comma(tokenized[i]):
            i += 1
            
        elif match_generic(tokenized[i], "}"):
            pass
        else:
            raise Exception("Improper formatting!")

            
            
            #print("yo!")

    return (parsed_dict, i)


def parse(tokenized: list) -> dict:
    if match_generic(tokenized[0], "{") == True:
        parsed = ({}, 1)
        return parse_entries(tokenized, parsed)
        

def parse_file(file_name: str) -> dict:
    #content = ""
    #access the file and get contents
    print(file_name)
    with open(file_name) as file:
        content = file.read()

    tokenized = tokenize(content)
    print(tokenized)

    #parsed = {}
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