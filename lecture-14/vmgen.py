import argparse
import random

from math import ceil


RAND_PAGE_BITS = [ 0x25, 0x65, 0x67, 0x865, 0x867]



def auto_int(x):
    return int(x, 0)


def get_bits(addr, start_bit, end_bit):
    addr >>= start_bit
    mask_bits = end_bit - start_bit
    mask = (1 << mask_bits) - 1
    return addr & mask

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="vmgen",
        description="map an address into generated page tables.",
    )
    parser.add_argument("address", type=auto_int)
    parser.add_argument("--page-size", default=4096, type=auto_int,
                        choices=[0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000, 0x10000],
                        help="the size of the page")
    parser.add_argument("--levels", choices = [5, 4, 3, 2], default=4, type=int,
                        help="number of page table levels")
    parser.add_argument("--address-bits", choices = [64, 32], default=64, type=int,
                       help="number of address bits")
    args = parser.parse_args()
    page_size = args.page_size
    address_bits = args.address_bits
    levels = args.levels
    address_bits = args.address_bits
    address = args.address
    entries_page = int(page_size / (address_bits/8))
    entry_bits = entries_page.bit_length() - 1
    offset_bits = page_size.bit_length() - 1
    offset_mask = (1 << offset_bits) - 1

    level_indexes = []
    start_bit = offset_bits # we start the page indexes where the offset ends
    for _ in range(levels):
        level_indexes.append(get_bits(address, start_bit, start_bit+entry_bits))
        start_bit += entry_bits

    offset = get_bits(address, 0, offset_bits)

    print(f"processing 0x{address:X} addr={address_bits}-bits levels={levels} page-size={page_size}")
    print(f"entries/page={entries_page} index-bits={entry_bits} offset-bits={offset_bits}")

    print("-----------")

    print(f"{address:b}: ", end="")
    for level_index in reversed(level_indexes):
        print(f" {level_index:0{entry_bits}b}", end="")
    
    print(f" {offset:0{offset_bits}b}")

    print(f"{address:X}: ", end="")
    for level_index in reversed(level_indexes):
        print(f" {level_index:0{ceil(entry_bits/4)}X}", end="")
    
    print(f" {offset:0{ceil(offset_bits/4)}X}")

    print("-----------")

    pagenum = random.randrange(100, 512*1024)
    cr3 = (pagenum << offset_bits) + 1
    print(f"CR3 = {cr3:X}")
    page_addr = cr3 & ~offset_mask

    for level in range(levels,0,-1):
        print("-----------")
        print(f"Physical address of page table {level}: 0x{page_addr:X}")
        print()
        print("Entry Address | Entry Index | Page table Entry")
        entries = [random.randrange(0, entries_page) for _ in range(4)]
        entries.append(level_indexes[level-1])
        for entry in sorted(entries):
            next_page_address = random.randrange(100, 512*1024) << offset_bits 
            if entry == level_indexes[level-1]:
                new_page_addr = next_page_address
            next_page_address |= random.choice(RAND_PAGE_BITS)
            if address_bits == 64 and random.randrange(0,4) == 1:
                next_page_address |= 1 << 63
            
            print(f"{page_addr+entry*(int(address_bits/8)):14X}|{entry:13X}|{next_page_address:X}")
        page_addr = new_page_addr

    print("-----------")
    print(f"Physical address for {address:X} is {page_addr+offset:X}")
