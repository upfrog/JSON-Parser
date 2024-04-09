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

'''

def parse_s(tokenized: list, parsed: list, i: int) -> dict:
    c = tokenized[i]

    if c == "{":
        match{"{"}


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


'''
A more flexible matching tool for doing simple checks.

Because none of these will be directly added to the final dictionary, it does not
need to return the matched value.
'''
def match_generic(c: str, target: str) -> bool:
    if c == target:
        return True
    else:
        raise Exception("Error: Expected " + target + ", got " + c + ".")


def add(parsed: list, c: str) -> dict:
    pass

'''
def parse_content(tokenized: list, i: int):
    #is the content an int?

    #is the content a strin?

    #is the content a dict?
    #dostuff
    return (3, 8)
'''


'''
These functions are technically unnecesary, but I think it is clearer than directly using
match_generic().

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
    

'''
Identifies the type of value in a list, and parses it as appropriate

This is a poor solution. It is almost identical to parse_dict_value() - the only
difference is how i is incremented.

I hope that I'll have time to fix this, but it works.
'''
def parse_list_value(tokenized: list, i: int):
    token = tokenized[i]
    value = None

    if match_num(token):
        value = parse_num(token)
        i += 1
    #Check this after num; any number can be a string, but not vice versa     
    elif match_string(token):
        value = parse_string(token)
        i += 1
    #Lists and dicts involve parsing multiple values, so we pass the list of tokens
    elif match_list(token):
        parse_result = parse_list(tokenized, i+3)
        value = parse_result[0]
        i = parse_result[1]
    elif match_dict(token):
        parse_result = parse_dict(tokenized, i+3)
        value = parse_result[0]
        i = parse_result[1]
    else:
        raise Exception("Error: list value is invalid")
    
    return (value, i)
    

def parse_list(tokenized: list, i: int) -> list:
    new_list = []

    #if the list is empty
    if tokenized[i] == "]":
        return new_list

    #Given that the list has at least one entry, it can only be closed after an entry.
    while i < len(tokenized):
        parse_result = parse_list_value(tokenized, i)
        new_list.append(parse_result[0])
        i = parse_result[1]
        if match_comma(tokenized[i+1]):
            i += 2
        #only return the list if it's closed. If it never is, we throw an error.
        elif match_generic(tokenized[i+1], "]") :
            return new_list
    
    raise Exception("Error: list is not closed with a \"]\".") 


'''
Takes in the list of tokens, and a start location, then parses to the end of the dictionary.

'''
def parse_dict(tokenized: list, i: int) -> tuple:
    
    new_dict = {}
    parsed_result = parse_entries(tokenized, (new_dict, i))
    new_dict = parsed_result[0]
    i = parsed_result[1]
    match_generic(tokenized[i], "}")

    return (new_dict, i)

'''
Takes a string number as input, and returns it as an into or a float.

Might be better handled by try-catching conversions - I understand that 
"ask forgiveness, not permission" is pythonic.
'''
def parse_num(token: str):
    num = num[1:-1] #strip quotation marks
    parsed_num = None

    if num.contains("."):
        parsed_num = float(num)
    else:
        parsed_num = int(num)

    return parsed_num

'''
Relies on parse_num().

Initially I wanted to independently code this, to reduce my constraints for ordering
functions, but I decided that it was better to rely on Python's in-built type
compatibility checking, than jury-rigging my own.
'''
def match_num(token: str) -> bool:
    try:
        parse_num(token)
    except:
        return False
    else:
        return True

'''
PROBLEM: This increments i as if it's still parsing dict members
'''
def parse_dict_value(tokenized: list, i: int):
    token = tokenized[i]
    value = None

    if match_num(token):
        value = parse_num(token)
        i += 3
    #Check this after num; any number can be a string, but not vice versa     
    elif match_string(token):
        value = parse_string(token)
        i += 3
    #Lists and dicts involve parsing multiple values, so we pass the list of tokens
    elif match_list(token):
        parse_result = parse_list(tokenized, i+3)
        value = parse_result[0]
        i = parse_result[1]
    elif match_dict(token):
        parse_result = parse_dict(tokenized, i+3)
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
    return token

'''
Parses all the entries at a given level of dictionary
'''
def parse_entries(tokenized: list, parsed: tuple) -> tuple:
    parsed_dict = parsed[0]
    i = parsed[1]

    #Find the end of the current dict, and parse to it. Each loop parses a key-value pair.
    try: 
        parse_extent = tokenized[i:].index("}")
    except:
        raise Exception("Error: Dictionary is not closed")
    else:
        while i < parse_extent:
            key = match_name(tokenized[i])
            match_generic(tokenized[i+1], ":")
            i += 2 #sets i to the index of the key's value
            value = None

            value_result = parse_dict_value(tokenized, i)

            value = value_result[0]
            i = value_result[1]
            match_comma(tokenized[i])

            parsed_dict[key] = value

    return (parsed_dict, i)


    '''
    #Check that a top-level dictionary is being made properly
    #if match_generic(tokenized[0], "{") == True:

    
        #should it be until i = the index of the next } instead?    
        while i < len(tokenized):
            #If it's a name-value pair
            
            key = match_name(tokenized[i])
            match_generic(tokenized[i+1], ":")
            parse_result = parse_content(tokenized[], i+2)
            
            val = parse_result[0]
            i += parse_result[1]

            parsed[key] = val
    else:
        raise Exception("Error: Dictionary is missing an opening \"{\".")
    
    if match_generic(tokenized[i], "}"):
        return parsed
    else:
        raise Exception("Dictionary is missing a closing \"}\".")
        '''
    
    
    

    #Make a parse_first method to handle making a dictionary with no name
    
    '''c = tokenized[i]

    if is_name(c) == True:
        #add name
        #add colon???
        #add value OR container
    else if is_container(c) == True:
        pass
'''

    


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


def parse(tokenized: list) -> dict:
    if match_generic(tokenized[0], "{") == True:
        parsed = ({}, 1)
        return parse_entries(tokenized, parsed)
        






def parse_file(file_name: str) -> dict:
    #content = ""
    #access the file and get contents
    with open(file_name) as file:
        content = file.read()

    tokenized = tokenize(content)
    print(tokenized)

    #parsed = {}
    parsed = parse(tokenized)
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

'''
TODO:
Figure out how to handle matching the list (probably should do the same
thing you do for dicts, just for consistency. COnsider implementing a
2-sided match function?)
Implement match_list()
Implement parse_list()
Test!
Extend!

'''