import random
import sys
import base64
import json
import os
PUB_FILE = './rsa.pub'
PRV_FILE = './rsa.key'
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


# 產生金鑰
def Generate(length):
    global pubJson
    global prvJson
    len_p = length//2
    len_q = length - len_p
    # 縮小加密金鑰長度
    len_e = int(length * 0.2)
    p = GenPrimeMiller(len_p, 4)
    q = GenPrimeMiller(len_q, 4)
    n = p*q
    fN = (p-1) * (q-1)
    e = 1
    d = 1
    while(True):
        e = GenPrimeCandidate(len_e)
        Result = ExtendGCD(e, fN)
        if(Result[0] == 1):
            d = Result[1][0]
            break
    # CRT 預先運算
    _p = ExtendGCD(p, q)[1][0]
    _q = ExtendGCD(q, p)[1][0]
    Dp = d % (p-1)
    Dq = d % (q-1)
    # 調整所有用於Invert的負數
    if(d < 0):
        d += fN
    if(_p < 0):
        _p += q
    if(_q < 0):
        _q += p

    # 存入公開檔案
    pubJson = {
        "n": n,
        "e": e,
        "len": length,
    }
    # 存入私有檔案
    prvJson = {
        "n": n,
        "d": d,
        "p": p,
        "_p": _p,
        "q": q,
        "_q": _q,
        "Dp": Dp,
        "Dq": Dq,
        "fN": fN,
        "len": length,

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
    # Print Debug Messages
    print("P:" + str(p))
    print("Q:" + str(q))
    print("N:" + str(n))
    print("fN:" + str(fN))
    print("e:" + str(e))
    print("d:" + str(d))
    print("_P:" + str(_p))
    print("_Q:" + str(_q))
    print("Dp:" + str(Dp))
    print("Dq:" + str(Dq))
    print("Validation:"+str((e * d) % fN))
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


# 加密
def Encrypt(plainStr: str):
    if(len(pubJson) == 0):
        Load()
    plainBytes = plainStr.encode('utf-8')
    if(len(plainBytes)*8 >= int(pubJson['len'])-1):
        print('Error: [String Len]('+str(len(plainBytes)*8) + ') > [Key Len - 1](' +
              str(int(pubJson['len'])-1)+').')
        sys.exit(0)
    else:
        EncInt = SquareMultiply(int.from_bytes(
            plainBytes, 'big', signed=False), pubJson['e'], pubJson['n'])
    return base64.b64encode(str(EncInt).encode('ascii')).decode('utf-8')


# 解密
def Decrypt(cypherStr: str):
    if(len(prvJson) == 0):
        Load()
    cypherBytes = cypherStr.encode('utf-8')
    cypher = int(base64.b64decode(cypherBytes).decode('ascii'))
    p = prvJson['p']
    _p = prvJson['_p']
    q = prvJson['q']
    _q = prvJson['_q']
    n = prvJson['n']
    Dp = prvJson['Dp']
    Dq = prvJson['Dq']
    d = prvJson['d']
    Xp = cypher % p
    Xq = cypher % q
    Yp = SquareMultiply(Xp, Dp, p)
    Yq = SquareMultiply(Xq, Dq, q)
    print(Xp.bit_length(), Dp.bit_length(), p.bit_length())
    print(Xq.bit_length(), Dq.bit_length(), q.bit_length())
    DecInt = (_q*q*Yp+_p*p*Yq) % n
    return DecInt.to_bytes(DecInt.bit_length()//8 + 1, byteorder='big').decode('utf-8')


# print(Decrypt(Encrypt(
#     '@fea')))
if __name__ == "__main__":
    if(len(sys.argv) == 1):
        print('-n {length}: Generate New Keys')
        print('-e {plain}: Encrypt')
        print("-d {cypher}: Decrypt")
        sys.exit(0)
    i = 1
    while(i < len(sys.argv)):
        if(sys.argv[i] == '-n'):
            i += 1
            Generate(int(sys.argv[i]))
        elif(sys.argv[i] == '-d'):
            i += 1
            print('Decrypt Result:\n' + Decrypt(sys.argv[i]))
            # Decrypt Cypher
        elif(sys.argv[i] == '-e'):
            i += 1
            print('Encrypt Result:\n' + Encrypt(sys.argv[i]))
            # Encrypt  Plain
        i += 1
