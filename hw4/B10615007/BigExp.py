from Euler import EulerPhiFunc


class BigExp(object):
    def __init__(self, number, mod_range, mode="NOR", p=None, q=None,  modIsPrime=True):
        self.mode = mode
        self.mod_range = mod_range
        self.baseNum = number % mod_range
        self.p = p
        self.q = q
        self.modIsPrime = modIsPrime
        # print(self.p, "now is q ", self.q)

    def __pow__(self, power, modulo=None):
        if self.mode == "NOR":
            return self._normal(power)
        elif self.mode == "SAM":
            return self._SAM(power)
        elif self.mode == "CRT":
            return self._CRT(power)

    def _normal(self, power):
        if power == -1:
            return self._mod_inverse()

        PhiN = EulerPhiFunc(self.mod_range, self.p, self.q, isPrime=self.modIsPrime)
        return pow(self.baseNum % self.mod_range, power % PhiN, self.mod_range)

    def _SAM(self, power):
        if power == -1:
            return self._mod_inverse()

        PhiN = EulerPhiFunc(self.mod_range, self.p, self.q, isPrime=self.modIsPrime)
        powerBin = bin(power % PhiN)[2:]
        baseN = 1
        f = open("Square_and_Multiply.txt", "w+")
        i = 0

        while i < len(powerBin):
            f.write(f"Step: {i+1}a\n\t")
            f.write(f"{(baseN % self.mod_range)} * {(baseN % self.mod_range)} % {self.mod_range} =")
            baseN = pow(baseN, 2, self.mod_range)
            f.write(f" {baseN}\n")

            if powerBin[i] == '1':
                f.write(f"Step: {i+1}b\n\t")
                f.write(f"{(baseN % self.mod_range)} * {(self.baseNum % self.mod_range)} % {self.mod_range} =")
                baseN = ((baseN % self.mod_range) * (self.baseNum % self.mod_range)) % self.mod_range
                f.write(f" {baseN}\n")
            elif powerBin[i] == '0':
                baseN *= 1
            i += 1

        return baseN % self.mod_range

    def _CRT(self, power):
        # if p or q is none, cant use CRT then
        if self.p is None or self.q is None:
            return self._SAM(power)

        if power == -1:
            return self._mod_inverse()

        # separate to 2 parts
        f = open("CRT.txt", "w+")
        f.write("==================\n")
        f.write(f"Calculating: ({self.baseNum} ** {power})mod({self.mod_range})\n")

        # first part for p
        a1 = BigExp(self.baseNum, self.p, mode="SAM", modIsPrime=True) ** power
        m1 = self.q
        y1 = BigExp(m1, self.p, mode="SAM") ** -1
        first = (a1 % self.mod_range * m1 % self.mod_range * y1 % self.mod_range) % self.mod_range
        f.write(f"a1 = {a1}, m1 = {m1}, y1 = {y1}\n")

        # second part for q
        a2 = BigExp(self.baseNum, self.q, mode="SAM", modIsPrime=True) ** power
        m2 = self.p
        y2 = BigExp(m2, self.q, mode="SAM") ** -1
        second = (a2 % self.mod_range * m2 % self.mod_range * y2 % self.mod_range) % self.mod_range
        f.write(f"a2 = {a2}, m2 = {m2}, y2 = {y2}\n")
        f.write(f"Answer is: {(first + second) % self.mod_range}\n")
        f.write("==================\n")

        return (first + second) % self.mod_range

    def _mod_inverse(self):
        a = self.baseNum
        m = self.mod_range
        m0 = m
        y = 0
        x = 1

        if m == 1:
            return 0

        while a > 1:
            q = a // m
            t = m
            m = a % m
            a = t
            t = y
            y = x - q * y
            x = t

        if x < 0:
            x += m0

        return x

    def __str__(self):
        return f"{self.baseNum}"


if __name__ == "__main__":
    # N = 3293
    # en_text = 2494
    # d = 2987
    # p = 37
    # q = 89
    # pl = BigExp(en_text, N, mode="CRT", p=p, q=q) ** d
    # print(pl)

    m = 175493943591238731153761981576487237587563120430682983380634739545583505060437983634797758234188782665301047856460669425127576675669630870097934356189228205804254899031631175444380187683740883544450622020030871028339340826290734750020703992014659932656415377396462841997579472522334744615347084637223933264369
    e = 65537
    p = 13152669733197520661105144678155135306170638825259666047837664566693508367641733844992599957362201143260332441781480495139530556148469199390924628542441477
    q = 13342838157662363081845169371286281575177735706631377898976601416107574326702201553692575320711679091407127002106358951360124680143120998966583677771174397
    d = BigExp(e, (p-1) * (q-1), "CRT") ** -1
    print(d)