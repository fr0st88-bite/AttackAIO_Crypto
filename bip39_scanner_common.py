#!/usr/bin/env python3
"""Shared BIP39 scanner support for multiple blockchains."""

import hashlib
import os
import random
import multiprocessing as mp
import queue
from typing import Dict, List

from hdwallet import HDWallet
from hdwallet.mnemonics import BIP39Mnemonic
from hdwallet.cryptocurrencies import (
    Bitcoin,
    BitcoinCash,
    BitcoinGold,
    Litecoin,
    Dash,
    DigiByte,
    Dogecoin,
    Qtum,
    Zcash,
    Ethereum,
    Tron,
)
from hdwallet.symbols import BTC, BCH, BTG, LTC, DASH, DGB, DOGE, QTUM, ZEC, ETH, TRX

WORDS_FILE = "words.txt"
FOUND_FILE = "FOUND.txt"
USED_FILE = "used_passphrases.txt"
DEFAULT_SEED_LENGTHS = (12, 18, 24)
DEFAULT_WORKER_COUNT = max(1, mp.cpu_count() - 1)

CHAIN_CONFIGS = {
    "bitcoin": {
        "cryptocurrency": Bitcoin,
        "symbol": BTC,
        "target_files": ["btc.txt", "bitcoin.txt"],
    },
    "bitcoincash": {
        "cryptocurrency": BitcoinCash,
        "symbol": BCH,
        "target_files": ["bitcoincash.txt"],
    },
    "bitcoingold": {
        "cryptocurrency": BitcoinGold,
        "symbol": BTG,
        "target_files": ["bitcoingold.txt"],
    },
    "dash": {
        "cryptocurrency": Dash,
        "symbol": DASH,
        "target_files": ["dash.txt"],
    },
    "digibyte": {
        "cryptocurrency": DigiByte,
        "symbol": DGB,
        "target_files": ["digibyte.txt"],
    },
    "doge": {
        "cryptocurrency": Dogecoin,
        "symbol": DOGE,
        "target_files": ["doge.txt"],
    },
    "ethereum": {
        "cryptocurrency": Ethereum,
        "symbol": ETH,
        "target_files": ["ethereum.txt"],
    },
    "litecoin": {
        "cryptocurrency": Litecoin,
        "symbol": LTC,
        "target_files": ["litecoin.txt"],
    },
    "qtum": {
        "cryptocurrency": Qtum,
        "symbol": QTUM,
        "target_files": ["qtum.txt"],
    },
    "tron": {
        "cryptocurrency": Tron,
        "symbol": TRX,
        "target_files": ["tron.txt"],
    },
    "zcash": {
        "cryptocurrency": Zcash,
        "symbol": ZEC,
        "target_files": ["zcash.txt"],
    },
}


class BIP39SeedGenerator:
    @staticmethod
    def _bytes_to_bits(data: bytes) -> str:
        return "".join(f"{byte:08b}" for byte in data)

    @staticmethod
    def generate_seed_phrase(words: List[str], length: int) -> str:
        if length not in (12, 18, 24):
            raise ValueError("Supported seed lengths are 12, 18, or 24 words.")
        entropy_bytes = {12: 16, 18: 24, 24: 32}[length]
        entropy = os.urandom(entropy_bytes)
        checksum_length = entropy_bytes * 8 // 32
        entropy_bits = BIP39SeedGenerator._bytes_to_bits(entropy)
        checksum = BIP39SeedGenerator._bytes_to_bits(hashlib.sha256(entropy).digest())[:checksum_length]
        bits = entropy_bits + checksum
        phrase_words = []
        for i in range(0, len(bits), 11):
            index = int(bits[i : i + 11], 2)
            phrase_words.append(words[index])
        return " ".join(phrase_words)


def load_wordlist() -> List[str]:
    if not os.path.exists(WORDS_FILE):
        raise FileNotFoundError(f"{WORDS_FILE} not found. Place the BIP39 English wordlist in the repository.")
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
    if len(words) != 2048:
        raise ValueError(f"{WORDS_FILE} must contain 2048 BIP39 words.")
    return words


def find_target_file(chain_name: str) -> str:
    config = CHAIN_CONFIGS.get(chain_name.lower())
    if not config:
        raise ValueError(f"Unsupported blockchain: {chain_name}")
    for candidate in config["target_files"]:
        if os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(
        f"No target file found for {chain_name}. Create one of: {', '.join(config['target_files'])}"
    )


def load_targets(target_file: str) -> set:
    with open(target_file, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip() and not line.strip().startswith("#"))


def load_used_passphrases() -> set:
    if os.path.exists(USED_FILE):
        with open(USED_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def add_to_used(passphrase: str) -> None:
    with open(USED_FILE, "a", encoding="utf-8") as f:
        f.write(passphrase + "\n")


def save_found(result: Dict[str, str]) -> None:
    with open(FOUND_FILE, "a", encoding="utf-8") as f:
        f.write(f"Blockchain: {result['blockchain']}\n")
        f.write(f"Address: {result['address']}\n")
        f.write(f"Seed Phrase: {result['seed_phrase']}\n")
        f.write(f"Private Key (HEX): {result['private_key']}\n")
        f.write(f"Target File: {result['target_file']}\n")
        f.write("-" * 80 + "\n\n")


def derive_address_from_seed(seed_phrase: str, cryptocurrency, symbol: str):
    mnemonic = BIP39Mnemonic(mnemonic=seed_phrase)
    hdwallet = HDWallet(cryptocurrency=cryptocurrency, symbol=symbol)
    hdwallet.from_mnemonic(mnemonic)
    return hdwallet.address(), hdwallet.private_key()


def check_seed_phrase(seed_phrase: str, chain_name: str, crypto_class, symbol: str, targets: set, target_file: str, found_queue: mp.Queue):
    address, private_key = derive_address_from_seed(seed_phrase, crypto_class, symbol)
    if address and address in targets:
        result = {
            "blockchain": chain_name,
            "address": address,
            "seed_phrase": seed_phrase,
            "private_key": private_key,
            "target_file": target_file,
        }
        found_queue.put(result)
        return True
    return False


def worker_process(chain_name: str, crypto_class, symbol: str, words: List[str], seed_lengths: List[int], targets: set, target_file: str, found_queue: mp.Queue, stop_event: mp.Event, worker_id: int):
    checked = 0
    while not stop_event.is_set():
        length = random.choice(seed_lengths)
        seed_phrase = BIP39SeedGenerator.generate_seed_phrase(words, length)
        if check_seed_phrase(seed_phrase, chain_name, crypto_class, symbol, targets, target_file, found_queue):
            print(f"[Worker {worker_id}] FOUND {chain_name.upper()} match: {seed_phrase}")
        checked += 1
        if checked % 1000 == 0:
            print(f"[Worker {worker_id}] {chain_name.upper()} checked {checked} {length}-word phrases...")


def run_chain_scanner(chain_name: str, seed_lengths: List[int] = None, worker_count: int = None) -> None:
    chain_name = chain_name.lower()
    config = CHAIN_CONFIGS.get(chain_name)
    if config is None:
        raise ValueError(f"Unsupported blockchain: {chain_name}")
    words = load_wordlist()
    target_file = find_target_file(chain_name)
    targets = load_targets(target_file)
    if not targets:
        raise ValueError(f"Target file {target_file} is empty. Please add one address per line.")
    seed_lengths = seed_lengths or list(DEFAULT_SEED_LENGTHS)
    worker_count = worker_count or DEFAULT_WORKER_COUNT

    print(f"Starting BIP39 scan for {chain_name.upper()}")
    print(f"Wordlist: {WORDS_FILE}")
    print(f"Target file: {target_file}")
    print(f"Worker count: {worker_count}")
    print(f"Checking seed lengths: {', '.join(str(l) for l in seed_lengths)}")
    print("Press Ctrl+C to stop.")

    found_queue = mp.Manager().Queue()
    stop_event = mp.Manager().Event()
    processes = []
    for worker_id in range(worker_count):
        process = mp.Process(
            target=worker_process,
            args=(
                chain_name,
                config["cryptocurrency"],
                config["symbol"],
                words,
                seed_lengths,
                targets,
                target_file,
                found_queue,
                stop_event,
                worker_id + 1,
            ),
        )
        process.daemon = True
        process.start()
        processes.append(process)

    try:
        while True:
            try:
                result = found_queue.get(timeout=1)
                save_found(result)
                print(f"FOUND {result['blockchain'].upper()} address {result['address']} saved to {FOUND_FILE}")
            except queue.Empty:
                if not any(p.is_alive() for p in processes):
                    break
    except KeyboardInterrupt:
        print("Stopping scanner...")
        stop_event.set()
    finally:
        stop_event.set()
        for process in processes:
            process.join(timeout=2)
        while True:
            try:
                result = found_queue.get_nowait()
                save_found(result)
            except queue.Empty:
                break
    print("Scanner stopped.")


def run_from_cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run BIP39 seed phrase scanner for a specific blockchain.")
    parser.add_argument("chain", nargs="?", choices=list(CHAIN_CONFIGS.keys()), default="bitcoin", help="Blockchain to scan")
    parser.add_argument("--workers", type=int, default=None, help="Number of worker processes to use")
    parser.add_argument("--lengths", type=str, default="12,18,24", help="Comma-separated seed lengths to check")
    args = parser.parse_args()
    lengths = [int(x) for x in args.lengths.split(",") if x.strip()]
    run_chain_scanner(args.chain, seed_lengths=lengths, worker_count=args.workers)


if __name__ == "__main__":
    run_from_cli()
