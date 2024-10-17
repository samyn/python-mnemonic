#!/usr/bin/env python

from binascii import hexlify, unhexlify
import binascii
from mnemonic import Mnemonic
import random
import sys
import hashlib
from termcolor import colored 

seeds_peers =  {"12": 128, '18':192, '24':256}
length = "12"
if len(sys.argv) > 1:
    length = sys.argv[1]
    if length not in seeds_peers.keys():
        print("Seeds length should be one of the following: [12, 18, 24], but it is not "+length)
        sys.exit(0)
key_bits_length = seeds_peers[length]
code_length = int(key_bits_length / 4)
mnemo = Mnemonic("english")

key_hexstr =""
'''
print("\n Random HEX:")
for _ in range(code_length):
    c1 = random.sample("ABCDEF0123456789",1)
    #print(c1)
    key_hexstr += c1[0]
#key_hexstr = "912BF6D0C3FE1111E6BC79E76D45FBD4"
print(key_hexstr)
'''
print("\n PLEASE INPUT PAIR OF DICE STEP BY STEP:")
key_dice = ""
key_binary = ""
key_base6 = ""
key_4digit6 = ""
key_4digit10 = ""
key_4digit10mod = ""
key_hexstr =""
key_hexstr_space =""
dices = []
p = 1
pair_no = 0
while p<=code_length:
    pair_no += 1
    dice1 = random.sample("123456",1)
    dice2 = random.sample("123456",1)
    '''
    print ("\nTRYING {0}/{1}... ".format(p,code_length))
    dice1 = input(" DICE1(1-6):")
    dice2 = input(" DICE2(1-6):")
    '''
    if len(dice1)==0 or len(dice2)==0:
        print("PLEASE INPUT AGAIN.")
        continue 
    if dice1[0] >"6" or dice1[0] <"1" or dice2[0] >"6" or dice2[0] <"1":
        print("[",dice1,dice2,"] ARE NOT REAL DICE NUMBERS.")
        continue

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
        c16 = "{0:X}".format(n10 % 16)
        key_hexstr += c16
        key_hexstr_space += "{0:4X}".format(n10 % 16)
        dices.append(dice1[0])
        dices.append(dice2[0])
        #print("Dice pair[",dice1[0],dice2[0],"] base6[",s1,s2,"] base10[",n10,"] HEX[",c16,"]")
        print("DICE[{0},{1}] B06[{2},{3}] B10[{4:2d}] B16[{5}]".format(dice1[0],dice2[0],s1,s2,n10,c16))
        #print(dices)
        p += 1
    else:
        print("DICE[{0},{1}] B06[{2},{3}] B10[{4:2d}] IN 32-35, ABANDONED.".format(dice1[0],dice2[0],s1,s2,n10))
        #print(dices)
print("\nROLLED DICES:",pair_no*2,"(",code_length*2,")")




# key_hexstr = "912BF6D0C3FE1111E6BC79E76D45FBD4"
data = unhexlify(key_hexstr)
mnemonic = mnemo.to_mnemonic(data)
print("SEEDS[12*/18/24]:"+length)
print("KEY_BITS[128/192/256]:"+str(key_bits_length))
print("\n  "+mnemonic+"\n")


print("HEX: ",key_hexstr)
print("DCS: ",key_dice)
print("SIX: ",key_4digit6)
print("DEC: ",key_4digit10)
print("MOD: ",key_4digit10mod)
print("HEX: ",key_hexstr_space)
print("BIN: ",key_binary)
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



