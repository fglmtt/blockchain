import hashlib
import time


class Block:
    def __init__(self, previous_hash: str, data: str) -> None:
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0
        self.hash = self.compute_hash()

    def __str__(self) -> str:
        return (
            f"{self.nonce} {self.previous_hash[:8]} {self.hash[:8]} "
            f"{self.data}"
        )

    def compute_hash(self) -> str:
        return sha256(str(self.nonce) + self.previous_hash + self.data)

    def mine(self, difficulty: int) -> None:
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.compute_hash()


class Blockchain:
    def __init__(self, difficulty: int = 0) -> None:
        self.difficulty = difficulty
        genesis_block = Block("0" * 64, "Genesis")
        genesis_block.mine(difficulty)
        self.blocks = [genesis_block]

    def __str__(self) -> str:
        return "\n".join(str(block) for block in self.blocks)

    def add(self, data: str) -> None:
        block = Block(self.blocks[-1].hash, data)
        block.mine(self.difficulty)
        self.blocks.append(block)

    def head(self) -> str:
        return self.blocks[-1].hash

    def is_valid(self) -> bool:
        for i, block in enumerate(self.blocks):
            if block.hash != block.compute_hash():
                return False
            if i > 0 and block.previous_hash != self.blocks[i - 1].hash:
                return False
            if not block.hash.startswith("0" * self.difficulty):
                return False
        return True


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def solve(data: str, difficulty: int) -> int:
    nonce = 0
    while not sha256(data + " " + str(nonce)).startswith("0" * difficulty):
        nonce += 1
    return nonce


def tamper(chain: Blockchain, index: int, data: str) -> None:
    if not 0 <= index < len(chain.blocks):
        raise IndexError("index out of range")
    chain.blocks[index].data = data
    for i in range(index, len(chain.blocks)):
        if i > 0:
            chain.blocks[i].previous_hash = chain.blocks[i - 1].hash
        chain.blocks[i].hash = chain.blocks[i].compute_hash()


def main() -> None:
    print("=== §1.1. Hashing ===")
    print(sha256("Fox"), end="\n\n")

    print("=== §1.2. Blocks ===")
    genesis_block = Block("0" * 64, "Genesis")
    next_block = Block(genesis_block.hash, "Alice pays Bob 17 coins")
    print(genesis_block)
    print(next_block, end="\n\n")

    print("=== §1.3. Chain of blocks ===")
    chain = Blockchain()
    chain.add("Alice pays Bob 17 coins")
    chain.add("Alice pays David 6 coins")
    chain.add("David and Alice pay Carol 8 coins")
    print(chain, end="\n\n")

    print("=== §1.4. Tampering with a single block ===")
    print("chain is valid:", chain.is_valid())
    block = chain.blocks[1]
    print("block[1]: data before tampering:", block.data)
    print("block[1]: hash before tampering:", block.hash[:8])
    block.data = "Alice pays Bob 170 coins"
    print("block[1]: data after tampering:", block.data)
    print("block[1]: hash after tampering:", block.compute_hash()[:8])
    print("chain is valid:", chain.is_valid(), end="\n\n")

    print("=== §1.4. Restoring block data ===")
    block.data = "Alice pays Bob 17 coins"
    print("block[1]: restored data:", block.data)
    print("chain is valid:", chain.is_valid(), end="\n\n")

    print("=== §1.4. Tampering with a block and subsequent blocks ===")
    head = chain.head()
    print("chain head before tampering:", head[:8])
    print("chain before tampering:")
    print(chain)
    tamper(chain, 1, "Alice pays Bob 170 coins")
    print("chain after tampering:")
    print(chain)
    print("chain is valid:", chain.is_valid())
    print("head is unchanged:", chain.head() == head, end="\n\n")

    print("=== §2.1. Hash puzzles ===")
    print("difficulty 3, nonce:", solve("Fox", 3))
    print("difficulty 4, nonce:", solve("Fox", 4), end="\n\n")

    print("=== §2.2. Mining a block ===")
    block = Block("0" * 64, "Genesis")
    print("block before mining:", block)
    block.mine(4)
    print("block after mining:", block, end="\n\n")

    print("=== §2.2. Mining a chain of blocks ===")
    chain = Blockchain(4)
    chain.add("Alice pays Bob 17 coins")
    chain.add("Alice pays David 6 coins")
    chain.add("David and Alice pay Carol 8 coins")
    print(chain)
    print("chain is valid:", chain.is_valid(), end="\n\n")

    print("=== §2.3. Difficulty ===")
    for difficulty in range(1, 6):
        start = time.perf_counter()
        chain = Blockchain(difficulty)
        chain.add("Alice pays Bob 17 coins")
        chain.add("Alice pays David 6 coins")
        chain.add("David and Alice pay Carol 8 coins")
        elapsed = time.perf_counter() - start
        print(f"difficulty {difficulty}: {round(elapsed, 3)} s")


if __name__ == "__main__":
    main()
