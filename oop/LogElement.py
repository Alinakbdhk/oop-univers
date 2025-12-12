class TLogElement:
    def __init__(self):
        self.__in1 = False
        self.__in2 = False
        self._res = False
        self.__nextEl = None
        self.__nextIn = 0
        if not hasattr(self, "calc"):
            raise NotImplementedError
    def link(self, nextEl, nextIn):
        self.__nextEl = nextEl
        self.__nextIn = nextIn
    def __setIn1(self, newIn1):
        self.__in1 = newIn1
        self.calc()
        if self.__nextEl:
            if self.__nextIn == 1:
                self.__nextEl.In1 = self._res
            elif self.__nextIn == 2:
                self.__nextEl.In2 = self._res
    def __setIn2(self, newIn2):
        self.__in2 = newIn2
        self.calc()
        if self.__nextEl:
            if self.__nextIn == 1:
                self.__nextEl.In1 = self._res
            elif self.__nextIn == 2:
                self.__nextEl.In2 = self._res
    In1 = property(lambda x: x.__in1, __setIn1)
    In2 = property(lambda x: x.__in2, __setIn2)
    Res = property(lambda x: x._res)

class TNot(TLogElement):
    def __init__(self):
        TLogElement.__init__(self)
    def calc(self):
        self._res = not self.In1

class TLog2In(TLogElement):
    pass

class TAnd(TLog2In):
    def __init__(self):
        TLog2In.__init__(self)
    def calc(self):
        self._res = self.In1 and self.In2

class TOr(TLog2In):
    def __init__(self):
        TLog2In.__init__(self)
    def calc(self):
        self._res = self.In1 or self.In2

el1 = TNot()
el2 = TNot()
el3 = TAnd()
el4 = TAnd()
el5 = TOr()
el1.link(el3, 1)
el2.link(el4, 2)
el3.link(el5, 1)
el4.link(el5, 2)
print(f"a b Xor")
for i in range(2):
    for j in range(2):
        el1.In1 = i
        el2.In1 = j
        el3.In2 = j
        el4.In1 = i
        print(f"{i} {j} {int(el5.Res)}")