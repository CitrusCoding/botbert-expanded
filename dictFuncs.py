#input the csv file into a dictionary 
def inputWords(csvFile): #Inputs words from csv into dictionary
    newDict = {}
    for words in csvFile:
        wordPairs = words.split(",")
        newDict[wordPairs[1].replace("\n", "")] = wordPairs[0]
    return (newDict)
    #morse : letters
#I took this directly from a school project lol