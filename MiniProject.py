# 1. Define Block and Key Sizes
BLOCK_SIZE_BITS = 8  # Each block is 8 bits (1 byte)
KEY_SIZE_BITS = 8    # The key is also 8 bits

# 2. Define Substitution Box (S-box)
# This is a predefined 4x4 S-box, which introduces non-linearity (confusion) in the encryption process.
SUBSTITUTION_BOX = [0xE, 0x4, 0xD, 0x1,
                    0x2, 0xF, 0xB, 0x8,
                    0x3, 0xA, 0x6, 0xC,
                    0x5, 0x9, 0x0, 0x7]

# Function to substitute 4-bit values using the S-box
def substitute_nibble(nibble):
    """Substitute 4-bit value using the substitution box"""
    return SUBSTITUTION_BOX[nibble]

# 3. Define Permutation Function
# This is the permutation table that rearranges the bits to provide diffusion.
PERMUTATION_MAP = [3, 0, 2, 4, 6, 1, 7, 5]

# Function to permute an 8-bit block according to the permutation table
def permute_block(input_block):
    """Permute 8-bit block using the permutation map"""
    # Convert the block to an 8-bit binary string
    binary_string = f'{input_block:08b}'  
    # Permute the bits based on the map and join them into a new string
    permuted_bits = ''.join([binary_string[PERMUTATION_MAP[i]] for i in range(BLOCK_SIZE_BITS)])
    # Convert the permuted string back into an integer
    return int(permuted_bits, 2)

# 4. Feistel Function
# This function takes the right half of the block and XORs it with the key.
def feistel_op(right_part, secret_key):
    """Feistel operation: XOR right half of the block with the key"""
    return right_part ^ secret_key

# 5. Combine Components for Single-Round Encryption
# This function performs a single round of block encryption using S-box, permutation, and Feistel function.
def encrypt_byte(plain_byte, secret_key):
    """Encrypt a single 8-bit byte"""
    # Split the byte into left and right halves (4 bits each)
    left_part = (plain_byte >> 4) & 0xF  # Top 4 bits
    right_part = plain_byte & 0xF        # Bottom 4 bits
   
    # Substitution using the S-box on the right half
    substituted_right = substitute_nibble(right_part)
   
    # Feistel operation: XOR left half with the substituted right half
    feistel_output = feistel_op(left_part, substituted_right)
   
    # Combine the left and right halves
    combined_result = (feistel_output << 4) | substituted_right
   
    # Permute the combined byte
    permuted_byte = permute_block(combined_result)
   
    return permuted_byte

# ECB Mode Implementation
# Encrypts multiple bytes independently of each other.
def encrypt_ecb(plain_bytes, secret_key):
    """Encrypt multiple bytes in ECB mode"""
    return [encrypt_byte(byte, secret_key) for byte in plain_bytes]

# Decrypts multiple bytes independently in ECB mode (symmetric to encryption).
def decrypt_ecb(cipher_bytes, secret_key):
    """Decrypt multiple bytes in ECB mode"""
    return [encrypt_byte(byte, secret_key) for byte in cipher_bytes]

# CBC Mode Implementation
# XORs the current plaintext byte with the previous ciphertext byte for added security.
def xor_bytes(byte1, byte2):
    """XOR two 8-bit bytes"""
    return byte1 ^ byte2

# Encrypts bytes using CBC mode, where each byte is XORed with the previous ciphertext byte.
def encrypt_cbc(plain_bytes, secret_key, iv):
    """Encrypt multiple bytes in CBC mode"""
    cipher_bytes = []
    previous_byte = iv  # Start with the initialization vector (IV)
    for byte in plain_bytes:
        # XOR the current byte with the previous ciphertext byte (or IV for the first byte)
        byte_to_encrypt = xor_bytes(byte, previous_byte)
        # Encrypt the XORed byte
        encrypted_byte = encrypt_byte(byte_to_encrypt, secret_key)
        # Append the encrypted byte to the ciphertext list
        cipher_bytes.append(encrypted_byte)
        # Update the previous byte to the current ciphertext
        previous_byte = encrypted_byte
    return cipher_bytes

# Decrypts bytes using CBC mode, reversing the process of encryption by XORing with the previous ciphertext byte.
def decrypt_cbc(cipher_bytes, secret_key, iv):
    """Decrypt multiple bytes in CBC mode"""
    plain_bytes = []
    previous_byte = iv  # Start with the initialization vector (IV)
    for byte in cipher_bytes:
        # Decrypt the current ciphertext byte
        decrypted_byte = encrypt_byte(byte, secret_key)
        # XOR the decrypted byte with the previous ciphertext byte (or IV for the first byte)
        plain_byte = xor_bytes(decrypted_byte, previous_byte)
        # Append the decrypted byte to the plaintext list
        plain_bytes.append(plain_byte)
        # Update the previous byte to the current ciphertext
        previous_byte = byte
    return plain_bytes

# Example usage for ECB and CBC modes
def main():
    # Test data
    test_plain_bytes = [0b11001101, 0b10011001]  # Two 8-bit bytes (205 and 153 in decimal)
    test_key = 0b10101010                         # 8-bit key
    initialization_vector = 0b10101010            # Initialization vector (IV)

    # ECB Mode Example
    print("ECB Mode = ")
    # Encrypt test bytes using ECB mode
    cipher_bytes_ecb = encrypt_ecb(test_plain_bytes, test_key)
    print(f"ECB Ciphertext bytes: {[bin(c) for c in cipher_bytes_ecb]}")

    # Decrypt ciphertext bytes back to plaintext using ECB mode
    decrypted_bytes_ecb = decrypt_ecb(cipher_bytes_ecb, test_key)
    print(f"ECB Decrypted bytes: {[bin(d) for d in decrypted_bytes_ecb]}")

    # CBC Mode Example
    print("\nCBC Mode = ")
    # Encrypt test bytes using CBC mode
    cipher_bytes_cbc = encrypt_cbc(test_plain_bytes, test_key, initialization_vector)
    print(f"CBC Ciphertext bytes: {[bin(c) for c in cipher_bytes_cbc]}")

    # Decrypt ciphertext bytes back to plaintext using CBC mode
    decrypted_bytes_cbc = decrypt_cbc(cipher_bytes_cbc, test_key, initialization_vector)
    print(f"CBC Decrypted bytes: {[bin(d) for d in decrypted_bytes_cbc]}")

if __name__ == "__main__":
    main()