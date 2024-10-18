#!/usr/bin/env python

from binascii import hexlify, unhexlify
import binascii
from mnemonic import Mnemonic
import random
import sys
import hashlib
import argparse

key_bin = ""
key_dex = ""
key_dexmod16 = ""
key_hex =""
key_hex_space =""

def is_valid_hex(key_hex):
    try:
        int(key_hex, 16)
        return len(key_hex) % 2 == 0
    except ValueError:
        return False

parser = argparse.ArgumentParser(description='Generate seeds from dice rolls.')
parser.add_argument('--len', type=str, help='Seeds length LEN = 12/18/24 default 12', default='12')
parser.add_argument('--dice', action='store_true', help='Use real dice rolls instead of random numbers')
parser.add_argument('--hex', type=str, help='Use HEX string to generate seeds', default='')
args = parser.parse_args()

seeds_peers =  {"12": 128, '18':192, '24':256}
hex_peers = {"32":12, '48':18, '64':24}
mnemo = Mnemonic("english")

if args.hex:
    key_hex = args.hex
    if not is_valid_hex(key_hex):
        print("Hex string should be 0123456789ABCDEF format.")
        sys.exit(0)
    if len(key_hex) not in {32, 48, 64}:
        print("Hex string should be 32, 48, 64 characters long.")
        sys.exit(0)
    key_length = str(hex_peers[str(len(key_hex))])
    key_bits_length = seeds_peers[key_length]
    
    p = 0

    while p < len(key_hex):
        n10=int(key_hex[p],16)
        key_bin += "{0:04b}".format(n10%16)
        key_dex += "{0:4d}".format(n10)
        c16 = "{0:X}".format(n10)
        key_hex_space += "{0:4X}".format(n10 % 16)
        p += 1
else:
    key_hex =""
    key_sen_space = ""
    key_dice = ""
    dices = []

    key_length = args.len
    if key_length not in seeds_peers.keys():
        print("Seeds length should be one of the following: [12, 18, 24], but it is not "+key_length)
        sys.exit(0)

    key_bits_length = seeds_peers[key_length]    
    code_length = int(key_bits_length / 4)

    if args.dice:
        print("\n Please input pair of dices step by step:\n")
    p = 1
    pair_no = 0
    while p<=code_length:
        pair_no += 1

        if args.dice:
            print ("\nTrying {0}/{1}... ".format(p,code_length))
            dice1 = input(" DICE1(1-6):")
            dice2 = input(" DICE2(1-6):")
            if len(dice1)!=1 or len(dice2)!=1:
                print("[",dice1,dice2,"] are not real dice numbers. Please input again.")
                continue 
            if dice1[0] >"6" or dice1[0] <"1" or dice2[0] >"6" or dice2[0] <"1":
                print("[",dice1,dice2,"] are not real dice numbers. Please input again.")
                continue
        else:
            dice1 = random.sample("123456",1)
            dice2 = random.sample("123456",1)

        s1 =int(dice1[0])-1
        s2 =int(dice2[0])-1
        n10=s1*6+s2

        if n10 < 32:
            key_dice += "  "+ dice1[0] + dice2[0]
            key_sen_space += f"  {s1}{s2}"
            key_bin += "{0:04b}".format(n10%16)
            key_dex += "{0:4d}".format(n10)
            key_dexmod16 += "{0:4d}".format(n10%16)

            n10_mod = n10 % 16
            c16 = "{0:X}".format(n10_mod)
            key_hex += c16
            key_hex_space += "{0:4X}".format(n10 % 16)
            dices.append(dice1[0])
            dices.append(dice2[0])
            print("DICE[\033[32m{0},{1}\033[0m] SEN[\033[32m{2},{3}\033[0m] DEC[\033[32m{4:2d}\033[0m] MOD[\033[32m{5:2d}\033[0m] HEX[\033[32m{6}\033[0m]".format(dice1[0],dice2[0],s1,s2,n10,n10_mod,c16))
            p += 1
        else:
            print("DICE[{0},{1}] SEN[{2},{3}] DEC[{4:2d}] above 31. Be abandoned.".format(dice1[0],dice2[0],s1,s2,n10))
        if args.dice:        
            print(dices)

    print("\nRolled dices:",pair_no*2,"(",code_length*2,")")

data = unhexlify(key_hex)
mnemonic = mnemo.to_mnemonic(data)

print("\nKEY_BITS:",str(key_bits_length))
print("\n ",key_hex)
print("\nSEEDS:",key_length)
print("\n  "+mnemonic+"\n")

if args.dice:
    print("DCS:",key_dice)
    print("SIX:",key_sen_space)

print("DEC:",key_dex)
if not args.hex:
    print("MOD:",key_dexmod16)
print("HEX:",key_hex_space)
print("BIN:",key_bin,"\n")

key_bin = bin(int(binascii.hexlify(data), 16))[2:].zfill(len(data) * 8)
digest_bin = bin(int(hashlib.sha256(data).hexdigest(), 16))[2:].zfill(256)[: len(data) * 8 // 32]
arr_mnemo = mnemonic.split(" ")
print("\033[32mNo 11 bits BIN Index Seed\033[0m")
for i in range(len(arr_mnemo)):
    if i == len(arr_mnemo)-1:
        idx_seed_bin = key_bin[i * 11 :] + digest_bin 
        idx_seed = key_bin[i * 11 :] + "\033[31m"+digest_bin + "\033[0m"
    else:
        idx_seed_bin = key_bin[i * 11 : (i + 1) * 11]
        idx_seed = idx_seed_bin
    idx_dec = int(idx_seed_bin, 2)
    print(f"{i+1:2} {idx_seed} {idx_dec:5} {arr_mnemo[i]:20}")
print("\nBits in \033[31mRED\033[0m "+"is SHA256 HEX digest")
print("\nSeeds format options: 12/18/24, here is \033[32m"+key_length+"\033[0m\n")

