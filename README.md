# logger

logParser reads the flow log data file passed to it, maps each row to a tag based on a lookup table,
summarizes counts associated with each tag and port/protocol combination, and writes the data to an output file.

This tool supports the default log format and only version 2. The following reference was used: [AWS Flow Log Records Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html).  

The lookup table `lookupTable.csv` is based on the example provided. The protocol number mapping file, `protocol-numbers-1.csv`, is based on information from [IANA Protocol Numbers](http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) as referenced in the Flow Log Records documentation.

The output is written to `output.txt`. If the file already exists, the output is appended.

**Usage:** python3 logParser.py -f "path-to-log-file"

**Sample run:**
```
er@ers-MacBook-Air-2 Python % python3 logger/logParser.py -f "logger/flowLog.txt"
```

Use `-h` for help
```
er@ers-MacBook-Air-2 Python % python3 logger/logParser.py -h                     
usage: logParser.py [-h] -f FILE

Reads a flow log data and maps each row to a tag based on lookup table

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the flow log file
```



## TESTS
`lookupTable_big.csv` was used to test large port-protocol-tag mappings. A comparison between cached and non-cached versions was performed using a timer. 



Execute `test_logParser.py` to run unit tests 
```
er@ers-MacBook-Air-2 Python % python3 logger/test_logParser.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```


Here is an example of a failed test. The `expected` value in the unit test was modified to generate a mismatch. 
```
er@ers-MacBook-Air-2 Python % python3 logger/test_logParser.py
F.
======================================================================
FAIL: test_getProtocol (__main__.TestLogParser.test_getProtocol)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/er/VisualStudioCode/Python/logger/test_logParser.py", line 41, in test_getProtocol
    self.assertEqual(got, test["expected"], "Mismatched in testcase: " + test["title"])
AssertionError: 'sv_P1' != 'sv_P100'
- sv_P1
+ sv_P100
?      ++
 : Mismatched in testcase: Happy Path

----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=1)
```
