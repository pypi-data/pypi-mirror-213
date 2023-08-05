
class mnmct:
    def test(testnum):
        print(f'test {str(testnum)} passed')
        return f'test {str(testnum)} passed'

    def xor(a, b):
        return (a and (not b)) or (b and (not a))

    def nor(a, b):
        return not (a or b)

    def nand(a, b):
        return not (a and b)

    def xnor(a, b):
        return not ((a and (not b)) or (b and (not a)))

    def proccesscode(rmvspc, code):
        if rmvspc:
            code = code.replace(' ', '')
            
        return code.split('\n').remove('')

    class generalgates:
        class gates:
            def __init__(self):
                self.in1 = False
                self.in2 = False
                self.out = False


        class and_gate(gates):
            def update(self):
                self.out = self.in1 and self.in2
                print(f'out: {self.out}, in1: {self.in1}, in2: {self.in2}')

        class or_gate(gates):
            def update(self):
                self.out = self.in1 or self.in2
                print(f'out: {self.out}, in1: {self.in1}, in2: {self.in2}')

        class not_gate(gates):
            def update(self):
                self.out = not self.in1
                print(f'out: {self.out}, in1: {self.in1}')

        class nor_gate(gates):
            def update(self):
                self.out = not (self.in1 or self.in2)
                print(f'out: {self.out}, in1: {self.in1}, in2: {self.in2}')

        class nand_gate(gates):
            def update(self):
                self.out = not (self.in1 and self.in2)
                print(f'out: {self.out}, in1: {self.in1}, in2: {self.in2}')

        class xor_gate(gates):
            def update(self):
                self.out = (self.in1 and not self.in2) or (not self.in1 and self.in2)
                print(f'out: {self.out}, in1: {self.in1}, in2: {self.in2}')

        class xnor_gate(gates):
            def update(self):
                self.out = not ((self.in1 and not self.in2) or (not self.in1 and self.in2))
                print(f'out: {self.out}, in1: {self.in1}, in2: {self.in2}')

        class buffer(gates):
            def update(self):
                self.out = self.in1
                print(f'out: {self.out}, in1: {self.in1}')