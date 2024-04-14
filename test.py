'''
This is somewhat overpowered for the task at hand, but I wanted to learn a more scaleable way of
organizing test.
'''
from json_parser import parse_file

import unittest
import json
import os


class TestParser(unittest.TestCase):
    
    def test_stuff(self):
        file_name = "test_data\\easy_test.json"
        
        local_dir = os.path.dirname(__file__)
        print(local_dir)
        file_path = os.path.join(local_dir, file_name)
        #dictionary = parse_file(file_path)
        print(file_path)
        with open(file_path) as file:
            content = file.read()
        true_dict = json.loads(content)

        print(true_dict)


        
        
        
        
        
        
        
        
        
        
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