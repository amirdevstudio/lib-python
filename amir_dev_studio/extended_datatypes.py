class Number(float):
    def is_between(self, num1: float, num2: float):
        num1, num2 = sorted([num1, num2])
        return num1 <= self <= num2

    def rounded(self, precision: int = 0):
        return round(self, precision)
