'''
These tests are not great, as there is a great deal of boilerplate, and
Python's inbuilt JSON module cannot handle many of my test files, 
meaning that my tests are quite short on rigor.

Files which are beyond Python's JSON parser's capability are printed.
While visual inspection is a poor way to verify the tests, the program
will at least crash if the dictionary was built improperly.

This would also benefit from some added tests for exceptions.
'''
from json_parser import parse_file
import unittest
import json
import os

class TestParser(unittest.TestCase):

    def setUp(self):
        self.wd = os.path.dirname(__file__)
    
    def test_basics(self):
        '''Tests files which Python's JSON module can convert.
        '''
        TEST_DATA_LOCATION =  "test_data/base_tests"
        test_directory = os.path.join(self.wd, TEST_DATA_LOCATION)
        test_files = os.listdir(TEST_DATA_LOCATION)

        for test in test_files:
            test_path = os.path.join(test_directory, test)
            
            with open(test_path) as input:
                content = input.read()
                unknown_parse = parse_file(test_path)
                known_parse = json.loads(content)
                self.assertEqual(unknown_parse, known_parse)

    def test_sets(self):
        '''Tests files containing the set extension.
        '''
        TEST_DATA_LOCATION =  "test_data/set_tests"
        test_directory = os.path.join(self.wd, TEST_DATA_LOCATION)
        test_files = os.listdir(TEST_DATA_LOCATION)

        for test in test_files:
            test_path = os.path.join(test_directory, test)
            
            with open(test_path) as input:
                unknown_parse = parse_file(test_path)
                print(unknown_parse)
                print("===========================")
            
    def test_complex(self):
        '''Tests files containing the complex number extension.
        '''
        TEST_DATA_LOCATION =  "test_data/complex_tests"
        test_directory = os.path.join(self.wd, TEST_DATA_LOCATION)
        test_files = os.listdir(TEST_DATA_LOCATION)

        for test in test_files:
            test_path = os.path.join(test_directory, test)
            
            with open(test_path) as input:
                unknown_parse = parse_file(test_path)
                print(unknown_parse)
                print("===========================")

    def test_complex_sets(self):
        '''Tests files containing the complex set extension.
        '''
        TEST_DATA_LOCATION =  "test_data/complex_set_tests"
        test_directory = os.path.join(self.wd, TEST_DATA_LOCATION)
        test_files = os.listdir(TEST_DATA_LOCATION)

        for test in test_files:
            test_path = os.path.join(test_directory, test)
            
            with open(test_path) as input:
                unknown_parse = parse_file(test_path)
                print(unknown_parse)
                print("===========================")    
         

if __name__ == '__main__':
    unittest.main()