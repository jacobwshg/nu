import functools as ft

def intl_call(code1, code2):
    return code1 != code2

class Caller:
    def __init__(self, name, code, number, callees):
        self.name = name
        self.code = code
        self.number = number
        self.callees = callees

    def count(self):
        '''
        return 1 + \
            0 \
            if not self.callees \
            else ft.reduce(lambda cnt, cle:cnt + cle.count(), \
                           self.callees, \
                           0)
        '''
        count = 1
        if self.callees:
            for cle in self.callees:
                count += cle.count()
        return count

    def count_intl_calls(self):
        num_icalls = 0
        for cle in self.callees:
            num_icalls += 1 if intl_call(self.code, cle.code) else 0
            num_icalls += cle.count_intl_calls()
        return num_icalls

class CallTree:
    def __init__(self, root_caller):
        self.root_caller = root_caller

    def count(self):
        return self.root_caller.count()

    def count_intl_calls(self):
        return self.root_caller.count_intl_calls()

denise = Caller('Denise', 886, '04-123-456-789', [])
candice = Caller('Candice', 33, '04 22 11 44 78', [])
charlie = Caller('Charlie', 886, '02-888-888-888', [denise])
carl = Caller('Carl', 1, '212-489-4608', [])
betty = Caller('Betty', 33, '01 02 03 04 05', [charlie, candice])
bob = Caller('Bob', 1, '414-897-0495', [carl])
alice = Caller('Alice', 1, '312-867-5309', [bob, betty])

calltree = CallTree(alice)

if __name__ == '__main__':
    print(f'Number of people in call tree: {calltree.count()}')
    print(f'Number of intl calls: {calltree.count_intl_calls()}')


