# Hands-on

## Table of contents

- [1. Data structure](#1-data-structure)
    - [1.1. Hashing](#11-hashing)
    - [1.2. Blocks](#12-blocks)
    - [1.3. Chain of blocks](#13-chain-of-blocks)
    - [1.4. Tamper evidence](#14-tamper-evidence)
- [2. Proof of work](#2-proof-of-work)
    - [2.1. Hash puzzles](#21-hash-puzzles)
    - [2.2. Mining](#22-mining)
    - [2.3. Difficulty](#23-difficulty)
- [3. Implementation](#3-implementation)
- [Licenses](#licenses)

## 1. Data structure

### 1.1. Hashing

Python computes [SHA-256](building-blocks.md#2-hash-functions) with the `hashlib` module, which is part of the standard library.

Create a file called `toychain.py`. Write a function `sha256` that encodes `data` as UTF-8 (`str.encode`) and computes its SHA-256 hash (`hashlib.sha256`). The result is a hash object, whose method `hexdigest` returns the hash as a hexadecimal string. The function `sha256` returns this string.

```python
import hashlib


def sha256(data: str) -> str:
    # TODO
    pass


def main() -> None:
    print("=== §1.1. Hashing ===")
    print(sha256("Fox"), end="\n\n")


if __name__ == "__main__":
    main()
```

If `sha256` is correct, it prints the same hash as in the [example](building-blocks.md#2-hash-functions) of hash functions

```
=== §1.1. Hashing ===
f55bd2cdfae7972827638f3691a5bc189199d7cff7188d5ead489afdea0e5403
```

### 1.2. Blocks

A block has some data and a [hash pointer](building-blocks.md#3-hash-pointers) to the previous block, that is, the hash of the previous block. It also has its own hash, which the next block points to. For simplicity, consider the data as a string in place of the [Merkle tree of transactions](bitcoin.md#13-bitcoins-ledger).

The first block of a chain is the genesis block. It has no previous block, so its previous hash is a string of 64 zeros.

Write a class `Block` whose method `compute_hash` joins `previous_hash` and `data` into a single string and returns its hash (`sha256`). The constructor computes the hash of the block by calling `compute_hash`. The method `__str__` returns a readable representation of a block for printing (`print`). It joins the first 8 characters of `previous_hash`, the first 8 characters of `hash`, and `data`, separated by spaces.

> [!note]
> From now on, each step shows the whole `toychain.py`, where `...` stands for code that you have already written. Keep your code, do not replace it with `...`.

```python
import hashlib


class Block:
    def __init__(self, previous_hash: str, data: str) -> None:
        self.previous_hash = previous_hash
        self.data = data
        self.hash = self.compute_hash()

    def __str__(self) -> str:
        # TODO
        pass

    def compute_hash(self) -> str:
        # TODO
        pass


def sha256(data: str) -> str: ...


def main() -> None:
    ...

    print("=== §1.2. Blocks ===")
    genesis_block = Block("0" * 64, "Genesis")
    next_block = Block(genesis_block.hash, "Alice pays Bob 17 coins")
    print(genesis_block)
    print(next_block, end="\n\n")


if __name__ == "__main__":
    main()
```

If `compute_hash` and `__str__` are correct, it prints

```
...

=== §1.2. Blocks ===
00000000 ec141dc1 Genesis
ec141dc1 8c657dc5 Alice pays Bob 17 coins
```

### 1.3. Chain of blocks

A chain starts with the genesis block. Each later block points to the previous one, as in a [tamper-evident log](building-blocks.md#31-tamper-evident-logs). The most recent block is the head.

Write a class `Blockchain` that keeps its blocks in the attribute `blocks`. The method `__str__` returns a readable representation of the chain for printing (`print`), with one block per line (`str`). The method `add` creates a new block (`Block`) that points to the hash of the last block and appends it to the list (`list.append`). The method `head` returns the hash of the last block.

```python
import hashlib


class Block: ...


class Blockchain:
    def __init__(self) -> None:
        self.blocks = [Block("0" * 64, "Genesis")]

    def __str__(self) -> str:
        # TODO
        pass

    def add(self, data: str) -> None:
        # TODO
        pass

    def head(self) -> str:
        # TODO
        pass


def sha256(data: str) -> str: ...


def main() -> None:
    ...

    print("=== §1.3. Chain of blocks ===")
    chain = Blockchain()
    chain.add("Alice pays Bob 17 coins")
    chain.add("Alice pays David 6 coins")
    chain.add("David and Alice pay Carol 8 coins")
    print(chain, end="\n\n")


if __name__ == "__main__":
    main()
```

The data of the blocks are the payments of the [transaction-based ledger](bitcoin.md#12-transaction-based-ledger) example. If `add` and `__str__` are correct, it prints

```
...

=== §1.3. Chain of blocks ===
00000000 ec141dc1 Genesis
ec141dc1 8c657dc5 Alice pays Bob 17 coins
8c657dc5 c9c0bb8f Alice pays David 6 coins
c9c0bb8f 73721767 David and Alice pay Carol 8 coins
```

### 1.4. Tamper evidence

For simplicity, consider a chain valid if

- Every block, genesis included, has a hash equal to the one computed from its contents
- Every block after the genesis block has a previous hash equal to the hash of the block before it

In Bitcoin, nodes also check that all the transactions in a block are [valid](bitcoin.md#22-simplified-consensus).

Write the method `is_valid` of `Blockchain`. It iterates over the blocks together with their positions (`enumerate`), and for each block compares `hash` with the result of `compute_hash`. Unless the block is the genesis block, it also compares `previous_hash` with the hash of the block before it. It returns `False` as soon as a comparison fails, and `True` otherwise.

```python
import hashlib


class Block: ...


class Blockchain:
    def __init__(self) -> None: ...

    def __str__(self) -> str: ...

    def add(self, data: str) -> None: ...

    def head(self) -> str: ...

    def is_valid(self) -> bool:
        # TODO
        pass


def sha256(data: str) -> str: ...


def main() -> None:
    ...

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


if __name__ == "__main__":
    main()
```

The adversary [tampers with the data of a block](building-blocks.md#31-tamper-evident-logs), so the hash of block 1 no longer matches its data. Restoring the data makes the chain valid again. If `is_valid` is correct, it prints

```
...

=== §1.4. Tampering with a single block ===
chain is valid: True
block[1]: data before tampering: Alice pays Bob 17 coins
block[1]: hash before tampering: 8c657dc5
block[1]: data after tampering: Alice pays Bob 170 coins
block[1]: hash after tampering: 62e86380
chain is valid: False

=== §1.4. Restoring block data ===
block[1]: restored data: Alice pays Bob 17 coins
chain is valid: True
```

Let us assume the adversary also tampers with the hash pointers, up to the [most recent block](building-blocks.md#31-tamper-evident-logs).

Write a function `tamper` that replaces the data of the block at position `index`. Then, from that block to the last one (`range`, `len`), it points each block, unless it is the genesis block, to the hash of the block before it (`previous_hash`) and recomputes its hash (`compute_hash`).

```python
import hashlib


class Block: ...


class Blockchain: ...


def sha256(data: str) -> str: ...


def tamper(chain: Blockchain, index: int, data: str) -> None:
    if not 0 <= index < len(chain.blocks):
        raise IndexError("index out of range")
    # TODO


def main() -> None:
    ...

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


if __name__ == "__main__":
    main()
```

The chain is valid again, but the head has changed. Since we remembered the head, we can still detect that someone tampered with the chain. If `tamper` is correct, it prints

```
...

=== §1.4. Tampering with a block and subsequent blocks ===
chain head before tampering: 73721767
chain before tampering:
00000000 ec141dc1 Genesis
ec141dc1 8c657dc5 Alice pays Bob 17 coins
8c657dc5 c9c0bb8f Alice pays David 6 coins
c9c0bb8f 73721767 David and Alice pay Carol 8 coins
chain after tampering:
00000000 ec141dc1 Genesis
ec141dc1 62e86380 Alice pays Bob 170 coins
62e86380 0db830b4 Alice pays David 6 coins
0db830b4 9248d116 David and Alice pay Carol 8 coins
chain is valid: True
head is unchanged: False
```

## 2. Proof of work

### 2.1. Hash puzzles

Hash functions are [puzzle friendly](building-blocks.md#21-security-properties): there is no strategy better than trying one input after another until the hash meets the target.

In Bitcoin, the block header hash, read as a number, must be smaller than a target. A smaller target makes the puzzle harder. A simplified way to make the target smaller is to require more leading zeros. Here, the difficulty is the number of zeros the hash must start with. For example, if you try `Fox 1`, `Fox 2`, and so on, the first hash that starts with `000` is for `Fox 11667`. The first hash that starts with `0000` is for `Fox 94388`.

Write a function `solve` that joins `data`, a space, and a nonce (`str`) into a single string, starting from nonce 0 and increasing it by 1, until the hash (`sha256`) starts with `difficulty` zeros (`str.startswith`). The function `solve` returns this nonce.

```python
import hashlib


class Block: ...


class Blockchain: ...


def sha256(data: str) -> str: ...


def solve(data: str, difficulty: int) -> int:
    # TODO
    pass


def tamper(chain: Blockchain, index: int, data: str) -> None: ...


def main() -> None:
    ...

    print("=== §2.1. Hash puzzles ===")
    print("difficulty 3, nonce:", solve("Fox", 3))
    print("difficulty 4, nonce:", solve("Fox", 4), end="\n\n")


if __name__ == "__main__":
    main()
```

If `solve` is correct, it prints

```
...

=== §2.1. Hash puzzles ===
difficulty 3, nonce: 11667
difficulty 4, nonce: 94388
```

### 2.2. Mining

To create a block, a node must find a nonce such that the hash of the block falls within the [target space](bitcoin.md#51-hash-puzzles). Here, the target space is the set of hashes that start with `difficulty` zeros. Each hexadecimal digit has 16 possible values, so the target space is $\frac{1}{16^{\text{difficulty}}}$ of the output space, and a node has to try around $16^{\text{difficulty}}$ nonces.

Add the attribute `nonce` to `Block`, and update `compute_hash` so that it joins the nonce (`str`), `previous_hash`, and `data`, in this order, as in $H(nonce \mid prev \mid TX_1 \mid \dots \mid TX_N)$. Update `__str__` so that it also returns the nonce, before the hashes. Write the method `mine`, which increases the nonce by 1 and recomputes the hash (`compute_hash`) until the hash starts with `difficulty` zeros (`str.startswith`).

```python
import hashlib


class Block:
    def __init__(self, previous_hash: str, data: str) -> None:
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0
        self.hash = self.compute_hash()

    def __str__(self) -> str:
        # TODO
        pass

    def compute_hash(self) -> str:
        # TODO
        pass

    def mine(self, difficulty: int) -> None:
        # TODO
        pass


class Blockchain: ...


def sha256(data: str) -> str: ...


def solve(data: str, difficulty: int) -> int: ...


def tamper(chain: Blockchain, index: int, data: str) -> None: ...


def main() -> None:
    ...

    print("=== §2.2. Mining a block ===")
    block = Block("0" * 64, "Genesis")
    print("block before mining:", block)
    block.mine(4)
    print("block after mining:", block, end="\n\n")


if __name__ == "__main__":
    main()
```

If `__str__`, `compute_hash`, and `mine` are correct, it prints

```
...

=== §2.2. Mining a block ===
block before mining: 0 00000000 da62e697 Genesis
block after mining: 99062 00000000 00009b49 Genesis
```

Add the attribute `difficulty` to `Blockchain`. Its default is 0, so the chain built in [§1.3](#13-chain-of-blocks) is still not mined when you run the program again. The constructor mines the genesis block, and the method `add` mines (`mine`) every new block before appending it. Update `is_valid` so it also rejects any block whose hash does not start with `difficulty` zeros.

```python
import hashlib


class Block: ...


class Blockchain:
    def __init__(self, difficulty: int = 0) -> None:
        self.difficulty = difficulty
        genesis_block = Block("0" * 64, "Genesis")
        genesis_block.mine(difficulty)
        self.blocks = [genesis_block]

    def __str__(self) -> str: ...

    def add(self, data: str) -> None:
        # TODO
        pass

    def head(self) -> str: ...

    def is_valid(self) -> bool:
        # TODO
        pass


def sha256(data: str) -> str: ...


def solve(data: str, difficulty: int) -> int: ...


def tamper(chain: Blockchain, index: int, data: str) -> None: ...


def main() -> None:
    ...

    print("=== §2.2. Mining a chain of blocks ===")
    chain = Blockchain(4)
    chain.add("Alice pays Bob 17 coins")
    chain.add("Alice pays David 6 coins")
    chain.add("David and Alice pay Carol 8 coins")
    print(chain)
    print("chain is valid:", chain.is_valid(), end="\n\n")


if __name__ == "__main__":
    main()
```

If `add` and `is_valid` are correct, it prints

```
...

=== §2.2. Mining a chain of blocks ===
99062 00000000 00009b49 Genesis
7878 00009b49 0000cd7a Alice pays Bob 17 coins
8369 0000cd7a 0000e442 Alice pays David 6 coins
26107 0000e442 0000e545 David and Alice pay Carol 8 coins
chain is valid: True
```

### 2.3. Difficulty

Every additional zero makes the target space smaller, and mining slower on average.

Measure how long it takes to build the chain of [§2.2](#22-mining) with difficulty from 1 to 5 (`range`). Take the time before and after (`time.perf_counter`) and print the difference rounded to 3 decimals (`round`).

```python
import hashlib
import time


class Block: ...


class Blockchain: ...


def sha256(data: str) -> str: ...


def solve(data: str, difficulty: int) -> int: ...


def tamper(chain: Blockchain, index: int, data: str) -> None: ...


def main() -> None:
    ...

    print("=== §2.3. Difficulty ===")
    for difficulty in range(1, 6):
        # TODO
        pass


if __name__ == "__main__":
    main()
```

The times depend on the computer. For example

```
...

=== §2.3. Difficulty ===
difficulty 1: 0.0 s
difficulty 2: 0.0 s
difficulty 3: 0.006 s
difficulty 4: 0.079 s
difficulty 5: 2.238 s
```

> [!question] Try difficulty 6. How long would you expect it to take?

> [!note]
> Bitcoin keeps the target space such that the whole network, which computes around $10^{21}$ hashes per second, [creates a new block every 10 minutes](bitcoin.md#51-hash-puzzles) on average.

## 3. Implementation

A possible implementation is in [`code/toychain.py`](../code/toychain.py).

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
