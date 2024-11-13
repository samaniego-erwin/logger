import logParser
import unittest

class TestLogParser(unittest.TestCase):
    def test_getProtocol(self):
        tests = [
            {
                "title": "Happy Path",
                "input_dstport": "23",
                "input_protocol": "tcp",
                "expected": "sv_P1"
             },
             {
                "title": "Tag Can Map To Multiple Port/Protocol Combo",
                "input_dstport": "25",
                "input_protocol": "tcp",
                "expected": "sv_P1"
             },
             {
                "title": "Case Insensitive Input",
                "input_dstport": "25",
                "input_protocol": "tCp",
                "expected": "sv_P1"
             },
             {
                "title": "No Associated Tag With Given Input",
                "input_dstport": "tcp",
                "input_protocol": "10000",
                "expected": None
            },
            {
                "title": "Empty Inputs",
                "input_dstport": "",
                "input_protocol": "",
                "expected": None
            }
        ]

        for test in tests:
            got = logParser.getTag(test["input_dstport"], test["input_protocol"])
            self.assertEqual(got, test["expected"], "Mismatched in testcase: " + test["title"])

    def test_getTag(self):
        tests = [
            {
                "title": "Happy Path",
                "input": "6",
                "expected": "tcp"
             },
             {
                "title": "Invalid Code",
                "input": "abc",
                "expected": None
             },
            {
                "title": "Empty Code",
                "input": "",
                "expected": None
            }
        ]

        for test in tests:
            got = logParser.getProtocol(test["input"])
            self.assertEqual(got, test["expected"], "Mismatched in testcase: " + test["title"])



if __name__ == '__main__':
    unittest.main()
        
