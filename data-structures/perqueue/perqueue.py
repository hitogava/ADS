from perstack import perStack


class queueEntry:
    def __init__(
        self,
        lVer,
        rVer,
        lPrimeVer,
        sVer,
        rcVer,
        rcPrimeVer,
        recopy,
        popCnt,
        phase,
        prev,
    ):
        self.lVer = lVer
        self.rVer = rVer
        self.lPrimeVer = lPrimeVer
        self.sVer = sVer
        self.rcVer = rcVer
        self.rcPrimeVer = rcPrimeVer
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
        self.queue = [queueEntry(0, 0, 0, 0, 0, 0, False, 0, 0, None)]
        self.l = perStack()
        self.lPrime = perStack()
        self.r = perStack()
        self.s = perStack()
        self.rc = perStack()
        self.rcPrime = perStack()

    def makeNewVersion(self, vFrom):
        q = self.queue[vFrom].copy()
        q.prev = self
        return q

    def makeRecopySteps(self, q):
        for _ in range(3):
            self.makeRecopyStep(q)

    def makeRecopyStep(self, q: queueEntry):
        if q.phase == 1:
            if not self.r.empty(q.rVer):
                x = self.r.pop(q.rVer)
                q.rVer += 1

                self.s.push(q.sVer, x.val)
                q.sVer += 1
                return
            q.phase = 2

        if q.phase == 2:
            if not self.l.empty(q.lVer):
                x = self.l.pop(q.lVer)
                q.lVer += 1

                self.r.push(q.rVer, x.val)
                q.rVer += 1

                self.rcPrime.push(q.rcPrimeVer, x.val)
                q.rcPrimeVer += 1

                return
            q.phase = 3

        if q.phase == 3:
            if self.s.empty(q.sVer):
                q.phase = 4
                q.recopy = False
                q.popCnt = 0
                # swap ( L, L' )
                self.l, self.lPrime = self.lPrime, self.l
                q.lVer, q.lPrimeVer = q.lPrimeVer, q.lVer

                # swap ( Rc, Rc' )
                self.rc, self.rcPrime = self.rcPrime, self.rc
                q.rcVer, q.rcPrimeVer = q.rcPrimeVer, q.rcVer

                # q.rcPrimeVer = 0

            else:
                x = self.s.pop(q.sVer)
                q.sVer += 1
                if q.popCnt <= self.s.size:
                    self.r.push(q.rVer, x.val)
                    q.rVer += 1

                    self.rcPrime.push(q.rcPrimeVer, x.val)
                    q.rcPrimeVer += 1

    def checkRecopy(self, q: queueEntry):
        if self.l.size > self.r.size:
            q.recopy = True
            q.popCnt = 0
            q.phase = 1
            self.makeRecopySteps(q)

    def push(self, v, x):
        q = self.makeNewVersion(v)
        if not q.recopy:
            if not self.rcPrime.empty(q.rcPrimeVer):
                _ = self.rcPrime.pop(q.rcPrimeVer)
                # q.rcPrimeVer = self.rcPrime.next_ver()
                q.rcPrimeVer += 1
            self.l.push(q.lVer, x)
            q.lVer += 1
            self.checkRecopy(q)
        else:
            self.lPrime.push(q.lPrimeVer, x)
            q.lPrimeVer += 1
            self.makeRecopySteps(q)

        self.queue.append(q)

    def pop(self, v):
        q = self.makeNewVersion(v)
        x = None
        if not q.recopy:
            x = self.r.pop(q.rVer)
            q.rVer += 1

            if not self.rcPrime.empty(q.rcPrimeVer):
                _ = self.rcPrime.pop(q.rcPrimeVer)
                q.rcPrimeVer += 1

            _ = self.rc.pop(q.rcVer)
            q.rcVer += 1

            self.checkRecopy(q)
        else:
            x = self.rc.pop(q.rcVer)
            q.rcVer += 1

            q.popCnt += 1

            if self.s.size < q.popCnt:
                x = self.r.pop(q.rVer)
                q.rVer += 1
                print(q.rcPrimeVer)
                if not self.rcPrime.empty(q.rcPrimeVer):
                    _ = self.rcPrime.pop(q.rcPrimeVer)
                    q.rcPrimeVer += 1

            self.makeRecopySteps(q)

        self.queue.append(q)
        return x

    def print(self, v):
        q = self.queue[v]
        print(f"Version {v}, recopy={q.recopy}:")
        print(f"{q.lVer} L: {self.l.stack[q.lVer]}")
        print(f"{q.lPrimeVer} L': {self.lPrime.stack[q.lPrimeVer]}")
        print(f"{q.rVer} R: {self.r.stack[q.rVer]}")
        print(f"{q.sVer} S: {self.s.stack[q.sVer]}")
        print(f"{q.rcVer} Rc: {self.rc.stack[q.rcVer]}")
        print(f"{q.rcPrimeVer} Rc': {self.rcPrime.stack[q.rcPrimeVer]}")
