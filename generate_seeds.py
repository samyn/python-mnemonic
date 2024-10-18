#!/usr/bin/env python

from binascii import hexlify, unhexlify
import binascii
from mnemonic import Mnemonic
import random
import sys
import hashlib

from termcolor import colored 
import argparse

key_binary = ""
key_4digit10 = ""
key_4digit10mod = ""
key_hexstr =""
key_hexstr_space =""

def is_valid_hex(key_hexstr):
    try:
        int(key_hexstr, 16)
        return len(key_hexstr) % 2 == 0
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
    key_hexstr = args.hex
    if not is_valid_hex(key_hexstr):
        print("Hex string should be 0123456789ABCDEF format.")
        sys.exit(0)
    if len(key_hexstr) not in {32, 48, 64}:
        print("Hex string should be 32, 48, 64 characters long.")
        sys.exit(0)
    length = str(hex_peers[str(len(key_hexstr))])
    key_bits_length = seeds_peers[length]
    
    p = 0

    while p < len(key_hexstr):
        n10=int(key_hexstr[p],16)
        key_binary += "{0:04b}".format(n10%16)
        key_4digit10 += "{0:4d}".format(n10)
        c16 = "{0:X}".format(n10)
        key_hexstr_space += "{0:4X}".format(n10 % 16)
        p += 1
else:
    key_hexstr =""
    key_base6 = ""
    key_4digit6 = ""
    key_dice = ""
    dices = []

    length = args.len
    if length not in seeds_peers.keys():
        print("Seeds length should be one of the following: [12, 18, 24], but it is not "+length)
        sys.exit(0)

    key_bits_length = seeds_peers[length]    
    code_length = int(key_bits_length / 4)

    if args.dice:
        print("\n PLEASE INPUT PAIR OF DICE STEP BY STEP:\n")
    p = 1
    pair_no = 0
    while p<=code_length:
        pair_no += 1

        if args.dice:
            print ("\nTRYING {0}/{1}... ".format(p,code_length))
            dice1 = input(" DICE1(1-6):")
            dice2 = input(" DICE2(1-6):")
            if len(dice1)==0 or len(dice2)==0:
                print("PLEASE INPUT AGAIN.")
                continue 
            if dice1[0] >"6" or dice1[0] <"1" or dice2[0] >"6" or dice2[0] <"1":
                print("[",dice1,dice2,"] ARE NOT REAL DICE NUMBERS.")
                continue
        else:
            dice1 = random.sample("123456",1)
            dice2 = random.sample("123456",1)

        s1 =int(dice1[0])-1
        s2 =int(dice2[0])-1
        n10=s1*6+s2

        if n10 < 32:
            key_dice += "  "+ dice1[0] + dice2[0]
            key_4digit6 += f"  {s1}{s2}"
            key_binary += "{0:04b}".format(n10%16)
            key_4digit10 += "{0:4d}".format(n10)
            key_4digit10mod += "{0:4d}".format(n10%16)
            key_base6 += chr(ord("0")+s1)
            key_base6 += chr(ord("0")+s2)

            n10mod = n10 % 16
            c16 = "{0:X}".format(n10mod)
            key_hexstr += c16
            key_hexstr_space += "{0:4X}".format(n10 % 16)
            dices.append(dice1[0])
            dices.append(dice2[0])
            print("DICE[{0},{1}] B06[{2},{3}] B10[{4:2d}] MOD[{5:2d}] B16[{6}]".format(dice1[0],dice2[0],s1,s2,n10,n10mod,c16))
            p += 1
        else:
            print(colored("DICE[{0},{1}] B06[{2},{3}] B10[{4:2d}] IN 32-35, ABANDONED.".format(dice1[0],dice2[0],s1,s2,n10),'light_grey'))
        if args.dice:        
            print(dices)

    print(colored("\nROLLED DICES:",'light_grey'),pair_no*2,"(",code_length*2,")")

data = unhexlify(key_hexstr)
mnemonic = mnemo.to_mnemonic(data)

print(colored("\nKEY_BITS:",'light_grey'),str(key_bits_length))
print("\n ",key_hexstr)

print(colored("\nSEEDS:",'light_grey'),length)
print("\n  "+mnemonic+"\n")

if args.dice:
    print(colored("DCS:",'light_grey'),key_dice)
    print(colored("SIX:",'light_grey'),key_4digit6)

print(colored("DEC:",'light_grey'),key_4digit10)
if not args.hex:
    print(colored("MOD:",'light_grey'),key_4digit10mod)
print(colored("HEX:",'light_grey'),key_hexstr_space)
print(colored("BIN:",'light_grey'),key_binary,"\n")
h = hashlib.sha256(data).hexdigest()
hb = bin(int(h, 16))[2:].zfill(256)[: len(data) * 8 // 32]
b = bin(int(binascii.hexlify(data), 16))[2:].zfill(len(data) * 8)
#print(h,  b, hb)
arr_mnemo = mnemonic.split(" ")
for i in range(len(arr_mnemo)):
    colorb = ""
    if i == len(arr_mnemo)-1:
        bidx = b[i * 11 :] + hb
        colorb = colored(b[i * 11 :], 'white') + colored(hb, 'red')
    else:
        bidx = b[i * 11 : (i + 1) * 11]
        colorb = colored(bidx, 'white')
    idx = int(bidx, 2)
    print(f"{i:2} {colorb} {idx:4} {arr_mnemo[i]:20}")
print(colored("\nBits in ",'light_grey')+colored("RED ", 'red')+colored("is SHA256 hexdigest",'light_grey'))
print(colored("\nSEEDS FORMAT OPTIONS:12/18/24, HERE IS ",'light_grey')+colored(length,'green')+"\n")

