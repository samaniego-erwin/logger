import csv
import argparse
from collections import defaultdict
from functools import cache

# from https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
# dstport is in 6th column and protocol is in 7th (0-based index)
PORTFIELD = 6
PROTOCOLFIELD = 7

# csv file from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
PROTOCOL_NUMBERS_MAP = "logger/protocol-numbers-1.csv"
DECIMAL = "Decimal"
KEYWORD = "Keyword"

DST = "dstport"
PROTOCOL = "protocol"
TAG = "tag"

OUTPUTFILE = "logger/output.txt"
LOOKUPTABLE = "logger/lookupTable.csv"

# flowLogParser will read the file passed to it.
# It maps each row to a tag based on a lookup table.
# It summarizes counts associated with each tag and port/protocol combo, and writes the data to an output file
def flowLogParser(filename):

    #these will track counts associated with tag and with port/protocol combo
    tagCounts = defaultdict(int)
    portAndProtocolCounts = defaultdict(int)

    # using "with" statement releases the resource automatically
    with open(filename, "r") as file:
        for line in file:
            fields = line.split()
            
            dstport = fields[PORTFIELD]
            protocol = getProtocol(fields[PROTOCOLFIELD])
            portAndProtocolCounts[dstport + "," + protocol] += 1

            tag = getTag(dstport, protocol)
            if tag is None:
                tagCounts["Untagged"] += 1
            else:
                tagCounts[tag] += 1

    # write count of matches for each tag and for each port/protocol combo to output
    writeOutput(tagCounts, "Tag Counts:\nTag,Count\n")
    writeOutput(portAndProtocolCounts, "Port/Protocol Combination Counts:\nPort, Protocol,Count\n")
    

# writeOutput appends new summary counts when program is executed
def writeOutput(summary, header):   
    with open(OUTPUTFILE, "a") as file: 
        file.write(header)
        keys = summary.keys()
        for key in keys:
            file.write(key + "," + str(summary[key]) + "\n")
        file.write("\n\n")
        

# getTag returns tag associated with the dstport + protocol passed to this function
# cache result from this function with @cache decorator
@cache        
def getTag(dstport, protocol):
    with open(LOOKUPTABLE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[DST] == dstport and row[PROTOCOL].lower() == protocol.lower():
                return row[TAG]
    return None


# getProtocol takes in a number and returns the corresponding protocol keyword associated with it
# If there is no match, None is returned
def getProtocol(protocolNum):
    with open(PROTOCOL_NUMBERS_MAP, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[DECIMAL] == protocolNum:
                return row[KEYWORD].lower()
    return None


def main():
    parser = argparse.ArgumentParser(description="Reads a flow log data and maps each row to a tag based on lookup table")
    parser.add_argument("-f", "--file", help="Path to the flow log file", required=True)

    try:
        args = parser.parse_args()
        flowLogParser(args.file)
    except argparse.ArgumentError as e:
        print(e)
        parser.print_help()
        exit(1)

    
if __name__ == '__main__':
    main()
    