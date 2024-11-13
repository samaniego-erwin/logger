import logParser
import unittest

class TestLogParser(unittest.TestCase):
    def test_getProtocol(self):
        result = logParser.getProtocol("6")
        self.assertEqual(result, "tcp")

if __name__ == '__main__':
    unittest.main()
        
