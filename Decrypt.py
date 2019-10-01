import sys
import math

def CAESAR_DEC(key,cipher):
    #print('CAESAR DECRYPTION')
    strDe = ""
    for char in cipher:
        charDe = ord(char) - ord('a')
        #print("Before: ",char,charDe)
        charDe = ( charDe - key ) % 26
        #print("After: ",charDe)
        strDe += chr(charDe + ord('a'))
    return strDe.lower()

def PLAYFAIR_DEC(key,cipher):
    print('PLAYFAIR DECRYPTION')
    #the Decrypted message
    strDe = ""
    #the Decryption Table
    tableDe = [ [-1 for i in range(5)] for i in range(5)]
    #record what alphabet has been filled 
    alphRecord = [False for i in range(26)]
    #index of next available alphabet in key to fill in to Decryption Table
    keyIdx = 0
    keyLen = len(key)
    #index of alphabet record indicating before which index has truley been filled. 
    alphRecIdx = 0
   
    #replace alphabet j into i in the key
    for char,step in enumerate(key):
        if(char == 'j'):
            key[step] = 'i'
   
    #fill up the Decryption Table
    for row in range(5):
        for col in range(5):
            #if we haven't fill all the alphabets in the key to the Decryption Table, do it first.
            if (keyIdx != keyLen) :
                alphInt = ord(key[keyIdx]) - ord('a')
                alphRecord[alphInt] = True
                tableDe[row][col] = alphInt
        
                #find the next available alphabet in the key
                #as for filling the Decryption Table
                keyIdx += 1
                while keyIdx < keyLen :
                    nextAlphInt = ord(key[keyIdx]) - ord('a')
                    if(alphRecord[nextAlphInt] == False):
                        #if the next alphabet in key was not in the Decrpytion Table break.
                        break
                    keyIdx += 1

            else:
                #iterate to find the next available alphabet to fill the  Decryption Table from a to z
                for itIdx in range(alphRecIdx,len(alphRecord)):
                    #if alphabet is not 'j' ('a' is 0)
                    if(itIdx != 9 and alphRecord[itIdx]==False):
                        alphRecord[itIdx] =True
                        tableDe[row][col] = itIdx
                        alphRecIdx = itIdx
                        break
    #transform tableDe from character index to char
    for row in range(5):
        for col in range(5):
            tableDe[row][col] = chr(ord('a')+tableDe[row][col])
            
    #print('tableDe: ',tableDe)

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
                elif(tableDe[r][c] == cipher[cipherIdx +1 ]):
                    r2 = r
                    c2 = c
        
        #Debugging
        if(r1 < 0 or r2 < 0 or c1 < 0 or c2 < 0):
            print("Decipher Error")
        
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
        #Debugging
        if(r1 < 0 or r2 < 0 or c1 < 0 or c2 < 0):
            print("Shift Error")
        #add into Decrypted message
        strDe += tableDe[r1][c1]
        strDe += tableDe[r2][c2]
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
    rowNum = int(math.ceil(len(cipher)/len(key)))
    colNum = len(key)
    table = [[ ' ' for i in range(colNum)] for i in range(rowNum)]
    #Create Decryption Table
    row = 0
    col = 0
    for char in cipher:
        table[row][col] = char
        row += 1
        if(row==rowNum):
            row = 0
            col += 1
            
    #Build Decrypted Message 
    for r in range(rowNum):
        for keyPosChar in key:
            keyPos = int(keyPosChar) - 1
            strDe += table[r][keyPos]

    return strDe


def RAILFENCE_DEC(key, cipher):
    strDe = ""
    keyLen = int(key)
    colNum = int(math.ceil(len(cipher)/float(keyLen)))
    table = [[' ' for i in range(colNum)] for i in range(keyLen)]
    #Create Decryption Table
    row = 0
    col = 0
    for char in cipher:
        table[row][col] = char
        col += 1
        if(col == colNum):
            col = 0
            row += 1
    #Build Decrypted Message
    for c in range(colNum):
        for r in range(keyLen):
            strDe += table[r][c]
    
    return strDe

if __name__ == '__main__':
    decType = sys.argv[1]
    Key = sys.argv[2].lower()
    Cipher = sys.argv[3].lower()
#    print(decType,Key,Cipher)
    if decType == 'caeser':
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


