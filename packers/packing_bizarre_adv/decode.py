# Given values in hexadecimal
X1_1 = 0x988a215bec73afb4
X1_2 = 0xef48e5cb65f245cf
Y1_1 = 0xedba58208b12c3d2
Y1_2 = 0x9c1791b3569c1abd

X2_1 = 0xa0e9997a1f26e55d
X2_2 = 0xf997be04d7255ecb
Y2_1 = 0x8e9aa8252c50896d
Y2_2 = 0x84e18d69e05c70e5

# Function to convert a 64-bit integer to a byte array in little endian format
def int_to_little_endian_bytes(value):
    return value.to_bytes(8, byteorder='little')

# Convert the given hex values to byte arrays
X1_bytes = int_to_little_endian_bytes(X1_1) + int_to_little_endian_bytes(X1_2)
Y1_bytes = int_to_little_endian_bytes(Y1_1) + int_to_little_endian_bytes(Y1_2)
X2_bytes = int_to_little_endian_bytes(X2_1) + int_to_little_endian_bytes(X2_2)
Y2_bytes = int_to_little_endian_bytes(Y2_1) + int_to_little_endian_bytes(Y2_2)

# XOR the bytes to find the original flag bytes
flag_bytes = bytes([y1 ^ x1 for y1, x1 in zip(Y1_bytes, X1_bytes)]) + bytes([y2 ^ x2 for y2, x2 in zip(Y2_bytes, X2_bytes)])

# Convert the flag bytes to a string
flag = flag_bytes.decode('utf-8', errors='ignore')
flag, flag_bytes.hex()


""" # Let's start by decoding the given code snippets and understanding the logic.

# We have two sections of code, each handling a part of the "flag" string.
# In each section, we have two pairs of hexadecimal values (X1_1, X1_2 and Y1_1, Y1_2 for the first part,
# and X2_1, X2_2 and Y2_1, Y2_2 for the second part). We need to concatenate these values for each pair.

# We then need to reverse engineer the code to find the correct input for "flag".
# The code compares each character of the flag with XORed values of X and Y to determine if it's correct.

# Let's define the hexadecimal values given:

# For the first part
X1_1 = 0xa0e9997a1f26e55d
X1_2 = 0xf997be04d7255ecb
Y1_1 = 0x8e9aa8252c50896d
Y1_2 = 0x84e18d69e05c70e5

# For the second part
X2_1 = 0x988a215bec73afb4
X2_2 = 0xef48e5cb65f245cf
Y2_1 = 0xedba58208b12c3d2
Y2_2 = 0x9c1791b3569c1abd

# Concatenating the values for X1, X2, Y1, and Y2
X1 = (X1_1 << 64) | X1_2
X2 = (X2_1 << 64) | X2_2
Y1 = (Y1_1 << 64) | Y1_2
Y2 = (Y2_1 << 64) | Y2_2

# We'll use bytearray to store the flag as we construct it. It's initialized with 32 bytes (0x20).
flag = bytearray(32)

# Let's reverse engineer the flag using the XOR operations described in the code.
# For each byte in the flag, we'll find the correct character that satisfies the condition.
# We need to consider little endian format for the calculations.

# First part (bytes 16-31 of the flag)
for i in range(16):
    flag[i + 16] = (Y1 >> (8 * i)) & 0xFF ^ (X1 >> (8 * i)) & 0xFF

# Second part (bytes 0-15 of the flag)
for i in range(16):
    flag[i] = (Y2 >> (8 * i)) & 0xFF ^ (X2 >> (8 * i)) & 0xFF

# Convert the bytearray to a string to display the flag
print(flag.decode())
 """