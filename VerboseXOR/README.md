░█──░█ ░█▀▀▀ ░█▀▀█ ░█▀▀█ ░█▀▀▀█ ░█▀▀▀█ ░█▀▀▀ ▀▄░▄▀ ░█▀▀▀█ ░█▀▀█ \
─░█░█─ ░█▀▀▀ ░█▄▄▀ ░█▀▀▄ ░█──░█ ─▀▀▀▄▄ ░█▀▀▀ ─░█── ░█──░█ ░█▄▄▀ \
──▀▄▀─ ░█▄▄▄ ░█─░█ ░█▄▄█ ░█▄▄▄█ ░█▄▄▄█ ░█▄▄▄ ▄▀░▀▄ ░█▄▄▄█ ░█─░█

# VERBOSE XOR

VERBOSEXOR is a small educational Python tool (interactive) that demonstrates
how XOR (exclusive-or) works on integers, binary strings and simple XOR-based
encryption using an 8-bit key.

---

**Installation**

- Requires Python 3.7+.
- Recommended (install dependencies):

```powershell
python -m pip install --upgrade pip
pip install colorama pyperclip
```

`colorama` is used for colored terminal output. `pyperclip` is used to copy
keys and ciphertext/plaintext to the clipboard for convenience.

There is no additional packaging — just [download](https://github.com/user-attachments/files/24074380/VerboseXOR.py) and run the `VerboseXOR.py` script.

---

**How to use**

Run the script from the folder where it lives:

```powershell
python VerboseXOR.py
```

The script presents an interactive menu. Supported actions (type one of these
and press Enter):

- `int` — interactive verbose XOR on two integers (decimal). Shows binary
  padding and per-bit steps.
- `list` — provide two comma-separated integer lists (equal length assumed);
  the script XORs pairs and prints results for each pair.
- `bin` — (new) provide two binary strings and see step-by-step binary XOR.
- `encrypt` — XOR-based demonstration encrypt: XORs every plaintext byte with
  an 8-bit key; outputs base64 ciphertext and copies ciphertext and key to
  clipboard.
- `decrypt` — provide base64 ciphertext and the 8-bit key to recover the
  original plaintext (if UTF-8). The tool prints the steps and copies the
  plaintext to the clipboard.
- `help` — prints a colorful explanation of XOR and the available actions.

Notes:
- The `encrypt`/`decrypt` features use a single 8-bit key (one byte) purposely
  to keep the demonstration simple and reversible: XORing with the same key
  twice returns the original data.
- Ciphertext is represented in base64 to make it safe for copying/pasting.

---

**Detailed explanation of functions (with code snippets)**

This section explains every XOR-related function in `VerboseXOR.py`. The code
snippets below mirror the key parts of each function and explain the logic.

---

### `verbose_decimal_xor(dec1, dec2)`

Purpose: Translate two non-negative integers to binary (both padded to the
same width), then perform and print a per-bit XOR with colored output.

Core steps and sample snippet:

```python
# choose bit width from the maximum value
max_val = max(dec1, dec2)
length = max_val.bit_length()

bin1 = decimal_to_padded_binary(dec1, length)
bin2 = decimal_to_padded_binary(dec2, length)

result = []
for i in range(length):
    bit_a = int(bin1[i])
    bit_b = int(bin2[i])
    xor_result_bit = bit_a ^ bit_b
    # print a colored step describing the XOR for that bit
    print(f"Bit {i+1}: {bit_a} ^ {bit_b} = {xor_result_bit}")
    result.append(str(xor_result_bit))

final_bin = ''.join(result)
final_dec = int(final_bin, 2)
```

Notes:
- The width used is the bit-length of the larger value, so both numbers are
  represented with just enough bits to show the highest set bit.
- The function returns the decimal value of the XOR result for convenience.

---

### `inputXOR_list()`

Purpose: Accept two comma-separated lists of integers, converts them to
integer lists, then calls `verbose_decimal_xor` on each corresponding pair.

Snippet:

```python
list1 = [int(x.strip()) for x in list1_input.split(',')]
list2 = [int(x.strip()) for x in list2_input.split(',')]

for num1, num2 in zip(list1, list2):
    result = verbose_decimal_xor(num1, num2)
    print('->', result)
```

Notes:
- This function uses `zip`, so if the lists differ in length, elements past the
  shorter list's end are ignored.
- Each pair is processed with the same detailed, verbose output as the
  `verbose_decimal_xor` function.

---

### `XOR_binary()` (action name: `bin`)  

Purpose: Perform verbose XOR on two binary strings directly (added in this
release). It validates input, left-pads both strings to equal length and
prints per-bit XOR steps.

Snippet:

```python
# sanitize and validate inputs
b1 = input(...).strip().replace(' ', '')
b2 = input(...).strip().replace(' ', '')
if not (all(ch in '01' for ch in b1) and all(ch in '01' for ch in b2)):
    print('Invalid binary input')
    return

length = max(len(b1), len(b2))
bin1 = b1.zfill(length)
bin2 = b2.zfill(length)

result = []
for i in range(length):
    bit_a = int(bin1[i])
    bit_b = int(bin2[i])
    xor_result_bit = bit_a ^ bit_b
    print(f"Bit {i+1}: {bit_a} ^ {bit_b} = {xor_result_bit}")
    result.append(str(xor_result_bit))

final_bin = ''.join(result)
```

Notes:
- The function copies the final binary result to the clipboard for convenience.
- It returns the binary string result.

---

### `XOR_ENCRYPT()` and `XOR_DECRYPT()`

These two functions demonstrate a simple reversible XOR-based cipher where
every byte of the plaintext is XORed with the same single-byte key (8 bits).
This is intentionally basic for teaching.

Encryption steps (snippet):

```python
content_bytes = content.encode('utf-8')
# key_byte is an integer 0..255 from the 8-bit binary key
encrypted_bytes = bytes([b ^ key_byte for b in content_bytes])
# present ciphertext as base64 so it can be copied/pasted safely
encrypted_b64 = base64.b64encode(encrypted_bytes).decode('ascii')
```

Decryption steps (snippet):

```python
encrypted_bytes = base64.b64decode(encrypted_text)
decoded_bytes = bytes([b ^ key_byte for b in encrypted_bytes])
plaintext = decoded_bytes.decode('utf-8')
```

Security note:
- Using a single byte key repeated over an entire plaintext is *not* secure
  for real-world cryptographic purposes. This is strictly an educational
  demonstration to show how XOR is reversible and how key reuse works.

---

**License & Author**

This repository belongs to the author shown in the script. This README is
intended as usage and educational documentation for `VerboseXOR.py`.

---


