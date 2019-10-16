import sys
import math

def CAESAR_DEC(key,cipher):
    strDe = ""
    for char in cipher:
        charDe = ord(char) - ord('a')
        charDe = ( charDe - key ) % 26
        strDe += chr(charDe + ord('a'))
    return strDe.lower()

def PLAYFAIR_DEC(key,cipher):
    #the Decrypted message
    strDe = ""
    #the Decryption Table
    tableDe = [ [-1 for i in range(5)] for i in range(5)]
    #array recording which alphabet has been filled 
    alphRecord = [False for i in range(26)]
    #modify the key to ensure all alphabets are included
    key += "abcdefghiklmnopqrstuvwxyz"
    keyLen = len(key)
    #index of next available alphabet in key to fill in to Decryption Table
    #initial value: 0
    keyIdx = 0   
    #replace alphabet j to i in the key
    for step,char in enumerate(key):
        if(char == 'j'):
            key = key[:step-1] + 'i' + key[step:]
   
    #fill up the Decryption Table
    for row in range(5):
        for col in range(5):
            alphInt = ord(key[keyIdx]) - ord('a')
            alphRecord[alphInt] = True
            tableDe[row][col] = alphInt
            #find the next available alphabet in the key
            #as for filling the Decryption Table
            while keyIdx < keyLen :
                nextAlphInt = ord(key[keyIdx]) - ord('a')
                if(alphRecord[nextAlphInt] == False):
                    #if the next alphabet in key was not in the Decrpytion Table break.
                    break
                keyIdx += 1

    #transform tableDe from character index to char
    for row in range(5):
        for col in range(5):
            tableDe[row][col] = chr(ord('a')+tableDe[row][col])
            
    #process the cipher,iterating with step 2
    for cipherIdx in range(0,len(cipher),2):
        r1 = -1
        r2 = -1
        c1 = -1
        c2 = -1
        #find the rows and columns of two cipher chars 
        for r in range(5):
            for c in range(5):
                if(tableDe[r][c] == cipher[cipherIdx]):
                    r1 = r
                    c1 = c
                elif(tableDe[r][c] == cipher[cipherIdx + 1]):
                    r2 = r
                    c2 = c
        #if same row shift left
        if(r1 == r2):
            c1 -= 1 if c1 > 0 else -4
            c2 -= 1 if c2 > 0 else -4
        #if same col shift up
        elif(c1 == c2):
            r1 -= 1 if r1 > 0 else -4
            r2 -= 1 if r2 > 0 else -4
        #else swap column
        else:
            tmpCol = c1
            c1 = c2
            c2 = tmpCol
        #add into Decrypted message
        strDe += tableDe[r1][c1] + tableDe[r2][c2]
    
    return strDe.lower()

def VERNAM_DEC(key,cipher):
    strDe = ""
    keyIdx = 0
    cipherIdx = 0
    cipherLen = len(cipher)
    while(len(strDe)!=cipherLen):
        keyCharInt = ord(key[keyIdx])-ord('a')
        cipherCharInt = ord(cipher[cipherIdx]) -ord('a')
        #vernam cipher decryption
        autoKeyChar =  chr((keyCharInt ^ cipherCharInt) + ord('a'))
        #Save decrypted character for further decryption(auto key)
        key += autoKeyChar
        strDe += autoKeyChar
        keyIdx += 1;
        cipherIdx += 1
    return strDe.lower()

def ROWTRANS_DEC(key,cipher):
    strDe = ""
    rowNum = int(math.ceil(len(cipher)/float(len(key))))
    colNum = len(key)
    #remainders. Determines the how many character to get for a column
    rem = len(cipher) % colNum
    table = [[ ' ' for i in range(colNum)] for i in range(rowNum)]
    cipherPos = 0

    #Create Decryption Table
    for i in range(1,colNum+1):
        idx = key.index(str(i))
        getChars = rowNum
        if( idx >= rem and rem != 0 ):
            getChars -= 1
        for row in range(getChars):
            table[row][idx] = cipher[cipherPos]
            cipherPos += 1

    #Build Decrypted Message 
    for r in range(rowNum):
        for c in range(colNum):
            if(table[r][c] != ' ' ):
                strDe += table[r][c]

    return strDe


def RAILFENCE_DEC(key, cipher):
    ciphLen = len(cipher)
    strDe = list([' ' for i in range(ciphLen)])
    rowNum = int(key)
    CalcGap = lambda x: x * 2 - 3
    
    ciphIdx = 0
    #Build Decrypted Message
    for layer in range(1,rowNum+1):
        #set the starting cipher index
        msgIdx = layer-1

        #highest and lowest point of wave
        #has no wave interception point
        if(layer==1 or rowNum-layer==0):
            while(msgIdx < ciphLen and ciphIdx < ciphLen):
                strDe[msgIdx] = cipher[ciphIdx]
                msgIdx += CalcGap(rowNum)+1
                ciphIdx += 1
        else:
            while(msgIdx < ciphLen):
                #wave start point
                strDe[msgIdx] = cipher[ciphIdx]
                #the intercept point distance is calculated 
                #base on the small wave.
                #the small wave height is the distance from current layer to the bottom
                msgIdx += CalcGap((rowNum-layer+1))+1
                ciphIdx += 1
                #interception point of wave
                if(msgIdx < ciphLen):
                    strDe[msgIdx] = cipher[ciphIdx]
                    #calculate the next wave start.
                    #the intercept point distance is calculated base on the small wave.
                    #the small wave height is the distance from current layer to the top.
                    msgIdx += CalcGap(layer)+1
                    ciphIdx += 1
                else:
                    break
    strDe = "".join(strDe)
    return strDe

if __name__ == '__main__':
    decType = sys.argv[1]
    Key = sys.argv[2].lower()
    Cipher = sys.argv[3].lower()
#    print(decType,Key,Cipher)
    if decType == 'caesar':
        print(CAESAR_DEC(int(Key),Cipher))
    elif decType == 'playfair':
        print(PLAYFAIR_DEC(Key,Cipher)) 
    elif decType == 'vernam':
        print(VERNAM_DEC(Key,Cipher))
    elif decType == 'row':
        print(ROWTRANS_DEC(Key,Cipher))
    elif decType == 'rail_fence':
        print(RAILFENCE_DEC(Key,Cipher))
    else:
        print("Unknown Decryption Command")


