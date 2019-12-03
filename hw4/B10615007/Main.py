import sys
from Prime import PrimeTest, GCD
from Euler import EulerPhiFunc
from BigExp import BigExp
import random
from Time import start, end, writeRecords, first
import math


if __name__ == "__main__":
    if sys.argv[1] == "init":
        start()

        bits = int(sys.argv[3]) - 2 if int(sys.argv[3]) > 2 else 0
        mode = sys.argv[2]

        # we only need to generate the part except first and last bit
        numberUsed = []
        randNums = []
        randInt = 0
        start()
        while True:
            randBin = bin(random.randrange(0, pow(2, bits)))[2:]
            randBin = randBin.rjust(bits, '0')
            randInt = int('0b1' + randBin + '1', 2)

            # check whether the randInt was used before
            if randInt in numberUsed:
                continue

            # go for primeTest
            if PrimeTest(randInt):
                randNums.append(randInt)

            if len(randNums) == 2:
                break

            # print("Not Prime: ", randInt)
            # append the randInt to numberUsed to prevent the test ran again on same number (save cost)
            numberUsed.append(randInt)
        end("Find prime n value")

        p, q = randNums
        n = p * q
        PhiN = EulerPhiFunc(n, p, q)

        e = None
        # e should be as small as possible so we use iteration from 2
        start()
        for i in range(2, PhiN):
            if GCD(PhiN, i) == 1:
                e = i
                break
        end("Iteration for e")

        start()
        # this part takes too long
        d = BigExp(e, PhiN, mode=mode) ** -1
        end("Calculate d value")

        # print result on console
        print(f"p = {p}\n"
              f"q = {q}\n"
              f"n = {n}\n"
              f"Phi(n) = {PhiN}\n"
              f"e = {e}\n"
              f"d = {d}")

        # write the result on file
        f = open("info.txt", "w+")
        f.write(f"p = {p}\n"
                f"q = {q}\n"
                f"n = {n}\n"
                f"Phi(n) = {PhiN}\n"
                f"e = {e}\n"
                f"d = {d}\n")
        f.close()
        writeRecords()

        while True:
            input_text = input("Input en or de or ex(encrypt/decrypt/exit): ")
            if input_text == 'en':
                key = input("Input key to encrypt: ")
                start()
                keyInt = ''
                for letter in key:
                    # the ord Ascii value should only between 1-255
                    keyInt += str(ord(letter)).rjust(3, '0')
                keyInt = int(keyInt)
                ciphertext = BigExp(keyInt, n, mode=mode, p=p, q=q) ** e
                print(f"\nYour encrypted value is:\n{ciphertext}")
                end("Calculate encrypt value")
                writeRecords(False)

            elif input_text == 'de':
                value = input("Input value to decrypt: ")
                start()
                value = int(value)
                plaintext = BigExp(value, n, mode=mode, p=p, q=q) ** d
                plaintext = str(plaintext)
                plaintext = str(plaintext).rjust(math.ceil(len(plaintext) / 3) * 3, '0')
                plaintext = [plaintext[i: i+3] for i in range(0, len(plaintext), 3)]
                plainInt = ''
                for char in plaintext:
                    # the ord Ascii value should only between 1-255
                    plainInt += str(chr(int(char)))
                print(f"\nYour decrypted key is:\n{plainInt}")
                end("Calculate decrypt value")
                writeRecords(False)

            elif input_text == 'ex':
                break













