import math
import random
from Crypto.PublicKey import RSA

primeNumbers = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
    109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
    173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
    293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
    367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431,
    433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
    499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
    577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
    643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
    719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
    797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
    863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
    947, 953, 967, 971, 977, 983, 991, 997]


def PrimeTest(number):
    return MillerRabinPrimeTest(number)


# Just a method found in
# https://www.geeksforgeeks.org/analysis-different-methods-find-prime-number-python/
def EasyPrimeTest(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n > 2 and n % 2 == 0:
        return False

    max_div = math.floor(math.sqrt(n))
    for i in range(3, 1 + max_div, 2):
        if n % i == 0:
            return False
    return True


def MillerRabinPrimeTest(n):
    if n in primeNumbers:
        return True
    k = 4
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # witness loop
    for i in range(k):
        gotoWitness = False
        a = random.randrange(2, n-2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for j in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                gotoWitness = True

        if gotoWitness is False:
            return False

    return True


def GCD(a, b):
    # get which is smaller and larger
    large, small = (a, b) if a > b else (b, a)
    if small == 0:
        return large
    else:
        return GCD(small, large % small)


if __name__ == "__main__":
    for i in range(100000):
        key = RSA.generate(1024)

        if MillerRabinPrimeTest(key.p) is False:
            print(f"Number is not prime: {key.p}")

        if MillerRabinPrimeTest(key.q) is False:
            print(f"Number is not prime: {key.q}")

