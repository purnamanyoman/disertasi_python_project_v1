import hashlib
import random

class CuckooFilter:
    def __init__(self, capacity=1000, bucket_size=4, fingerprint_size=16, max_kicks=100):
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.fingerprint_size = fingerprint_size
        self.max_kicks = max_kicks
        self.num_buckets = max(2, capacity // bucket_size)
        self.buckets = [[] for _ in range(self.num_buckets)]

    def _fingerprint(self, item: str) -> str:
        digest = hashlib.md5(item.encode()).hexdigest()
        return digest[: max(1, self.fingerprint_size // 4)]

    def _hash(self, value: str) -> int:
        return int(hashlib.md5(value.encode()).hexdigest(), 16)

    def _index1(self, item: str) -> int:
        return self._hash(item) % self.num_buckets

    def _index2(self, index1: int, fp: str) -> int:
        return (index1 ^ self._hash(fp)) % self.num_buckets

    def insert(self, item: str) -> bool:
        fp = self._fingerprint(item)
        i1 = self._index1(item)
        i2 = self._index2(i1, fp)

        if len(self.buckets[i1]) < self.bucket_size:
            self.buckets[i1].append(fp)
            return True
        if len(self.buckets[i2]) < self.bucket_size:
            self.buckets[i2].append(fp)
            return True

        i = random.choice([i1, i2])
        for _ in range(self.max_kicks):
            j = random.randrange(len(self.buckets[i]))
            self.buckets[i][j], fp = fp, self.buckets[i][j]
            i = self._index2(i, fp)
            if len(self.buckets[i]) < self.bucket_size:
                self.buckets[i].append(fp)
                return True
        return False

    def contains(self, item: str) -> bool:
        fp = self._fingerprint(item)
        i1 = self._index1(item)
        i2 = self._index2(i1, fp)
        return fp in self.buckets[i1] or fp in self.buckets[i2]
