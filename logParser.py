import csv
# import timeit
# import time
from collections import defaultdict
from functools import cache


#WRITE TEST


# from https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
# dstport is in 6th column and protocol is in 7th (0-based index)
PORT = 6
PROTOCOL = 7

# csv file from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
PROTOCOL_NUMBERS_MAP = "logger/protocol-numbers-1.csv"
DECIMAL = "Decimal"
KEYWORD = "Keyword"

OUTPUTFILE = "logger/output.txt"

# flowLogParser will read the file passed to it
# and map each row to a tag based on a lookup table.
# It then writes to an output file and summarizes counts associated with tag and with port/protocol combo
def flowLogParser(filename):

    #these will track counts associated with tag and with port/protocol combo
    tagCounts = defaultdict(int)
    portAndProtocolCounts = defaultdict(int)

    # using "with" statement releases the resource automatically
    with open(filename, "r") as file:
        for line in file:
            fields = line.split()
            
            dstport = fields[PORT]
            protocol = getProtocol(fields[PROTOCOL])
            portAndProtocolCounts[dstport + "," + protocol] += 1

            tag = getTag(dstport, protocol)
            if tag is None:
                tagCounts["Untagged"] += 1
            else:
                tagCounts[tag] += 1

    # write to output count of matches for each tag and for each port/protocol combo
    writeOutput(tagCounts, "Tag Counts:\nTag,Count\n")
    writeOutput(portAndProtocolCounts, "Port/Protocol Combination Counts:\nPort, Protocol,Count\n")
    
    # with open(OUTPUTFILE, "a") as file:
    #     file.write("Tag Counts:\n")
    #     file.write("Tag,Count\n")
    #     keys = tagCounts.keys()
    #     for key in keys:
    #         file.write(key + "," + str(tagCounts[key]) + "\n")
    #     file.write("\n\n")

    #     file.write("Port/Protocol Combination Counts:\n")
    #     file.write("Port, Protocol,Count\n")
    #     keys = portAndProtocolCounts.keys()
    #     for key in keys:
    #         file.write(key + "," + str(portAndProtocolCounts[key]) + "\n")
    #     file.write("\n\n")
        


def writeOutput(summary, header):   
    with open(OUTPUTFILE, "a") as file: 
        file.write(header)
        keys = summary.keys()
        for key in keys:
            file.write(key + "," + str(summary[key]) + "\n")
        file.write("\n\n")
        

# add documenation
@cache        
def getTag(dstport, protocol):
    #no hardcode
    with open("logger/lookupTable.csv", "r") as file:
        reader = csv.DictReader(file)


        for row in reader:
            #no hard code
            #not case sensitive
            if row["dstport"] == dstport and row["protocol"].lower() == protocol.lower():
                return row["tag"]
    return None

# getProtocol takes in a number and returns the corresponding protocol keyword associated with it
def getProtocol(protocolNum):
    with open(PROTOCOL_NUMBERS_MAP, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[DECIMAL] == protocolNum:
                return row[KEYWORD].lower()
    return None




if __name__ == '__main__':
    #change this to args
    flowLogParser("logger/flowLog.txt")
    
    
    # flowLogParser("sampleText.txt")
    