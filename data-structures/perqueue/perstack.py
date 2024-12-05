class stackEntry:
    def __init__(self, value, prev, sz):
        self.val = value
        self.sz = sz
        self.prev = prev

    def __str__(self):
        return f"{self.val}"


class perStack:
    def __init__(self):
        self.stack = [stackEntry(None, None, 0)]

    def empty(self, t):
        return self.stack[t].sz == 0

    def size(self, t):
        return self.stack[t].sz

    def next_ver(self):
        return len(self.stack) - 1

    def push(self, t, value):
        if len(self.stack) <= t:
            return
        prev = self.stack[t]
        self.stack.append(stackEntry(value, prev, prev.sz + 1))

    def pop(self, t):
        if self.stack[t] == self.stack[0]:
            self.stack.append(self.stack[t])
            return self.stack[0]
        self.stack.append(self.stack[t].prev)
        return self.stack[t]

    def __str__(self):
        return f"{[str(x) for x in self.stack]}"
