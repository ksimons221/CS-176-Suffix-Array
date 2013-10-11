def generateIndexMapping(aStr, keyIndex):
    lDict = {}
    lIndexMapping = {}
    
    index = 0
    for char in aStr:
        if char in lDict:
            lDict[char] = lDict[char] + 1
        else:
            lDict[char] = 1
        key = char + str(lDict[char])
        if keyIndex:
            lIndexMapping[index] = key
        else:
            lIndexMapping[key] = index
        index +=1

    return lIndexMapping

def decodeBWT(bwt):
    L = list(bwt)
    F = sorted(L)
    results = []

    LIndexMapping = generateIndexMapping(L, False)
    FIndexMapping = generateIndexMapping(F, True)
    
    nullChar = "$1"
    
    currentIndex = LIndexMapping[nullChar]
    currentChar = FIndexMapping[currentIndex]
    
    while currentChar != nullChar:
        results.append(currentChar[0])
        currentIndex = LIndexMapping[currentChar]
        currentChar = FIndexMapping[currentIndex]

    results.append(currentChar[0])
    
    results = "".join(results)

    return results