

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
    if len(originalStr) > 32250:


        print "FUCK"
        #print sortedBOIndex
        #print "GAP"
        #print sortedRIndex    

        print len(originalStr)
        print len(sortedBOIndex)
        print len(sortedRIndex)
        print sortedBOIndex
        print sortedRIndex
        for i  in range(len(originalStr)):
            if originalStr[i] == "a":
                print i
            
        
        exit(0)
    B0pointer = 0
    Rpointer = 0
    results = []
    
    while B0pointer < len(sortedBOIndex) and Rpointer < len(sortedRIndex):
        #print B0pointer , Rpointer
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
    #print "Results"
    #print results 
    #exit(1)
    #print results
    #exit(1)

    return results

def sortedIndexNewRankMapping(sortedRecursiveIndex):
    results = {}
    for i in range(len(sortedRecursiveIndex)):
        results[sortedRecursiveIndex[i]] = i + 1
    return results
        
def sampledOrderAndDic(inStr):
    R1Dict = charTripleList(inStr, 1)
    R2Dict = charTripleList(inStr, 2)
    numTuples = len(R1Dict)
        
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
        #print len(noDuplicates) 
        #print len(bothR)
        #t = sorted(bothR)
        #print t
        #exit(1)
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
                #newString.append(str(tupleRanking[originalR[i]]))
                newString.append(tupleRanking[originalR[i]])
            #newString.append("$")
            newString.append(-1)

            arr = createSuffixArray(newString)
            #print arr
            #print newString

    
            #print tupleRanking
            #print(len(inStr))
            #exit(1)
            sortedIndex = []
            for a in arr[1:]:
                sortedIndex.append(convertBack(numTuples, a))
            sortedIndexDict = sortedIndexNewRankMapping(sortedIndex)

            #print "CHARS"
            #for x in sortedIndex:
                #print inStr[x]
            #exit(1)
            return (sortedIndex, sortedIndexDict)
       
def convertBack(half, x):
    if x < half:
        return 1 + 3*x
    else:
        x = x - half
        return 2 + 3 * x

def createSuffixArray(inStr):
  
    #print "hey"
  
  
    R1R2results = sampledOrderAndDic(inStr)
    rIndexInOrder =  R1R2results[0]
    #print len(rIndexInOrder)
 
    #print "Shit"
    #print R1R2results
    
 
    #if len(rIndexInOrder) != 200:
        #print inStr
     #   for x in rIndexInOrder:
      #      print inStr[x]
    #exit(0)
    
    sortedRecursiveIndex = R1R2results[1]
 
    sortedB0Index = createSortedB0Indexs(inStr, sortedRecursiveIndex) 

    suffixArray = mergeB0andB(inStr, sortedB0Index, rIndexInOrder, sortedRecursiveIndex )

    #print suffixArray

    return suffixArray
