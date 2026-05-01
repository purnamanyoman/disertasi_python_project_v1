import math
import hashlib

class BloomFilter:
    def __init__(self, n_items: int, fp_rate: float):
        if n_items <= 0:
            raise ValueError("n_items harus > 0")
        if not (0 < fp_rate < 1):
            raise ValueError("fp_rate harus di antara 0 dan 1")
        self.n_items = n_items
        self.fp_rate = fp_rate
        self.size = self.get_size(n_items, fp_rate)
        self.hash_count = max(1, self.get_hash_count(self.size, n_items))
        self.bit_array = [0] * self.size

    @staticmethod
    def get_size(n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return max(1, int(m))

    @staticmethod
    def get_hash_count(m: int, n: int) -> int:
        k = (m / n) * math.log(2)
        return int(k)

    def _hashes(self, item: str):
        results = []
        for i in range(self.hash_count):
            data = f"{item}_{i}".encode()
            digest = hashlib.md5(data).hexdigest()
            idx = int(digest, 16) % self.size
            results.append(idx)
        return results

    def add(self, item: str) -> None:
        for idx in self._hashes(item):
            self.bit_array[idx] = 1

    def contains(self, item: str) -> bool:
        return all(self.bit_array[idx] == 1 for idx in self._hashes(item))
