# this is how a patcher is implemented

BINARY_BASE = 0x00100000

def patch_binary(binary, path_file, address):
    with open(path_file, "rb") as f:
        patch = f.read()
        offset = address-BINARY_BASE
        print("Offset is: {}".format(offset))
    patch_len = len(patch)
    if len(patch) > len(binary[offset:]):
        print("Patch is too big")
        return binary
    print("Patching {} bytes at address {}".format(patch_len, hex(address)))
    binary = binary[:offset] + patch + binary[offset+patch_len:]
    return binary

with open("./chall_patch1", "rb") as f:
    binary = f.read()

binary = patch_binary(binary, "./memdump0", 0x001011b9)

with open("./chall_patch1", "wb") as f:
    f.write(binary)