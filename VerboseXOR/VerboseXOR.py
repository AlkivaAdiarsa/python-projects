# ░█──░█ ░█▀▀▀ ░█▀▀█ ░█▀▀█ ░█▀▀▀█ ░█▀▀▀█ ░█▀▀▀ ▀▄░▄▀ ░█▀▀▀█ ░█▀▀█ 
# ─░█░█─ ░█▀▀▀ ░█▄▄▀ ░█▀▀▄ ░█──░█ ─▀▀▀▄▄ ░█▀▀▀ ─░█── ░█──░█ ░█▄▄▀ 
# ──▀▄▀─ ░█▄▄▄ ░█─░█ ░█▄▄█ ░█▄▄▄█ ░█▄▄▄█ ░█▄▄▄ ▄▀░▀▄ ░█▄▄▄█ ░█─░█



from colorama import Fore, Style, init
import pyperclip
import secrets
import base64

init(autoreset=True)

def decimal_to_padded_binary(decimal_num, length):
    """Converts decimal to binary string and pads with leading zeros."""
    # Convert to binary string, remove '0b' prefix
    binary_str = bin(decimal_num)[2:]
    # Pad to required length
    padded_binary = binary_str.zfill(length)
    return padded_binary

def verbose_decimal_xor(dec1, dec2):
    """
    Translates decimal inputs to binary, performs verbose bitwise XOR,
    and counts the steps.
    """
    # 1. Determine maximum required bit length
    # This ensures both numbers are represented with the same number of bits
    max_val = max(dec1, dec2)
    # Calculate length needed to represent the max value (e.g., max_val=5 needs 3 bits)
    length = max_val.bit_length()
    
    print(f"Translating decimals to padded binary (length {length} bits):\n")
    
    # 2. Translate decimals to padded binary strings
    bin1 = decimal_to_padded_binary(dec1, length)
    bin2 = decimal_to_padded_binary(dec2, length)

    print(f"  Decimal {dec1} -> Binary A: {bin1}")
    print(f"  Decimal {dec2} -> Binary B: {bin2}\n")

    result = []
    steps = 0
    print("Step-by-step comparison (A ^ B):")

    # 3. Perform the verbose bitwise XOR
    for i in range(length):
        bit_a = int(bin1[i])
        bit_b = int(bin2[i])
        
        xor_result_bit = bit_a ^ bit_b
        
        print(f"  Bit {i+1}:{Fore.GREEN} {bit_a} ^ {bit_b} ={Fore.LIGHTGREEN_EX} {xor_result_bit}{Style.RESET_ALL}")
        
        result.append(str(xor_result_bit))
        steps += 1
    
    final_bin_result = "".join(result)
    final_dec_result = int(final_bin_result, 2)
    
    print(f"\nFinal Result (Binary):{Fore.GREEN} {final_bin_result}{Style.RESET_ALL}")
    print(f"Final Result (Decimal):{Fore.CYAN} {final_dec_result}{Style.RESET_ALL}")
    print(f"Total Steps (bit comparisons):{Fore.LIGHTYELLOW_EX} {steps}{Style.RESET_ALL}")
    
    return final_dec_result


print(f"{Fore.GREEN}---" * 21)
print(f"{Fore.GREEN}░█──░█{Fore.RED} ░█▀▀▀{Fore.BLUE} ░█▀▀█ {Fore.MAGENTA}░█▀▀█ ░█▀▀▀█ {Fore.LIGHTBLUE_EX}░█▀▀▀█ ░█▀▀▀ {Fore.YELLOW}▀▄░▄▀ ░█▀▀▀█ ░█▀▀█")
print(f"{Fore.GREEN}─░█░█─{Fore.RED} ░█▀▀▀{Fore.BLUE} ░█▄▄▀ {Fore.MAGENTA}░█▀▀▄ ░█──░█ {Fore.LIGHTBLUE_EX}─▀▀▀▄▄ ░█▀▀▀ {Fore.YELLOW}─░█── ░█──░█ ░█▄▄▀")
print(f"{Fore.GREEN}──▀▄▀─{Fore.RED} ░█▄▄▄{Fore.BLUE} ░█─░█ {Fore.MAGENTA}░█▄▄█ ░█▄▄▄█ {Fore.LIGHTBLUE_EX}░█▄▄▄█ ░█▄▄▄ {Fore.YELLOW}▄▀░▀▄ ░█▄▄▄█ ░█─░█{Style.RESET_ALL}")
print(f"{Fore.GREEN}---" * 21)
print(f"{Fore.RED}VERBOSE XOR{Style.RESET_ALL} Version 1.8")
print("-" * 40)

def help_page():
            print()
            print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "VERBOSEXOR" + Style.RESET_ALL, f"by {Fore.YELLOW}AlkivaAdiarsa{Style.RESET_ALL} - {Fore.BLUE}{link_url}{Style.RESET_ALL}")
            print("-"*40)
            print(f"{Style.BRIGHT}{Fore.CYAN}What is VERBOSEXOR?{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}VERBOSEXOR{Style.RESET_ALL} is an educational tool showing step-by-step XOR operations and simple XOR-based encryption.\n")
            print(f"{Style.BRIGHT}{Fore.MAGENTA}Quick XOR rules:{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}1 XOR 1 = 0{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}1 XOR 0 = 1{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}0 XOR 0 = 0{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}0 XOR 1 = 1{Style.RESET_ALL}\n")
            print(f"{Style.BRIGHT}{Fore.GREEN}Encryption/Decryption in this tool:{Style.RESET_ALL}")
            print(f"  - {Fore.CYAN}encrypt{Style.RESET_ALL}: XORs plaintext bytes with an 8-bit key and returns base64 ciphertext.")
            print(f"  - {Fore.CYAN}decrypt{Style.RESET_ALL}: takes base64 ciphertext and the 8-bit key to recover plaintext.")
            print("-"*40)

def InputXOR():
    print("-" * 40)
    print(f"{Fore.GREEN}VerboseXOR:{Fore.RESET} input XOR")
    decimal1 = int(input("Enter first number:"))
    decimal2 = int(input("Enter Second number:"))
    print("-" * 40)
    verbose_decimal_xor(decimal1, decimal2)
    print("-" * 40)


def inputXOR_list():
    print("-" * 40)
    print(f"{Fore.GREEN}VerboseXOR:{Fore.RESET} input XOR LIST")
    list1_input = input("Enter first list (comma-separated numbers): ")
    list2_input = input("Enter second list (comma-separated numbers): ")
    print("-" * 40)
    
    # Split and convert to integers
    list1 = [int(x.strip()) for x in list1_input.split(',')]
    list2 = [int(x.strip()) for x in list2_input.split(',')]
    
    # XOR each pair of elements
    print(f"List 1: {list1}")
    print(f"List 2: {list2}\n")
    
    results = []
    for i, (num1, num2) in enumerate(zip(list1, list2)):
        result = verbose_decimal_xor(num1, num2)
        results.append(result)
        print()
    
    print(f"XOR Results: {results}")
    print("-" * 40)

def XOR_ENCRYPT():
    print("-"*40)
    content = input("Input unencrypted message: ")
    key = input("Input 8-digit binary key (e.g. 01010101), or leave blank for random: ")

    # Determine key byte
    if key.strip() == "":
        key_byte = secrets.randbelow(256)
        key = format(key_byte, '08b')
        generated = True
    else:
        # validate key
        try:
            key_byte = int(key, 2)
            if key_byte < 0 or key_byte > 255:
                raise ValueError
            generated = False
        except Exception:
            print(f"{Fore.RED}Invalid key. Must be an 8-bit binary string like 01010101.{Style.RESET_ALL}")
            return

    print(f"{Style.BRIGHT}{Fore.BLUE}Using key:{Style.RESET_ALL} {Fore.YELLOW}{key}{Style.RESET_ALL}")
    pyperclip.copy(key)
    input(f"{Fore.CYAN}Key copied to clipboard. Paste it somewhere safe and press Enter to continue...{Style.RESET_ALL}")

    # Convert content to bytes
    content_bytes = content.encode('utf-8')

    # XOR each byte with key_byte
    encrypted_bytes = bytes([b ^ key_byte for b in content_bytes])

    # Represent ciphertext as base64 so it's printable
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode('ascii')

    print(f"\n{Style.BRIGHT}{Fore.GREEN}Encryption steps:{Style.RESET_ALL}")
    print(f"  Message bytes: {list(content_bytes)}")
    print(f"  Key byte: {key_byte} ({key})")
    print(f"  Encrypted bytes: {list(encrypted_bytes)}")
    print(f"{Fore.GREEN}\n  Ciphertext (base64): {Fore.LIGHTBLUE_EX}{encrypted_b64}{Style.RESET_ALL}\n")

    pyperclip.copy(encrypted_b64)
    input(f"{Fore.CYAN}Ciphertext copied to clipboard. Press Enter when done...{Style.RESET_ALL}")
    print("-"*40)
    return encrypted_b64

def XOR_DECRYPT():
    print("-"*40)
    encrypted_text = input("Input encrypted text (base64): ")
    key = input("Input 8-digit binary key: ")

    # Validate key
    try:
        key_byte = int(key, 2)
        if key_byte < 0 or key_byte > 255:
            raise ValueError
    except Exception:
        print(f"{Fore.RED}Invalid key. Must be an 8-bit binary string like 01010101.{Style.RESET_ALL}")
        return

    # Decode base64
    try:
        encrypted_bytes = base64.b64decode(encrypted_text)
    except Exception:
        print(f"{Fore.RED}Invalid ciphertext. Expected base64-encoded data.{Style.RESET_ALL}")
        return

    # XOR to recover plaintext bytes
    decrypted_bytes = bytes([b ^ key_byte for b in encrypted_bytes])

    try:
        deciphered_message = decrypted_bytes.decode('utf-8')
    except Exception:
        deciphered_message = str(decrypted_bytes)

    print(f"\n{Style.BRIGHT}{Fore.GREEN}Decryption steps:{Style.RESET_ALL}")
    print(f"  Ciphertext bytes: {list(encrypted_bytes)}")
    print(f"  Key byte: {key_byte} ({key})")
    print(f"  Decrypted bytes: {list(decrypted_bytes)}")
    print(f"{Fore.GREEN}\n  Deciphered message: {Fore.LIGHTBLUE_EX}{deciphered_message}{Style.RESET_ALL}\n")

    pyperclip.copy(deciphered_message)
    input(f"{Fore.CYAN}Plaintext copied to clipboard. Press Enter when done...{Style.RESET_ALL}")
    print("-"*40)
    return deciphered_message

def XOR_binary():
    """Perform verbose XOR directly on two binary strings (action: 'bin').

    Prompts the user for two binary strings, pads them to equal length,
    and prints a step-by-step XOR with colored output. Copies the
    resulting binary string to the clipboard and returns it.
    """
    print("-" * 20)
    print(f"{Fore.GREEN}VerboseXOR:{Fore.RESET} input XOR BINARY")
    b1 = input("Enter first binary string (e.g. 0101): ").strip().replace(' ', '')
    b2 = input("Enter second binary string (e.g. 0011): ").strip().replace(' ', '')
    print("-" * 20)

    # Validate
    if not (all(ch in '01' for ch in b1) and all(ch in '01' for ch in b2)):
        print(f"{Fore.RED}Invalid binary input. Only characters 0 and 1 are allowed.{Style.RESET_ALL}")
        return

    # Pad to same length (left-pad)
    length = max(len(b1), len(b2))
    bin1 = b1.zfill(length)
    bin2 = b2.zfill(length)

    print(f"  Binary A (padded): {bin1}")
    print(f"  Binary B (padded): {bin2}\n")

    result = []
    print("Step-by-step comparison (A ^ B):")
    for i in range(length):
        bit_a = int(bin1[i])
        bit_b = int(bin2[i])
        xor_result_bit = bit_a ^ bit_b
        print(f"  Bit {i+1}:{Fore.GREEN} {bit_a} ^ {bit_b} ={Fore.LIGHTGREEN_EX} {xor_result_bit}{Style.RESET_ALL}")
        result.append(str(xor_result_bit))

    final_bin = "".join(result)
    try:
        final_dec = int(final_bin, 2)
    except Exception:
        final_dec = 0

    print(f"\nFinal Result (Binary):{Fore.GREEN} {final_bin}{Style.RESET_ALL}")
    print(f"Final Result (Decimal):{Fore.CYAN} {final_dec}{Style.RESET_ALL}")

    pyperclip.copy(final_bin)
    input(f"{Fore.CYAN}Result copied to clipboard. Press Enter to continue...{Style.RESET_ALL}")
    print("-" * 20)
    return final_bin

link_url = 'https://github.com/AlkivaAdiarsa'

def startXORops():
    while True:
        answer = input(f"{Fore.LIGHTGREEN_EX} input action: XOR Binary, XOR integers, XOR list, encrypt/decrypt text, or help? actions:{Fore.LIGHTMAGENTA_EX} \n - bin \n - int\n - list\n - encrypt \n - decrypt \n - help{Style.RESET_ALL}\nenter action: ").lower()
        
        if answer == "int":
            InputXOR()
        elif answer == "list":
            inputXOR_list()
        elif answer == "help":
                help_page()
        elif answer == "encrypt":
            XOR_ENCRYPT()
        elif answer == "decrypt":
            XOR_DECRYPT()
        elif answer == "bin":
            XOR_binary()
        else:
            print(f"{Fore.RED}INVALID INPUT{Fore.RESET}")
        
        again = input(f"Run{Fore.RED} VerboseXOR{Fore.RESET} again? Y/N: ").lower()
        if again != "y":
            break


startXORops()