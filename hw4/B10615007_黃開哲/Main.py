import sys
from Prime import PrimeTest, GCD
from Euler import EulerPhiFunc
from BigExp import BigExp
import random
from Time import start, end, writeRecords
import math


if __name__ == "__main__":
    if sys.argv[1] == "init":
        # a start point for saving current time(for further used)
        start()

        # as the first and last bit is '1', RNG needed bits will get divide(if n is 1024, p and q are 512 bits) and minus 2
        bits = int(int(sys.argv[3]) / 2) - 2
        # get the mode value from console
        mode = sys.argv[2]

        # we only need to generate the part except first and last bit
        # numberUsed: save the non prime value use in previous RNG, if RNG the same value again, no need to determine again
        numberUsed = []
        # randNums: the prime number, will only has 2 elements, p and q
        randNums = []
        # randInt: the Int form the RNG number
        randInt = 0
        # another start point for saving current time
        start()
        while True:
            # RNG
            randBin = bin(random.randrange(0, pow(2, bits)))[2:]
            # add '0' to front, if the value wasn't as required bits
            randBin = randBin.rjust(bits, '0')
            # add '1' in front and back
            randInt = int('0b1' + randBin + '1', 2)

            # check whether the randInt was used before
            # if it has been generate before, skip the continuous steps
            if randInt in numberUsed:
                continue

            # go for primeTest
            # if the primeTest pass, means it is probably a prime number
            if PrimeTest(randInt):
                randNums.append(randInt)

            # if the length is 2, means p and q has been found
            if len(randNums) == 2:
                break

            # append the randInt to numberUsed to prevent the test ran again on same number (save cost)
            numberUsed.append(randInt)

        # Saving the time used for finding prime n
        end("Find prime n value")

        # save value in each variables
        p, q = randNums
        n = p * q
        # calculate the PhiN which is (p-1)*(q-1)
        PhiN = EulerPhiFunc(n, p, q)

        e = None
        # another start point for saving current time
        start()
        # e should be as small as possible so we use iteration from 2
        for i in range(2, PhiN):
            # if co-prime found, exit loop then
            if GCD(PhiN, i) == 1:
                e = i
                break
        # Save the time used for finding e
        end("Iteration for e")

        start()
        # d = (e^-1)mod(PhiN)
        d = BigExp(e, PhiN, mode=mode) ** -1
        end("Calculate d value")

        # print result on console
        print(f"p = {p}\n"
              f"q = {q}\n"
              f"n = {n}\n"
              f"Phi(n) = {PhiN}\n"
              f"e = {e}\n"
              f"d = {d}")

        # write the result on info file
        f = open("info.txt", "w+")
        f.write(f"p = {p}\n"
                f"q = {q}\n"
                f"n = {n}\n"
                f"Phi(n) = {PhiN}\n"
                f"e = {e}\n"
                f"d = {d}\n")
        f.close()
        # write records of time in log.txt
        writeRecords()

        while True:
            # ask user to input choice between encrypt, decrypt and exit
            input_text = input("Input en or de or ex(encrypt/decrypt/exit): ")
            if input_text == 'en':
                # get key
                key = input("Input key to encrypt: ")
                start()
                keyInt = ''

                # as the key for encryption, only accept integer,
                # so I change string form to integer form, depends on their ASCII

                for letter in key:
                    # the ord Ascii value should only between 1-255
                    # if the value was under 100, it will fill 0 in front, ex: 99 -> 099
                    keyInt += str(ord(letter)).rjust(3, '0')

                # set the string value to int
                keyInt = int(keyInt)
                # y = key^e mod(n)
                ciphertext = BigExp(keyInt, n, mode=mode, p=p, q=q) ** e
                print(f"\nYour encrypted value is:\n{ciphertext}")
                # save the time for calculating encrypt value
                end("Calculate encrypt value")
                # write records again, first parameter indicates to write(True) the log.txt, or append(False)
                # this case is append
                writeRecords(False)

            elif input_text == 'de':
                value = input("Input value to decrypt: ")
                start()
                value = int(value)

                # message = y ^ d
                plaintext = BigExp(value, n, mode=mode, p=p, q=q) ** d

                # just steps from the bottom to top of encryption,
                # same function of steps, but difference order
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













