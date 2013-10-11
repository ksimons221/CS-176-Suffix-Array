import sys 
from generateSuffixArray import createSuffixArray
from generateBWTEncoding import *
from generateBWTDecoding import decodeBWT

def writeToFileWithBreaks(anFile, aStr):
    counter = 0
    while counter < len(aStr):
        anFile.write(aStr[counter: (counter +80)] + '\n')
        counter += 80

def stripAwayNewLines(inputFile):
    allLines = ""
    count = 0
    for line in inputFile:
        if count == 1:
            line = line.rstrip('\n')
            allLines = allLines + line
        count = 1
    allLines = list(allLines)
    return allLines


if len(sys.argv) != 4:
    print "Wrong number of arguments. Please provide a flag, and input file, and an output file"
    exit(1)

flag = sys.argv[1]
inputFileName = sys.argv[2]
outputFileName = sys.argv[3]

inputFile = None


if flag == "-bwt":
    try:
        inputFile = open(inputFileName, 'r')
    except IOError:
        print 'The input file does not exist to read'
        exit(1)
    allLines = stripAwayNewLines(inputFile)
    arr = createSuffixArray(allLines)
    t = encodeBWT(allLines, arr)
    outputFile = open(outputFileName, 'w')
    outputFile.write('>BWT\n')
    writeToFileWithBreaks(outputFile, t)
    outputFile.close()
    inputFile.close()

elif flag == "-ibwt":
    try:
        inputFile = open(inputFileName, 'r')
    except IOError:
        print 'The input file does not exist to read'
        exit(1)    
    
    allLines = stripAwayNewLines(inputFile)
    originalString = decodeBWT(allLines)
    outputFile = open(outputFileName, 'w')
    outputFile.write('>iBWT\n')
    writeToFileWithBreaks(outputFile, originalString)
    outputFile.close()
    inputFile.close()

else:
    print "Invalid flag. The flag must be \"-bwt\" to encode or \"-ibwt\" to decode"
    exit(1)
    