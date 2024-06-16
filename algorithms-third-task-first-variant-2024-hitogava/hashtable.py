import enum, math, random
from avltree import AVLTree, TNode
from llist import DoublyLinkedList, LNode, Pair
from primelib import MillerRabin, primes


class BucketTypes(enum.Enum):
    BUCKET_LLIST = 0
    BUCKET_BST = 1


class Bucket:
    def __init__(self, bucket, bucket_type=BucketTypes.BUCKET_LLIST) -> None:
        self.bucket_type = bucket_type
        self.bucket = bucket

    def insert(self, key, value, **kwargs):
        if self.bucket_type == BucketTypes.BUCKET_LLIST:
            node = LNode(Pair(key, value))
            self.bucket.add_head(node)
        elif self.bucket_type == BucketTypes.BUCKET_BST:
            node = TNode(key, value)
            self.bucket.insert(node)

    def remove(self, node):
        self.bucket.remove(node)

    def find(self, key):
        return self.bucket.find(key)

    def get_size(self):
        if self.bucket_type == BucketTypes.BUCKET_LLIST:
            return self.bucket.n
        return self.bucket.root.size

    def __iter__(self):
        return iter(self.bucket)

    def __str__(self):
        return str(self.bucket)


def hash(key, a, m):
    h = 0
    for i in range(len(key)):
        h = (h + ord(key[i]) * (a**i)) % m
    return h


def binary_search(value, array=primes, left=0, right=len(primes) - 1):
    if right < left:
        return array[left]
    m = (left + right) // 2
    if value < array[m]:
        return binary_search(value, array, left, m - 1)
    return binary_search(value, array, m + 1, right)


def nearest_prime(value):
    if value < primes[-1]:
        return binary_search(value)

    # because of Chebyshev theorem: n < p < 2 * n, where p is prime
    for i in range(value, value * 2):
        if MillerRabin(i):
            return i


class HashTable:
    def __init__(self, m_index=10, chlimit=math.inf, load_factor=0.75) -> None:
        self.m_index = m_index # index of m in primes list
        self.m = primes[self.m_index]
        self.n = 0
        self.hash_constant = random.randint(0, self.m)
        self.load_factor = load_factor
        self.chain_limit = chlimit
        self.htable = [None for _ in range(self.m)]

    def __getitem__(self, key):
        h = hash(key, self.hash_constant, self.m)
        return self.htable[h]

    def __setitem__(self, key, value):
        h = hash(key, self.hash_constant, self.m)
        self.htable[h] = value

    def find(self, key):
        if self[key]:
            return self[key].find(key)
        return None

    def rehash(self):
        buffer = self.htable.copy()
        self.__init__(self.m_index + 1)
        for bucket in buffer:
            if bucket:
                for node in bucket:
                    self.insert(node.pair.key, node.pair.value)

    def remove(self, key):
        bucket = self[key]
        if bucket:
            for n in bucket:
                if n.pair.key == key:
                    bucket.remove(n)
                    self.n -= 1
                    return n
        return None

    def insert(self, key, value):
        assert self.n <= self.m
        if self.n / self.m >= self.load_factor:
            self.rehash()
        if not self[key]:
            self[key] = Bucket(DoublyLinkedList())
            self[key].insert(key, value)
        else:
            b = self[key]
            b.insert(key, value)
            if (
                b.get_size() >= self.chain_limit
                and b.bucket_type == BucketTypes.BUCKET_LLIST
            ):
                self[key] = Bucket(AVLTree(None, b.bucket), BucketTypes.BUCKET_BST)
        self.n += 1

    def __iter__(self):
        for key in self.htable:
            yield key
