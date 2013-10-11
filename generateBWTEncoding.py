def encodeBWT(inStr, arr):
    
    results = []
    for el in arr:
        if el == 0:
            results.append("$")
        else:
            results.append(inStr[el - 1])

    results = "".join(results)
    return results