# BIP39 Seed Phrase Scanner

This tool generates random BIP39 seed phrases (12, 18, and 24 words) using the standard wordlist from `words.txt`, derives Bitcoin addresses from them, and checks if those addresses match any in `btc.txt`.

## Features

- **Multi-length seed phrases**: Generates 12, 18, and 24 word phrases
- **Parallel processing**: Uses CPU multiprocessing for faster scanning
- **GPU support**: Option for GPU acceleration (requires PyCUDA)
- **Match detection**: Saves matches to `FOUND.txt` with address, seed phrase, and private key
- **Resume capability**: Can be stopped and restarted (no persistence tracking yet)

## Files Required

- `words.txt`: BIP39 wordlist (2048 words)
- `btc.txt`: List of target Bitcoin addresses to check against

## Usage

### Option 1: Run BIP39 Scanner Only
```batch
BIP39_Scanner.bat
```

### Option 2: Choose from Main Menu
```batch
00BatchAttack.bat
```
Then select option [2] for BIP39 scanner.

## GPU Acceleration

To enable GPU support:
1. Install PyCUDA: `pip install pycuda`
2. Set `USE_GPU = True` in `bip39_scanner.py`
3. Ensure you have CUDA-compatible GPU and drivers

Note: GPU implementation is currently a placeholder and requires custom CUDA kernel development for full acceleration.

## Output Format

When matches are found, they're saved to `FOUND.txt`:

```
Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Seed Phrase: abandon ability able about above absent absorb abstract absurd abuse access accident
Private Key (HEX): abc123def456...
--------------------------------------------------------------------------------
```

## Performance

- CPU: Uses all available cores with multiprocessing
- GPU: Placeholder for CUDA acceleration (much faster potential)

The scanner runs continuously until manually stopped (Ctrl+C).