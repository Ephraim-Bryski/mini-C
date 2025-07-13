def print_memory_range(top_bytes, name):
    n_bits = 16
    n_extra_bits = n_bits - len(top_bytes)
    binary_string_low = f"0b{top_bytes}{'0'*n_extra_bits}"
    binary_string_high = f"0b{top_bytes}{'1'*n_extra_bits}"
    hex_low = hex(int(binary_string_low, 2))
    hex_high = hex(int(binary_string_high, 2))
    print(f"{name}: {hex_low} to {hex_high}")

print_memory_range("00","RAM")
print_memory_range("011","VIA")
print_memory_range("1","ROM")