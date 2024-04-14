            cur_directory = os.path.dirname(__file__)
            test_path = os.path.join(TEST_DATA_LOCATION, test)



            test_path = os.path.join(cur_directory,test_path)

            
            with open(str(test_path)) as input:
                content = input.read()
                unknown_parse = parse_file(str(test_path))
                known_parse = json.loads(content)

            self.assertEqual(unknown_parse, known_parse)
