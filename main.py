import sys

def radixSort (items, index):
    results = []
    buckets = {}
    reApplyRadix = []
    for i in items:
        key = i[index]
        if key in buckets:
            reApplyRadix.append(key)
            buckets[key] = buckets[key] + [i]
        else: 
            buckets[key] = [i]
    reApplyRadix = set(reApplyRadix)
    reApplyRadix = list(reApplyRadix)
    for key in reApplyRadix:
        buckets[key] =  radixSort(buckets[key], index+1)
    currentKeys = buckets.keys()
    currentKeys = sorted(currentKeys)
    for key in currentKeys:
        results = results + buckets[key]
    
    return results

def charTripleList(inStr, startIndex):
    results = {}
    while startIndex < len(inStr):
        stringSlice = inStr[startIndex : startIndex + 3] + ["$"] + ["$"] + ["$"]
        tripleChar = stringSlice[0:3]
        results[startIndex] = (tripleChar[0],tripleChar[1],tripleChar[2])
        startIndex += 3;
    return results

def strip2(x): return x[2]

def createSortedB0Indexs(inStr, masterDict):

    results = []
    index = 0
    while index < len(inStr):
        if index == len(inStr) - 1:
            results.append((inStr[len(inStr) - 1], 0, len(inStr) - 1))
        else:
            rank = masterDict[index+1]
            results.append((inStr[index], rank, index) )
        index += 3

    results = radixSort(results, 0)
    b0IndexResults =  map(strip2, results)    # CORRECT
    return b0IndexResults

def mergeB0andB(originalStr, sortedBOIndex, sortedRIndex, rankRDictionary):
    
    B0pointer = 0
    Rpointer = 0
    results = []
    
    while B0pointer < len(sortedBOIndex) and Rpointer < len(sortedRIndex):
        bIndex = sortedBOIndex[B0pointer]
        rIndex = sortedRIndex[Rpointer]
        if originalStr[bIndex] == originalStr[rIndex]:
            if rIndex % 3 == 1:
                if rankRDictionary[bIndex+1] < rankRDictionary[rIndex+1]:
                    results.append(bIndex)
                    B0pointer += 1
                else:
                    results.append(rIndex)
                    Rpointer += 1
            elif rIndex % 3 == 2:
                if originalStr[bIndex+1] == originalStr[rIndex+1]:
                    if rankRDictionary[bIndex+2] < rankRDictionary[rIndex+2]:
                        results.append(bIndex)
                        B0pointer += 1
                    else:
                        results.append(rIndex)
                        Rpointer += 1
                elif originalStr[bIndex+1] < originalStr[rIndex+1]:
                    results.append(bIndex)
                    B0pointer += 1
                else:
                    results.append(rIndex)
                    Rpointer += 1
            else:
                print "FATAL ERROR"
                exit(1)
        else:
            if originalStr[bIndex] < originalStr[rIndex]:
                results.append(bIndex)
                B0pointer += 1
            else:
                results.append(rIndex)
                Rpointer += 1
                
    if Rpointer < len(sortedRIndex):
        results = results + sortedRIndex[Rpointer:]
    
    if B0pointer < len(sortedBOIndex):
        results = results + sortedBOIndex[B0pointer:]
    return results

def sortedIndexNewRankMapping(sortedRecursiveIndex):
    results = {}
    for i in range(len(sortedRecursiveIndex)):
        results[sortedRecursiveIndex[i]] = i + 1
    return results
        
def sampledOrderAndDic(inStr):
    R1Dict = charTripleList(inStr, 1)
    R2Dict = charTripleList(inStr, 2)
    
    
    tuple1 = []
    tuple2 = []
    counter = 1
    while counter < len(inStr):
        if counter in R1Dict:
            tuple1.append(R1Dict[counter])
        if (counter+1) in R2Dict:
            tuple2.append(R2Dict[(counter+1)]) 
        counter +=3

    originalR = tuple1 + tuple2    
    
    bothR = []
    backMap = {}
    
    for key in R1Dict.keys():
        backMap[R1Dict[key]] = key
        bothR.append(R1Dict[key])
    
    for key in R2Dict.keys():
        backMap[R2Dict[key]] = key
        bothR.append(R2Dict[key])
    
    noDuplicates = list(set(bothR))

    sortedR = radixSort(noDuplicates, 0)

    haveDuplicates = False
    if len(noDuplicates) != len(bothR):
        haveDuplicates = True
         
    tupleRanking = {}
    for i in range(len(sortedR)):   
        tupleRanking[sortedR[i]] = i + 1
    
    if haveDuplicates == False:
        rIndexInOrder = []    
        
        for i in range(len(sortedR)):
            rIndexInOrder.append(backMap[sortedR[i]])
    
        sortedRecursiveDict = sortedIndexNewRankMapping(rIndexInOrder)
    
        return (rIndexInOrder, sortedRecursiveDict)
    
    else:
        if haveDuplicates:
            newString = []
            for i in range(len(originalR)):
                newString.append(str(tupleRanking[originalR[i]]))
            newString.append("$")
            arr = createSuffixArray(newString)

            sortedIndex = []
            for a in arr[1:]:
                sortedIndex.append(convertBack(len(inStr)/3, a))
            sortedIndexDict = sortedIndexNewRankMapping(sortedIndex)

            return (sortedIndex, sortedIndexDict)
       
def convertBack(half, x):
    if x < half:
        return 1 + 3*x
    else:
        x = x - half
        return 2 + 3 * x

def createSuffixArray(inStr):
  
    R1R2results = sampledOrderAndDic(inStr)
 
    rIndexInOrder =  R1R2results[0]
    sortedRecursiveIndex = R1R2results[1]
 
    sortedB0Index = createSortedB0Indexs(inStr, sortedRecursiveIndex) 

    suffixArray = mergeB0andB(inStr, sortedB0Index, rIndexInOrder, sortedRecursiveIndex )

    return suffixArray

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
    allLines = ""
    count = 0
    for line in inputFile:
        if count == 1:
            line = line.rstrip('\n')
            allLines = allLines + line
        count = 1
    allLines = list(allLines)
    arr = createSuffixArray(allLines)
    print arr
    outputFile = open(outputFileName, 'w')
    outputFile.write('This is a test\n')
    outputFile.write('This is a test2\n')
    
    outputFile.close()
    inputFile.close()

elif flag == "-ibwt":
    try:
        inputFile = open(inputFileName, 'r')
    except IOError:
        print 'The input file does not exist to read'
        exit(1)
    inputFile.close()

else:
    print "Invalid flag. The flag must be \"-bwt\" to encode or \"-ibwt\" to decode"
    exit(1)
    
print "Done"
