def GCD(a, b):
    # get which is smaller and larger
    large, small = (a, b) if a > b else (b, a)
    if small == 0:
        return large
    else:
        return GCD(small, large % small)


def EulerPhiFunc(n, p=None, q=None, isPrime=False):
    if p is not None and q is not None:
        return (p-1) * (q-1)
    if isPrime:
        return n-1

    # bruto force
    # return BFPhi(n)

    # Euler's product formula
    return EPPhi(n)


def BFPhi(n):
    # 1 is always a relatively prime number for every number
    result = 1
    for i in range(2, n):
        if GCD(i, n) == 1:
            result += 1
    return result


# https://www.geeksforgeeks.org/optimized-euler-totient-function-multiple-evaluations/
def EPPhi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1

    if n > 1:
        result -= result // n
    return result


if __name__ == "__main__":
    print(f"phi({154681043064895080}) = {EulerPhiFunc(154681043064895080)}\n")
    print(f"phi({2415423688769381937042135215966800702356}) = {EulerPhiFunc(2415423688769381937042135215966800702356)}\n")
