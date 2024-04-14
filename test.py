'''
This is somewhat overpowered for the task at hand, but I wanted to learn a more scaleable way of
organizing test.


My ability to easily test this is severely
'''
from json_parser import parse_file

import unittest
import json
import os
import sys


class TestParser(unittest.TestCase):
    
    def test_stuff(self):
        test_files = os.listdir("test_data/base_tests")
        TEST_DATA_LOCATION =  "test_data/base_tests"
        

    

        for test in test_files:
            try:
                cur_directory = os.path.dirname(__file__)
                test_path = os.path.join(TEST_DATA_LOCATION, test)
                print(cur_directory)
                print(test_path)


                test_path = os.path.join(cur_directory,test_path)
                print(test_path)
                
                with open(str(test_path)) as input:
                    content = input.read()
                    unknown_parse = parse_file(str(test_path))
                    known_parse = json.loads(content)

                #self.assertEqual(unknown_parse, known_parse)
                print("\n\n=====================================================\n\n")
            except:
                raise Exception("Failed on file " + test)
        

        
        
        
        
        
        
        
        
        
        
        '''
        target = __import__("json_parser.py")
        sum = target.parse_file

        FILE_PATH = '/test_data/easy_test.json'
        "../src/json_parser.parse_file(FILE_PATH)"
        json_parser.sum(FILE_PATH)
        '''

        
        '''correct_dict = []
        

        with open(FILE_PATH, "r") as file:
            correct_dict = json.load(file)

        self.assertEqual(correct_dict, "../src/json_parser.py")'''

   

if __name__ == '__main__':
    unittest.main()