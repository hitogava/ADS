class stackEntry:
    def __init__(self, value, prev):
        self.val = value
        self.prev = prev

    def __str__(self):
        return f"{self.val}"


class perStack:
    def __init__(self):
        self.stack = [stackEntry(None, None)]
        self.size = 0

    def empty(self, t):
        return self.stack[t] == self.stack[0]

    def top(self, t):
        return self.stack[t]

    def next_ver(self):
        return len(self.stack) - 1

    def push(self, t, value):
        if len(self.stack) <= t:
            return
        self.stack.append(stackEntry(value, self.stack[t]))
        self.size += 1

    def pop(self, t):
        if len(self.stack) <= t:
            return self.stack[0]
        self.size = max(0, self.size - 1)
        self.stack.append(self.stack[t].prev)
        return self.stack[t]

    def __str__(self):
        return f"{[str(x) for x in self.stack]}"
