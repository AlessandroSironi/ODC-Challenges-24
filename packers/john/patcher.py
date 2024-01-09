# this is how a patcher is implemented

BINARY_BASE = 0x08048000

def patch_binary(binary, path_file, address):
    with open(path_file, "rb") as f:
        patch = f.read()
        offset = address-BINARY_BASE
    patch_len = len(patch)
    binary = binary[:offset] + patch + binary[offset+patch_len:]
    return binary

with open("./john_clear", "rb") as f:
    binary = f.read()

binary = patch_binary(binary, "./memdump/check4", 0x08049385)

with open("./john_clear", "wb") as f:
    f.write(binary)