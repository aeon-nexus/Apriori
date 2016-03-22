import csv
import itertools

dataPath = '/home/aeon/Proj2/Apriori/INTEGRATED-DATASET2.csv'
configPath = '/home/aeon/Proj2/Apriori/Parameters2.config'

def main():
    dataSet = getData()
    minSup = getParam()
    #print "\nDATA:"+str(dataSet)+"\nMinSupport:"+str(minSup)
    frequentSets = Apriori(dataSet, minSup)
    print "\n Frequent Sets \n --------------"
    count = 1
    for freq in frequentSets:
        print "\n"+str(count)+" Frequnet Set :"+str(freq)
        count += 1

def Apriori(dataSet, minSup):
    frequentSet = []
    curFreqSet = []
    temp = []
    k = 1
    for transaction in dataSet:
        #print "\n Transaction Found: "+str(transaction)
        for item in transaction:
            #print "\nItem Found: "+item
            count = 0
            #print "\n curFreqSet:"+str(curFreqSet)
            if len(curFreqSet) == 0:
                curFreqSet.append([item,1])
                continue
            for curItem in curFreqSet:
                if curItem[0] == item:
                    #print "\nItem Found in CurFreqSet"
                    curItem[1] += 1
                    break
                else:
                    #print "\nItem not found, Incrementing Count"
                    count += 1
                    if count == len(curFreqSet):
                        #print "Item not found in curFreqSet, Adding Item "+ str([item,1])
                        curFreqSet.append([item,1])
                        break
    for item in curFreqSet:
        if item[1] >= minSup:
            temp.append(item)
    #print "\n1-ItemSet:"+str(curFreqSet)
    print "\n1-Frequent ItemSet:"+str(temp)
    curFreqSet = temp
    frequentSet.append(curFreqSet)
    print "\nFrequentSet : "+str(frequentSet)
    while curFreqSet:
        preFreqSet = list(curFreqSet)
        curFreqSet = []
        print "\npreFreqSet"+str(preFreqSet)
        candidateSet  = genCandidates(k,preFreqSet,dataSet)
        for cand in candidateSet:
            if cand[k+1] >= minSup:
                curFreqSet.append(cand)
        if curFreqSet:
            frequentSet.append(curFreqSet)
            print "\n"+str(k+1)+" FrequentSet : "+str(curFreqSet)
        else:
            print "\nFreqSet EMPTY"
        k += 1
    print "ALL FrequentSets :"+str(frequentSet)
    return frequentSet


def genCandidates(k,preFreqSet,dataSet):
    items = []
    combination = []
    preSets = []
    candidates = []
    for itemset in preFreqSet:
        sets = []
        for i in range(0,k):
            sets.append(itemset[i])
            if itemset[i] not in items:
                items.append(itemset[i])
        preSets.append(sets)
    print "\nPRESETS : "+str(preSets)
    print "\nITEMS: "+str(items)
    #print "\nCombinations : "+str(list(itertools.combinations(items,k+1)))
    for tup in list(itertools.combinations(items,k+1)):
        combination.append(list(tup))        
    print "\n COMBINATIONS : "+ str(combination)
    for comb in combination:
        flag = 0
        for tup in list(itertools.combinations(comb,k)):
            if list(tup) not in preSets:
                flag = 1
                break            
        if flag == 0 :
            candidates.append(comb)
    print "\nCandidates : "+str(candidates)
    for cand in candidates:
        supval = 0
        for transaction in dataSet:
            if set(cand).issubset(set(transaction)):
                supval += 1
        cand.append(supval)
    print "\nFinal CandidateSet :"+str(candidates)
    return candidates

def getData():
    Data = []
    with open(dataPath, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            Data.append(row)
    return Data

def getParam():
    f = open(configPath, 'r')
    minSup = int(f.readline())
    return minSup

main()