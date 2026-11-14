# Hands-on

## Table of contents

- [1. Hash chain of blocks](#1-hash-chain-of-blocks)
    - [1.1. Hashing](#11-hashing)
    - [1.2. Blocks](#12-blocks)
    - [1.3. Chain](#13-chain)
    - [1.4. Validation](#14-validation)
    - [1.5. Tampering](#15-tampering)
- [2. Proof of work](#2-proof-of-work)
    - [2.1. Hash puzzles](#21-hash-puzzles)
    - [2.2. Mining](#22-mining)
    - [2.3. Difficulty](#23-difficulty)
- [3. Implementation](#3-implementation)
- [Licenses](#licenses)

## 1. Hash chain of blocks

### 1.1. Hashing

Python computes [SHA-256](building-blocks.md#2-hash-functions) with the `hashlib` module, which is part of the standard library.

Create a file called `toychain.py`. Write a function `sha256` that encodes `data` as UTF-8 (`str.encode`), computes its SHA-256 hash (`hashlib.sha256`), and returns the hash as a hexadecimal string (`hexdigest`).

```python
import hashlib


def sha256(data: str) -> str:
    # TODO
    pass


def main() -> None:
    print(sha256("Fox"))


if __name__ == "__main__":
    main()
```

If `sha256` is correct, it prints the same hash as in the [example](building-blocks.md#2-hash-functions) of hash functions

```
f55bd2cdfae7972827638f3691a5bc189199d7cff7188d5ead489afdea0e5403
```

### 1.2. Blocks

A block has some data and a [hash pointer](building-blocks.md#3-hash-pointers) to the previous block, that is, the hash of the previous block. It also has its own hash, which the next block points to. For simplicity, the data is a string in place of the [Merkle tree of transactions](bitcoin.md#13-bitcoins-ledger).

The first block of a chain is the genesis block. It has no previous block, so its previous hash is a string of 64 zeros.

Write a class `Block` whose method `compute_hash` joins `previous_hash` and `data` into a single string and returns its hash (`sha256`). The constructor computes the hash of the block by calling `compute_hash`.

```python
import hashlib


class Block:
    def __init__(self, data: str, previous_hash: str) -> None:
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        # TODO
        pass


def sha256(data: str) -> str: ...


def main() -> None:
    genesis = Block("Genesis", "0" * 64)
    block = Block("Alice pays Bob 17 coins", genesis.hash)
    print(genesis.hash)
    print(block.hash)


if __name__ == "__main__":
    main()
```

> [!note]
> From now on, each step shows the whole `toychain.py`, where `...` stands for code that you have already written. Keep your code, do not replace it with `...`.

If `compute_hash` is correct, it prints

```
ec141dc1ac281e8ca95590bdeaf7c20610063905198e3363a596937d43a94126
8c657dc5739e112b911011a277dc9453826568d447c002efaa7d06b8542f884e
```

### 1.3. Chain

A chain starts with the genesis block. Each later block points to the previous one, as in a [tamper-evident log](building-blocks.md#31-tamper-evident-logs). The most recent block is the head.

Write a class `Blockchain` that keeps its blocks in the attribute `blocks`. The method `add` creates a new block (`Block`) that points to the hash of the last block (`self.blocks[-1].hash`) and appends it to the list (`list.append`). The method `head` returns the hash of the last block.

```python
import hashlib


class Block: ...


class Blockchain:
    def __init__(self) -> None:
        self.blocks = [Block("Genesis", "0" * 64)]

    def add(self, data: str) -> None:
        # TODO
        pass

    def head(self) -> str:
        # TODO
        pass


def sha256(data: str) -> str: ...


def main() -> None:
    chain = Blockchain()
    chain.add("Alice pays Bob 17 coins")
    chain.add("Alice pays David 6 coins")
    chain.add("David and Alice pay Carol 8 coins")
    for block in chain.blocks:
        print(block.hash, block.data)


if __name__ == "__main__":
    main()
```

The data of the blocks are the payments of the [transaction-based ledger](bitcoin.md#12-transaction-based-ledger) example. If `add` is correct, it prints

```
ec141dc1ac281e8ca95590bdeaf7c20610063905198e3363a596937d43a94126 Genesis
8c657dc5739e112b911011a277dc9453826568d447c002efaa7d06b8542f884e Alice pays Bob 17 coins
c9c0bb8f4833a41028921cba71730ba80fb9e363a14735ca34317a42b60791f3 Alice pays David 6 coins
7372176787b84f8e11c921dbf7bbf9742752033d5e42c2163c29c9acf2465f2a David and Alice pay Carol 8 coins
```

### 1.4. Validation

A chain is valid if

- Every block, genesis included, has a hash equal to the one computed from its contents
- Every block after the genesis block has a previous hash equal to the hash of the block before it

Write the method `is_valid` of `Blockchain`. It iterates over the blocks together with their positions (`enumerate`), and for each block compares `hash` with the result of `compute_hash`. Unless the block is the genesis block, it also compares `previous_hash` with the hash of the block before it (`self.blocks[i - 1].hash`). It returns `False` as soon as a comparison fails, and `True` otherwise.

```python
import hashlib


class Block: ...


class Blockchain:
    def __init__(self) -> None: ...

    def add(self, data: str) -> None: ...

    def head(self) -> str: ...

    def is_valid(self) -> bool:
        for i, block in enumerate(self.blocks):
            # TODO
            pass
        return True


def sha256(data: str) -> str: ...


def main() -> None:
    ...
    head = chain.head()
    print("valid:", chain.is_valid())
    chain.blocks[1].data = "Alice pays Bob 170 coins"
    print("valid after changing data:", chain.is_valid())


if __name__ == "__main__":
    main()
```

The adversary [tampers with the data of a block](building-blocks.md#31-tamper-evident-logs), so the hash of block 1 no longer matches its data. If `is_valid` is correct, it prints

```
...
valid: True
valid after changing data: False
```

### 1.5. Tampering

Let us assume the adversary also tampers with the hash pointers, up to the [most recent block](building-blocks.md#31-tamper-evident-logs).

Write a function `tamper` that replaces the data of the block at position `index`. Then, from that block to the last one (`range`, `len`), it points each block to the hash of the block before it (`previous_hash`) and recomputes its hash (`compute_hash`).

```python
import hashlib


class Block: ...


class Blockchain: ...


def sha256(data: str) -> str: ...


def tamper(chain: Blockchain, index: int, data: str) -> None:
    # TODO
    pass


def main() -> None:
    ...
    tamper(chain, 1, "Alice pays Bob 170 coins")
    print("valid after tampering:", chain.is_valid())
    print("head unchanged:", chain.head() == head)


if __name__ == "__main__":
    main()
```

The chain is valid again, but the head has changed. Since we remembered the head, we can still detect that someone tampered with the chain. If `tamper` is correct, it prints

```
...
valid after tampering: True
head unchanged: False
```

## 2. Proof of work

### 2.1. Hash puzzles

Hash functions are [puzzle friendly](building-blocks.md#21-security-properties): there is no strategy better than trying one input after another until the hash meets the target.

In Bitcoin, the block header hash, read as a number, must be smaller than a target. A smaller target makes the puzzle harder. A simplified way to make the target smaller is to require more leading zeros. Here, the difficulty is the number of zeros the hash must start with. For example, if you try `Fox 1`, `Fox 2`, and so on, the first hash that starts with `000` is for `Fox 11667`, which is found after 11667 tries.

Write a function `solve` that joins `data` and a nonce (`str`) into a single string, starting from nonce 0 and increasing it by 1, until the hash (`sha256`) starts with `difficulty` zeros (`str.startswith`). It returns the nonce.

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
    # the space after Fox gives the same inputs as in the lecture
    print(solve("Fox ", 3))


if __name__ == "__main__":
    main()
```

If `solve` is correct, it prints

```
11667
```

### 2.2. Mining

To create a block, a node must find a nonce such that the hash of the block falls within the [target space](bitcoin.md#51-hash-puzzles). Here, the target space is the set of hashes that start with `difficulty` zeros. Each hexadecimal digit has 16 possible values, so the target space is $\frac{1}{16^{\text{difficulty}}}$ of the output space, and a node has to try around $16^{\text{difficulty}}$ nonces.

Add the attribute `nonce` to `Block`, and update `compute_hash` so that it joins the nonce (`str`), `previous_hash`, and `data`, in this order, as in $H(nonce \mid prev \mid TX_1 \mid \dots \mid TX_N)$. Write the method `mine`, which increases the nonce by 1 and recomputes the hash (`compute_hash`) until the hash starts with `difficulty` zeros (`str.startswith`). Then, add the attribute `difficulty` to `Blockchain`. The constructor mines the genesis block, and the method `add` mines (`mine`) every new block before appending it. Update `is_valid` so it also rejects any block whose hash does not start with `difficulty` zeros.

Replace `main` with the version below, since `Blockchain` now requires a difficulty.

```python
import hashlib


class Block:
    def __init__(self, data: str, previous_hash: str) -> None:
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        # TODO
        pass

    def mine(self, difficulty: int) -> None:
        # TODO
        pass


class Blockchain:
    def __init__(self, difficulty: int) -> None:
        self.difficulty = difficulty
        genesis = Block("Genesis", "0" * 64)
        genesis.mine(difficulty)
        self.blocks = [genesis]

    def add(self, data: str) -> None:
        # TODO
        pass

    def head(self) -> str: ...

    def is_valid(self) -> bool: ...


def sha256(data: str) -> str: ...


def solve(data: str, difficulty: int) -> int: ...


def tamper(chain: Blockchain, index: int, data: str) -> None: ...


def main() -> None:
    chain = Blockchain(4)
    chain.add("Alice pays Bob 17 coins")
    chain.add("Alice pays David 6 coins")
    chain.add("David and Alice pay Carol 8 coins")
    for block in chain.blocks:
        print(block.nonce, block.hash, block.data)


if __name__ == "__main__":
    main()
```

With difficulty 4, a node has to try around $16^4 = 65536$ nonces per block. If `mine` and `add` are correct, it prints

```
99062 00009b4974fd6db0a38377088df7791a07aa09ab34cbfc0124868b7e5320d0ed Genesis
7878 0000cd7a68dd702047428595eaa1d6642b890d6247e80f6e685038963b01df56 Alice pays Bob 17 coins
8369 0000e4426e24addce5746d34823ddf90415836d938704dac165992efcc8ab559 Alice pays David 6 coins
26107 0000e545c4e77751101483e046ccd05e4671c469a26b22fd967fc70ff586c881 David and Alice pay Carol 8 coins
```

### 2.3. Difficulty

Every additional zero makes the target space 16 times smaller, and mining 16 times slower on average.

Measure how long it takes to build the chain of [§2.2](#22-mining) with difficulty from 1 to 5 (`range`). Take the time before and after (`time.perf_counter`) and print the difference.

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
    for difficulty in range(1, 6):
        # TODO
        pass


if __name__ == "__main__":
    main()
```

The times depend on the computer. For example

```
...
difficulty 1: 0.000 s
difficulty 2: 0.000 s
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
