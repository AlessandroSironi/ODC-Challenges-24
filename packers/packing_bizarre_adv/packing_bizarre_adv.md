# Packing Bizarre Adventure

1) Break at decode() in gdb
2) Look for the end of the decode stage. Last instruction is at decode+284, when JNE is not taken, the decode is finished.
First address to break to is decode + 290, 0x5555555552db
Second address is decode + 432, 0x555555555369
Third address is decode + 438, 0x55555555536f
Fourth is 0x55555555540c
These are jumps that are useful to break to, as you can check the code and, in this order, are accessible, as the unpack routine has occurred.
3) memdump.

''' bash
dump memory memdump 0x00005555555551b9 0x0000555555555369 
dump memory memdump2 0x00005555555551b9 0x000055555555548e 
'''
4) Patch the whole decode function with patcher.py
5) Reverse engineer. Keep in mind that 16 bytes are needed, and Ghidra splits them in two variables that have to be concatenated. 

Seems like there are two steps, and the found element is used as the decryption key for a second part. 

''' c
X1_1 = 0x988a215bec73afb4;
    X1_2 = 0xef48e5cb65f245cf;
    local_38 = 0;
    Y1_1 = 0xedba58208b12c3d2;
    Y1_2 = 0x9c1791b3569c1abd;
    local_18 = 0;
    bVar2 = true;
    for (i = 0; i < 0x10; i = i + 1) {
      bVar2 = (bool)(bVar2 & ((int)*(char *)((long)&flag + (long)i) ^
                             (uint)*(byte *)((long)&X1_1 + (long)i)) ==
                             (uint)*(byte *)((long)&Y1_1 + (long)i));
    }
    if (!bVar2) break;


  X2_1 = 0xa0e9997a1f26e55d;
  X2_2 = 0xf997be04d7255ecb;
  local_38 = 0;
  Y2_1 = 0x8e9aa8252c50896d;
  Y2_2 = 0x84e18d69e05c70e5;
  local_18 = 0;
  bVar2 = true;
  for (i = 0; i < 0x10; i = i + 1) {
    bVar2 = (bool)(bVar2 & ((int)(char)flag[(long)i + 0x10] ^ (uint)*(byte *)((long)&X2_1 + (long)i)
                           ) == (uint)*(byte *)((long)&Y2_1 + (long)i));
  }
  if (bVar2) {
    puts(win);
  }
  else {
    puts(fail);
  }
'''

''' python
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
'''

FLAG: flag{y0ur_n3xt_s0lv3_1s...y7m3v}