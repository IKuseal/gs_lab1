import math

def generateHemingMatrix(wordLength):
    codeBitN = getControlBitsNum(wordLength)

    list1 = []
    for i in range(1, wordLength + codeBitN + 1):
        col = bin(i)[2:]
        col = col.zfill(codeBitN)
        list1.append(col)

    result = []
    for i in range(0,codeBitN):
        str = ""
        for j in range(0, wordLength + codeBitN):
            str+= list1[j][codeBitN-i-1]
        result.append(str)

    return result

def mult2BitStringsMod2(str1,str2):
    num = 0
    for i in range(0,len(str1)):
        num+= int(str1[i])*int(str2[i])
    return num % 2



def getControlBitsNum(wordLeng):
    initControlBitsNum = int(math.log(wordLeng,2)) + 1
    while(initControlBitsNum != int(math.log(wordLeng + initControlBitsNum,2)) + 1):
        initControlBitsNum += 1

    return initControlBitsNum