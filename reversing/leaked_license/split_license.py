# Split the license key into 5 parts
# Hexadecimal license
license_hex = "726cfc2d26c6defedb06562199f5c7d0da4f4930"

# Convert to binary
license_bin = bin(int(license_hex, 16))[2:].zfill(160)  # Ensure 160 bits

# Split into 5 segments of 32 bits each
segments = [license_bin[i:i+32] for i in range(0, 160, 32)]

# Convert each segment back to hexadecimal
segments_hex = [hex(int(segment, 2))[2:].zfill(8) for segment in segments]

print(segments_hex)
# ['726cfc2d', '26c6defe', 'db065621', '99f5c7d0', 'da4f4930']
