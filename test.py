class A:
    def __init__(self, a):
        self.a = a


class B(A):
    def __init__(self, a):
        A.__init__(self, a)

    def thing(self):
        print(self.a)


b = B(1)
b.thing()