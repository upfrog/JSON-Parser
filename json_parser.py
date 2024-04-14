

DESCRIPTION = '''
A homebrew JSON parser which extends standard JSON with sets and complex numbers.
'''

import argparse
import os.path

YOUR_NAME_HERE = "Stephen Rout" 

'''
GRAMMAR:

This is quite rough. It was useful for organizing my thoughts, especially since 
it was illustrative for my problem statement and decomposision, but it is a 
long ways from being mathematically rigorous.

DRAFT IV++:

Start/dict      S -> {C}
Content         C -> str : D
Data            D -> (L||S||SET||str||num||bool) E
List            L -> [D]
Set           SET -> {num||str||bool||complex}

Not 100% corrent; data within lists has different rules for commas.

To expand to new types, I must add new methods for matching and parsing
the types, and I must checks for those types to parse_value functions


EXTENSION:

Data can now yield complex numbers or sets,

SET -> {num||str||bool||complex}
'''

'''
==========================================================
==================TOKENIZING==============================
==========================================================
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
Checks if a given entry is a number, using a dictionary for O(1) lookup speed.

There is probably a way to do this with python type conversion, but in this case
this seemed simplest.
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

For quotation marks, we know the end of the split once we reach it, but for
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


def match_colon(token: str) -> bool:
    return token == ":"

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

Represents S from the grammar
'''
def parse_dict(tokenized: list, i: int) -> tuple:
    
    new_dict = {}

    parsed_result = parse_entries(tokenized, new_dict, i)
    new_dict = parsed_result[0]
    i = parsed_result[1]
    if match_generic(tokenized[i], "}"):
        i += 1

    return (new_dict, i)


def match_comma(token: str) -> bool:
    return match_generic(token, ",")



'''
Unlike the other types, a set requires two tokens of look-ahead: one to check that
the value is of the allowed types (int, float, boolean, string), and a second to to
check that the token after the value is not a colon, which would indicate a key-value
pair.
'''
def match_set(tokenized: list, i: int) -> bool:
    if (match_generic(tokenized[i], "{")
        and match_primitive(tokenized[i+1])
        and not match_colon(tokenized[i+2])):
        return True
    else:
        return False


'''
Because sets cannot contain multi-token structures, stuff

The structure of the code is extremely similar to parse_list(). I wonder if there is
some way to use this similarity to economize on code?

Represent Set from the grammar.
'''
def parse_set(tokenized: list, i: int) -> tuple:
    new_set = set()

    if tokenized[i] == ")":
        return new_set
    
    while i < len(tokenized):
        if not match_primitive(tokenized[i]):
            raise Exception("Set can only contain Python primitive types.")
        
        parse_result = parse_value(tokenized, i)
        new_set.add(parse_result[0])
        i += 1

        if match_comma(tokenized[i]):
            i += 1
        if match_generic(tokenized[i], "}"):
            return (new_set, i+1)

    raise Exception("Set is not closed with a \"]\".") 


'''
Any content wrapped in quotation marks can be a String.
'''
def match_string(token: str) -> bool:
    if token[0] == "\"" and token[-1] == "\"":
        return True
    
'''
Represents String from the grammar.
'''
def parse_string(token: str) -> str:
    if token == "\"\"":
        return ""
    else:
        return token[1:-1]
    

def match_list(token) -> list:
    return match_generic(token, "[")
    
'''
Given the index of the first content token in a list, parses that list and it's contents.

Represents L from the grammar.
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
    

def match_complex(token: str) -> bool:
    if token[-1] == "i":
        return True

'''
Start at the right (or maybe index 1)
go left until you find a non-number, non-decimal
    -if it's + || -, this is the end of the first number
    -if it's e, go ahead one, then keep going right until you find + || -
    that point, to the left, is your second term

    Nope!!! :33
'''
def parse_complex(token: str) -> complex:
    if token.find(" ") != -1:
        raise Exception("Imaginary numbers must not contain spaces")
    '''
    token[:-1].append("j")
    print(complex(token))
    '''
    return complex(token.replace("i","j"))

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
    

def match_primitive(token: str) -> bool:
    if (match_bool(token)
        or match_string(token)
        or match_num(token)
        or match_complex(token)):
        return True
    else:
        return False       

'''
Takes a given value (not key) token, formed as a string, as input, and returns
it it's proper data type.

The order of the if-statements could be important, since a boolean "true" or "false"
could be read as a string - as could any number. This shouldn't matter, since my string
matching relies on the presence of quoation marks, which shouldn't be present in numbers
or booleans.

Represents D from the grammar
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
    elif match_complex(token):
        value = parse_complex(token)
        i += 1     
    elif match_string(token):
        value = parse_string(token)
        i += 1
    #Lists, sets, and dicts involve parsing multiple values, so we pass the list of tokens
    elif match_set(tokenized, i):
        parse_result = parse_set(tokenized, i+1)
        value = parse_result[0]
        i = parse_result[1]
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
Parses all the entries at a given level of dictionary.
'''
def parse_entries(tokenized: list, parsed: dict, i: int) -> tuple:
    while tokenized[i] != "}":
        #Checks for a name and ":"
        key = parse_name(tokenized[i])
        if not match_colon(tokenized[i+1]):
            raise Exception("Input is missing \":\" sepperating key and value.")
        i += 2 

        parse_result = parse_value(tokenized, i)

        value = parse_result[0]
        i = parse_result[1]

        parsed[key] = value

        #Paired conditionals cover dict ending, whether or not there is a trailing comma.
        if match_comma(tokenized[i]):
            i += 1
        if i >= len(tokenized):
            raise Exception("Dictionary is not closed with a \"}\".")
        
    return (parsed, i)

'''
For convenience, we make the top-level dictionary here, and pass it into the rest of the
code.
'''
def parse_file(file_name: str) -> dict:
    with open(file_name) as file:
        content = file.read()

    tokenized = tokenize(content)
    #print(tokenized)
    
    if match_generic(tokenized[0], "{") == True:
        return parse_entries(tokenized, {}, 1)[0]
    else:
        raise Exception("Input does not start with a \"{\".")


def run_tests(test_files: list) -> str:
    TEST_DATA_LOCATION = "test_data"
    for test in test_files:
        try:
            path = os.path.join(TEST_DATA_LOCATION, test)
            print(parse_file(path))
            print("\n\n=====================================================\n\n")
        except:
            raise Exception("Failed on file " + test)

'''
Proccesses command line input, and prints the final product.

This has two modes: "command line" and "mass test". The former requires a command line
parameter, consisting of thena me of the input file. The latter will instead run the
parser on all files in the designated directory - which directory is hardcoded in
run_tests() as TEST_DATA_LOCATION.
'''
def main():
    mode = "command line"

    if mode == "command line":
        ap = argparse.ArgumentParser(description=(DESCRIPTION + f"\nBy: {YOUR_NAME_HERE}"))
        ap.add_argument('file_name', action='store', help='Name of the JSON file to read.')
        args = ap.parse_args()
        
        file_name = args.file_name
        local_dir = os.path.dirname(__file__)
        file_path = os.path.join(local_dir, file_name)

        dictionary = parse_file(file_path)

        print('DICTIONARY:')
        print(dictionary)

    elif mode == "mass test":
        dir_list = os.listdir("test_data/")
        run_tests(dir_list)


if __name__ == '__main__':
    main()