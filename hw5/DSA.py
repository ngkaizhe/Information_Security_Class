import random
import sys
import base64
import hashlib
import json
import os
import math
PUB_FILE = './dsa.pub'
PRV_FILE = './dsa.key'
OUT_FILE = './out.txt'
IN_FILE = './in.txt'
pubJson = {}
prvJson = {}


# modn的情況下快速運算次方
def SquareMultiply(base: int, expo: int, moduler: int):
    base = base % moduler
    pattern = []
    while(expo > 0):
        if(expo % 2 == 0):
            pattern.append(False)
        else:
            pattern.append(True)
        expo //= 2
    pattern.reverse()
    Result = 1
    for bit in pattern:
        Result = (Result ** 2) % moduler
        if(bit == True):
            Result = (Result * base) % moduler
    return Result


# 亂數產生可能的質數
def GenPrimeCandidate(bits: int = 64):
    bits -= 1
    i = 1
    Result = 1
    while(i < bits):
        Result *= 2
        Result += random.randint(0, 1)
        i += 1
    Result = Result * 2 + 1
    return Result

# 測驗 r = range(1,s)之間有沒有符合a^(2r*d)(modp) == -1


def MillerTestHelper(s: int, Witness: int, PrimeCandidate: int):
    _PrimeCandidate = PrimeCandidate - 1
    for _ in range(1, s):
        Witness = (Witness ** 2) % PrimeCandidate
        if(Witness == _PrimeCandidate):
            return True
    return False


# 驅動米勒測試
def MillerTest(PrimeCandidate: int, times: int):
    _PrimeCandidate = PrimeCandidate - 1

    d = _PrimeCandidate
    s = 0
    # 找出質因數分解中2的個數
    while(d % 2 == 0):
        s += 1
        d //= 2

    # 進行機率測試
    for _ in range(times):
        randInt = random.randint(2, _PrimeCandidate-1)
        Witness = SquareMultiply(randInt, int(d), PrimeCandidate)
        if(Witness == 1 or Witness == _PrimeCandidate):
            continue
        elif(MillerTestHelper(s, Witness, PrimeCandidate) != True):
            # 不是質數
            return False
    # 有可能是質數
    return True


# 產生通過米勒測試的大質數
def GenPrimeMiller(bits: int, tests: int):
    while(True):
        PrimeCandidate = GenPrimeCandidate(bits)
        if(MillerTest(PrimeCandidate, tests) == True):
            return PrimeCandidate


# 歐拉求公因數
def ExtendGCD(a: int, b: int):
    A = (1, 0)
    B = (0, 1)
    while(a != 0 and b != 0):
        mult = a//b
        a %= b
        A = (A[0]-mult*B[0], A[1]-mult*B[1])
        A, B = B, A
        a, b = b, a
    return a, A


def ValidKeyPairs():
    len_p = 1024
    len_q = 160

    b_1024 = 2**1024
    b_1023 = 2**1023

    q = GenPrimeMiller(len_q, 3)
    p = 0
    p0 = GenPrimeMiller(math.ceil(len_p/2+1), 3)
    x = GenPrimeCandidate(len_p)
    x = b_1023 + x % b_1023
    t = math.ceil(x/(2*q*p0))
    counter = 0
    while(counter < 4 * len_p):
        # Generate Prime Candidate
        if((2 * t * q * p0) + 1 > b_1024):
            t = math.ceil(b_1023/(2*q*p0))
        p = (2*t*q*p0) + 1
        counter += 1
        # Test Validity
        a = random.randint(2, p-2)
        a = 2 + a % (p-3)
        z = SquareMultiply(a, 2*t*q, p)
        if(ExtendGCD(z-1, p)[0] == 1 and SquareMultiply(z, p0, p) == 1):
            # Valid Key Pair
            return p, q
        t = t + 1
    return -1, -1


# 產生金鑰
def Generate():
    global pubJson
    global prvJson

    # Common Parameters
    p, q = ValidKeyPairs()
    if(p == -1):
        print('Cannot Generate Key. Please Try Again.')
        return
    g = SquareMultiply((random.randint(2, p-2)), (p-1)//q, p)
    # Private Key
    x = random.randint(2, p-1)
    # Public Key
    y = SquareMultiply(g, x, p)

    # 存入公開檔案
    pubJson = {
        "p": p,
        "q": q,
        "g": g,
        "y": y,
    }
    # 存入私有檔案
    prvJson = {
        "p": p,
        "q": q,
        "g": g,
        "x": x
    }
    # 存入指定檔案位置
    pubfile = open(PUB_FILE, 'w')
    prvfile = open(PRV_FILE, 'w')
    pubfile.write(base64.b64encode(json.dumps(
        pubJson).encode('utf-8')).decode('utf-8'))
    prvfile.write(base64.b64encode(json.dumps(
        prvJson).encode('utf-8')).decode('utf-8'))
    pubfile.close()
    prvfile.close()
    # # Print Debug Messages
    print("P:" + str(p))
    print("Q:" + str(q))
    print("G:" + str(g))
    print("Y:" + str(y))
    print("X:" + str(x))
    print("Validation[g^q%p]:"+str(SquareMultiply(g, q, p)))
    print("Key Generation Done...")


# 載入金鑰
def Load():
    print('Loading Key Files...')
    global pubJson
    global prvJson
    if(os.path.exists(PUB_FILE) == False or os.path.exists(PRV_FILE) == False):
        print('Cannot Load Key Files.')
        print('Check Your File Location or Generate a New One.')
        sys.exit(0)
    pubfile = open(PUB_FILE)
    prvfile = open(PRV_FILE)

    pubJson = json.loads(base64.b64decode(
        pubfile.read().encode('utf-8')).decode('utf-8'))
    prvJson = json.loads(base64.b64decode(
        prvfile.read().encode('utf-8')).decode('utf-8'))

    pubfile.close()
    prvfile.close()


# 簽章
def Sign(plainStr: str):
    if(len(prvJson) == 0):
        Load()
    # Preparation
    plainBytes = plainStr.encode('utf-8')
    p = int(prvJson['p'])
    q = int(prvJson['q'])
    g = int(prvJson['g'])
    x = int(prvJson['x'])
    hashf = hashlib.sha1()
    hashf.update(plainBytes)
    hashv = int(hashf.hexdigest(), base=16)
    k = random.randint(1, q-1)
    (gcd, xy) = ExtendGCD(k, q)
    k_inv = xy[0]
    if(not gcd == 1):
        print('Error: Cannot Sign Message(cannot find k inverse).Please Retry Again.')
        return
    r = SquareMultiply(g, k, p) % q
    s = ((k_inv % q) * (hashv % q + (x * r) % q)) % q

    outData = {
        'plain': plainStr,
        'r': r,
        's': s,
    }
    # 寫出到檔案
    # outfile = open(OUT_FILE, 'w')
    # outfile.write(base64.b64encode(json.dumps(
    #     outData).encode('utf-8')).decode('utf-8'))
    # outfile.close()
    return base64.b64encode(json.dumps(outData).encode('utf-8')).decode('utf-8')


# 驗證
def Verify(cypherStr: str):
    if(len(pubJson) == 0):
        Load()

    inData = json.loads(base64.b64decode(
        cypherStr.encode('utf-8')).decode('utf-8'))
    # Preparation
    p = int(pubJson['p'])
    q = int(pubJson['q'])
    g = int(pubJson['g'])
    y = int(pubJson['y'])
    r = int(inData['r'])
    s = int(inData['s'])
    plainStr = str(inData['plain'])
    # Get Hash of Plain Text
    hashf = hashlib.sha1()
    hashf.update(plainStr.encode('utf-8'))
    hashv = int(hashf.hexdigest(), base=16)
    # Get w/u1/u2/v
    (gcd, xy) = ExtendGCD(s, q)
    if(not gcd == 1):
        print("Error: Cannot Verify Message(gcd != 1)")
        return
    else:
        w = xy[0] % q

    u1 = (hashv * w) % q
    u2 = (r * w) % q
    v = ((SquareMultiply(g, u1, p) * SquareMultiply(y, u2, p)) % p) % q
    if(v == r):
        return '(Verified)' + plainStr
    else:
        return '(Unverified)' + plainStr


# Generate()
# print(Verify(Sign('87878787878787878787')))
if __name__ == "__main__":
    if(len(sys.argv) == 1):
        print('-n : Generate New Keys (1024,160)')
        print('-s {plain msg}: s')
        print("-v {signed msg}: v")
        sys.exit(0)
    i = 1
    while(i < len(sys.argv)):
        if(sys.argv[i] == '-n'):
            Generate()
        elif(sys.argv[i] == '-s'):
            # Sign
            i += 1
            print('Sign Result:\n' + Sign(sys.argv[i]))
        elif(sys.argv[i] == '-v'):
            # Verify
            i += 1
            print('Verify Result:\n' + Verify(sys.argv[i]))
        i += 1
