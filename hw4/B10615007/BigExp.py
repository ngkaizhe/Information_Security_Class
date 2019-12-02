from Euler import EulerPhiFunc
from Time import start, end


class BigExp(object):
    def __init__(self, number, mod_range, mode="NOR", p=None, q=None):
        self.mode = mode
        self.mod_range = mod_range
        self.baseNum = number % mod_range
        self.p = p
        self.q = q
        # print(self.p, "now is q ", self.q)

    def __pow__(self, power, modulo=None):
        if self.mode == "NOR":
            return self._normal(power)
        elif self.mode == "SAM":
            return self._SAM(power)
        elif self.mode == "CRT":
            return self._CRT(power)

    def _normal(self, power):
        PhiN = EulerPhiFunc(self.mod_range, self.p, self.q)
        if power == -1:
            power += PhiN

        return pow(self.baseNum % self.mod_range, power % PhiN) % self.mod_range

    def _SAM(self, power):
        PhiN = EulerPhiFunc(self.mod_range, self.p, self.q)
        if power == -1:
            power += PhiN

        powerBin = bin(power % PhiN)[2:]
        baseN = 1
        f = open("Square_and_Multiply.txt", "w+")
        i = 0

        while i < len(powerBin):
            f.write(f"Step: {i+1}a\n\t")
            f.write(f"{(baseN % self.mod_range)} * {(baseN % self.mod_range)} % {self.mod_range} =")
            baseN = ((baseN % self.mod_range) * (baseN % self.mod_range)) % self.mod_range
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

        PhiN = EulerPhiFunc(self.mod_range, self.p, self.q)
        if power == -1:
            power += PhiN

        # separate to 2 parts
        f = open("CRT.txt", "w+")
        f.write("==================\n")
        f.write(f"Calculating: ({self.baseNum} ** {power})mod({self.mod_range})\n")

        # first part for p
        start()
        a1 = BigExp(self.baseNum, self.p, mode="SAM") ** power
        m1 = self.q
        y1 = BigExp(m1, self.p, mode="SAM") ** -1
        first = (a1 % self.mod_range * m1 % self.mod_range * y1 % self.mod_range) % self.mod_range
        f.write(f"a1 = {a1}, m1 = {m1}, y1 = {y1}\n")
        end("First part of CRT: ")

        # second part for q
        start()
        a2 = BigExp(self.baseNum, self.q, mode="SAM") ** power
        m2 = self.p
        y2 = BigExp(m2, self.q, mode="SAM") ** -1
        second = (a2 % self.mod_range * m2 % self.mod_range * y2 % self.mod_range) % self.mod_range
        f.write(f"a2 = {a2}, m2 = {m2}, y2 = {y2}\n")
        f.write(f"Answer is: {(first + second) % self.mod_range}\n")
        f.write("==================\n")
        end("Second part of CRT: ")

        return (first + second) % self.mod_range

    def __str__(self):
        return f"{self.baseNum}"


if __name__ == "__main__":
    N = 3293
    en_text = 2494
    d = 2987
    p = 37
    q = 89
    pl = BigExp(en_text, N, mode="CRT", p=p, q=q) ** d
    print(pl)