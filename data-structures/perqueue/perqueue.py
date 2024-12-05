from perstack import perStack
from enum import Enum


class tuple:
    def __init__(self, x, y):
        self.ver = x
        self.type = y

    def copy(self):
        return tuple(self.ver, self.type)

    def __str__(self):
        return f"{self.ver} {self.type}"


class StackType(Enum):
    DEFAULT = 0
    PRIME = 1


class queueEntry:
    def __init__(
        self,
        lVer=tuple(0, StackType.DEFAULT),
        rVer=tuple(0, StackType.DEFAULT),
        lPrimeVer=tuple(0, StackType.PRIME),
        sVer=tuple(0, StackType.DEFAULT),
        rcVer=tuple(0, StackType.DEFAULT),
        rcPrimeVer=tuple(0, StackType.PRIME),
        recopy=False,
        popCnt=0,
        phase=0,
        prev=None,
    ):
        self.lVer = lVer.copy()
        self.rVer = rVer.copy()
        self.lPrimeVer = lPrimeVer.copy()
        self.sVer = sVer.copy()
        self.rcVer = rcVer.copy()
        self.rcPrimeVer = rcPrimeVer.copy()
        self.recopy = recopy
        self.popCnt = popCnt
        self.phase = phase
        self.prev = prev

    def copy(self):
        return queueEntry(
            self.lVer,
            self.rVer,
            self.lPrimeVer,
            self.sVer,
            self.rcVer,
            self.rcPrimeVer,
            self.recopy,
            self.popCnt,
            self.phase,
            self.prev,
        )


class perQueue:
    def __init__(self):
        self.queue = [queueEntry()]
        self.l = perStack()
        self.lPrime = perStack()
        self.r = perStack()
        self.s = perStack()
        self.rc = perStack()
        self.rcPrime = perStack()

    def __rcPush(self, q, x):
        ver, dest = q.ver, q.type
        newVer = None
        if dest == StackType.DEFAULT:
            self.rc.push(ver, x)
            newVer = self.rc.next_ver()
        elif dest == StackType.PRIME:
            self.rcPrime.push(ver, x)
            newVer = self.rcPrime.next_ver()
        q.ver = newVer

    def __rcPop(self, q):
        ver, dest = q.ver, q.type
        x = None
        newVer = None
        if dest == StackType.DEFAULT:
            x = self.rc.pop(ver)
            newVer = self.rc.next_ver()
        elif dest == StackType.PRIME:
            x = self.rcPrime.pop(ver)
            newVer = self.rcPrime.next_ver()
        q.ver = newVer
        return x

    def __lPush(self, q, x):
        ver, dest = q.ver, q.type
        newVer = None
        if dest == StackType.DEFAULT:
            self.l.push(ver, x)
            newVer = self.l.next_ver()
        elif dest == StackType.PRIME:
            self.lPrime.push(ver, x)
            newVer = self.lPrime.next_ver()
        q.ver = newVer

    def __lPop(self, q):
        ver, dest = q.ver, q.type
        x = None
        newVer = None
        if dest == StackType.DEFAULT:
            x = self.l.pop(ver)
            newVer = self.l.next_ver()
        elif dest == StackType.PRIME:
            x = self.lPrime.pop(ver)
            newVer = self.lPrime.next_ver()
        q.ver = newVer
        return x

    def __rPush(self, q, x):
        self.r.push(q.ver, x)
        q.ver = self.r.next_ver()

    def __rPop(self, q):
        x = self.r.pop(q.ver)
        q.ver = self.r.next_ver()
        return x

    def __sPush(self, q, x):
        self.s.push(q.ver, x)
        q.ver = self.s.next_ver()

    def __sPop(self, q):
        x = self.s.pop(q.ver)
        q.ver = self.s.next_ver()
        return x

    def __lSize(self, t):
        return (
            self.l.size(t.ver)
            if t.type == StackType.DEFAULT
            else self.lPrime.size(t.ver)
        )

    def __rcSize(self, t):
        return (
            self.rc.size(t.ver)
            if t.type == StackType.DEFAULT
            else self.rcPrime.size(t.ver)
        )

    def makeNewVersion(self, vFrom):
        q = self.queue[vFrom].copy()
        q.prev = self
        return q

    def makeRecopySteps(self, q):
        for _ in range(3):
            self.makeRecopyStep(q)

    def makeRecopyStep(self, q: queueEntry):
        if q.phase == 1:
            if not self.r.empty(q.rVer.ver):
                x = self.__rPop(q.rVer)
                self.__sPush(q.sVer, x.val)
                return
            q.phase = 2

        if q.phase == 2:
            if self.__lSize(q.lVer):
                x = self.__lPop(q.lVer)
                self.__rPush(q.rVer, x.val)
                self.__rcPush(q.rcPrimeVer, x.val)
                return
            q.phase = 3

        if q.phase == 3:
            if self.s.empty(q.sVer.ver):
                q.phase = 4
                q.recopy = False
                q.popCnt = 0
                # swap ( L, L' )
                q.lVer, q.lPrimeVer = q.lPrimeVer, q.lVer

                # swap ( Rc, Rc' )
                q.rcVer, q.rcPrimeVer = q.rcPrimeVer, q.rcVer

            else:
                x = self.__sPop(q.sVer)
                if q.popCnt <= self.s.size(q.sVer.ver):
                    self.__rPush(q.rVer, x.val)
                    self.__rcPush(q.rcPrimeVer, x.val)

    def checkRecopy(self, q: queueEntry):
        if self.__lSize(q.lVer) > self.r.size(q.rVer.ver):
            q.recopy = True
            q.popCnt = 0
            q.phase = 1
            self.makeRecopySteps(q)

    def push(self, v, x):
        q = self.makeNewVersion(v)
        if not q.recopy:
            if self.__rcSize(q.rcPrimeVer):
                self.__rcPop(q.rcPrimeVer)
            self.__lPush(q.lVer, x)
            self.checkRecopy(q)
        else:
            self.__lPush(q.lPrimeVer, x)
            self.makeRecopySteps(q)

        self.queue.append(q)

    def pop(self, v):
        q = self.makeNewVersion(v)
        x = queueEntry()
        if not q.recopy:
            x = self.__rPop(q.rVer)
            if self.__rcSize(q.rcPrimeVer):
                self.__rcPop(q.rcPrimeVer)
            if self.__rcSize(q.rcVer):
                self.__rcPop(q.rcVer)
            self.checkRecopy(q)
        else:
            x = self.__rcPop(q.rcVer)
            q.popCnt += 1
            # if self.s.size(q.sVer.ver) <= q.popCnt:
            if self.s.size(q.sVer.ver) < q.popCnt:
                self.__rPop(q.rVer)
            if self.__rcSize(q.rcPrimeVer):
                self.__rcPop(q.rcPrimeVer)
            self.makeRecopySteps(q)
        self.queue.append(q)
        return x

    def print(self, v):
        q = self.queue[v]
        print(f"Version {v}, recopy={q.recopy}:")
        print(f"{q.lVer} L: {self.l.stack[q.lVer.ver]}")
        print(f"{q.lPrimeVer} L': {self.lPrime.stack[q.lPrimeVer.ver]}")
        print(f"{q.rVer} R: {self.r.stack[q.rVer.ver]}")
        print(f"{q.sVer} S: {self.s.stack[q.sVer.ver]}")
        print(f"{q.rcVer} Rc: {self.rc.stack[q.rcVer.ver]}")
        print(f"{q.rcPrimeVer} Rc': {self.rcPrime.stack[q.rcPrimeVer.ver]}")
