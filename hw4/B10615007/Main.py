import sys
from Prime import PrimeTest, GCD
from Euler import EulerPhiFunc
from BigExp import BigExp
import random
from Time import start, end


if __name__ == "__main__":
    if True or sys.argv[1] == "init":
        start()
        # bits = sys.argv[2] - 2 if sys.argv[2] > 2 else 0
        bits = 40
        mode = "CRT"

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
        for i in range(2, PhiN):
            if GCD(PhiN, i) == 1:
                e = i
                break

        start()
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
        f = open("log.txt", "w+")
        f.write(f"p = {p}\n"
                f"q = {q}\n"
                f"n = {n}\n"
                f"Phi(n) = {PhiN}\n"
                f"e = {e}\n"
                f"d = {d}\n")

        message = 5191651
        start()
        ciphertext = BigExp(message, n, mode=mode, p=p, q=q) ** e
        end("Get ciphertext value")
        start()
        plaintext = BigExp(ciphertext, n, mode=mode, p=p, q=q) ** d
        end("Get plaintext value")

        print(f"message = {message}\n"
              f"ciphertext = {ciphertext}\n"
              f"plaintext = {plaintext}\n")
        end("Whole function")











