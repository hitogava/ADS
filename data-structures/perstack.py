import copy


class stackEntry:
    def __init__(self, value, prev):
        self.value = value
        self.prev = prev

    def __str__(self):
        return f"{self.value}; {self.prev.value if self.prev else None}"


class perstack:
    def __init__(self):
        self.stack = [stackEntry(None, None)]
        self.size = 0

    def empty(self):
        return self.size == 0

    def top(self, t):
        return self.stack[t]

    def push(self, t, value):
        if len(self.stack) <= t:
            return
        self.stack.append(stackEntry(value, self.stack[t]))
        self.size += 1

    def pop(self, t):
        if len(self.stack) <= t:
            return None
        self.size -= 1
        self.stack.append(self.stack[t].prev)
        return self.stack[t]

    def print(self, t):
        if len(self.stack) <= t:
            return
        curr = self.stack[-1]
        while curr:
            print(curr.value)
            curr = curr.prev


class pentaqueue:
    def __init__(
        self,
        stackVersions=None,
        l=perstack(),
        lPrime=perstack(),
        r=perstack(),
        rPrime=perstack(),
        s=perstack(),
        recopy=False,
        toCopy=0,
        copied=False,
    ):
        if stackVersions:
            self.stackVersions = stackVersions
        else:
            self.stackVersions = [0] * 5
        self.l = l
        self.lPrime = lPrime

        self.r = r
        self.rPrime = rPrime

        self.s = s

        self.recopy = recopy
        self.toCopy = toCopy
        self.copied = copied

    def copy(self):
        stackVersions = copy.deepcopy(self.stackVersions)
        return pentaqueue(
            stackVersions,
            self.l,
            self.lPrime,
            self.r,
            self.rPrime,
            self.s,
            self.recopy,
            self.toCopy,
            self.copied,
        )

    def additionalOperations(self):
        toDo = 3
        curCopied = self.copied
        newVersions = copy.deepcopy(self.stackVersions)
        while not curCopied and toDo > 0 and not self.r.empty():
            x = self.r.pop(newVersions[2])
            self.s.push(newVersions[4], x)
            newVersions[2] += 1
            newVersions[4] += 1
            toDo -= 1
        while toDo > 0 and not self.l.empty():
            curCopied = True
            x = self.l.pop(newVersions[0])
            self.r.push(newVersions[2], x)
            print([str(x) for x in self.r.stack])
            newVersions[0] += 1
            newVersions[2] += 1
            toDo -= 1

        curCopy = self.toCopy
        while toDo > 0 and not self.s.empty():
            x = self.s.pop(newVersions[4])
            newVersions[4] += 1
            if curCopy > 0:
                self.r.push(newVersions[2], x)
                newVersions[2] += 1
                curCopy -= 1
            toDo -= 1

        self.stackVersions = newVersions
        if self.s.empty():
            self.l, self.lPrime = self.lPrime, self.l
            self.stackVersions[0], self.stackVersions[1] = (
                self.stackVersions[1],
                self.stackVersions[0],
            )
        self.toCopy = curCopy
        return self

    def checkNormal(self):
        return self.additionalOperations()

    def checkRecopy(self):
        if self.l.size > self.r.size:
            self.recopy = True
            self.toCopy = self.r.size
            self.copied = False
            return self.checkNormal()
        self.recopy = False
        return self

    def push(self, t, value):
        if not self.recopy:
            self.l.push(t, value)
            qPrime = self.copy()
            qPrime.stackVersions[0] += 1
            return qPrime.checkRecopy()
        else:
            self.lPrime.push(t, value)
            qPrime = self.copy()
            qPrime.stackVersions[1] += 1
            return qPrime.checkNormal()

    def pop(self, t):
        if not self.recopy:
            x = self.r.pop(t)
            qPrime = self.copy()
            qPrime.stackVersions[2] += 1
            return qPrime.checkRecopy(), x
        else:
            newVersions = copy.deepcopy(self.stackVersions)
            x = self.rPrime.pop(t)
            newVersions[3] += 1
            curCopy = self.toCopy
            if self.toCopy > 0:
                curCopy -= 1
            else:
                x = self.r.pop(t)
                newVersions[2] += 1
            qPrime = self.copy()
            qPrime.stackVersions = newVersions
            qPrime.toCopy = curCopy
            return qPrime.checkNormal(), x


vs = [pentaqueue()]
vs.append(vs[-1].push(0, 1))
vs.append(vs[-1].push(1, 2))
vs.append(vs[-1].push(2, 3))
vs.append(vs[-1].push(3, 4))
print(vs)
print(vs[-1].pop(3)[1])
