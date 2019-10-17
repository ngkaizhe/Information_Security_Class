import re
import sys

# init tables
IP = [
58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17, 9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7,
]

IP1 = [
40, 8, 48, 16, 56, 24, 64, 32,
39, 7, 47, 15, 55, 23, 63, 31,
38, 6, 46, 14, 54, 22, 62, 30,
37, 5, 45, 13, 53, 21, 61, 29,
36, 4, 44, 12, 52, 20, 60, 28,
35, 3, 43, 11, 51, 19, 59, 27,
34, 2, 42, 10, 50, 18, 58, 26,
33, 1, 41, 9, 49, 17, 57, 25,
]

E = [
32, 1, 2, 3, 4, 5,
4, 5, 6, 7, 8, 9,
8, 9, 10, 11, 12, 13,
12, 13, 14, 15, 16, 17,
16, 17, 18, 19, 20, 21,
20, 21, 22, 23, 24, 25,
24, 25, 26, 27, 28, 29,
28, 29, 30, 31, 32, 1,
]

PC1 = [
57, 49, 41, 33, 25, 17, 9,
1, 58, 50, 42, 34, 26, 18,
10, 2, 59, 51, 43, 35, 27,
19, 11, 3, 60, 52, 44, 36,
63, 55, 47, 39, 31, 23, 15,
7, 62, 54, 46, 38, 30, 22,
14, 6, 61, 53, 45, 37, 29,
21, 13, 5, 28, 20, 12, 4,
]

PC2 = [
14, 17, 11, 24, 1, 5,
3, 28, 15, 6, 21, 10,
23, 19, 12, 4, 26, 8,
16, 7, 27, 20, 13, 2,
41, 52, 31, 37, 47, 55,
30, 40, 51, 45, 33, 48,
44, 49, 39, 56, 34, 53,
46, 42, 50, 36, 29, 32,
]

P = [
16, 7, 20, 21, 29, 12, 28, 17,
1, 15, 23, 26, 5, 18, 31, 10,
2, 8, 24, 14, 32, 27, 3, 9,
19, 13, 30, 6, 22, 11, 4, 25,
]

Ss = [
[
14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
15, 12, 8, 2, 4, 9, 1,7, 5, 11, 3, 14, 10, 0, 6, 13,
]
,
[
15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,
]
,
[
10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,
]
,
[
7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,
]
,
[
2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,
]
,
[
12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,
]
,
[
4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,
]
,
[
13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11,
]
,
]


def get_table(contents: list, name: str):
	rows = 0
	cols = 0
	pos = 0

	for line in contents:
		if ' ' + name + ' ' in line:
			pos = contents.index(line)
			line_list = re.split(' |:', line)
			line_list = [x for x in line_list if x]
			rows = int(line_list[1])
			cols = int(line_list[2])
			break

	rtn = []
	for r in range(pos + 1, pos + 1 + rows):
		temp1 = [int(x) for x in contents[r].split(' ') if x]
		rtn += temp1

	return rtn


def match_table(table: list, input_list: list):
	# initialize the rtn output
	rtn = [0 for x in range(len(table))]

	# start to do permutation
	for i in range(len(table)):
		rtn[i] = input_list[table[i] - 1]

	return rtn


def get_string_binary(hex_value: str):
	string_form = ''.join([bin(int(letter, 16))[2:].zfill(4) for letter in hex_value])
	return [char for char in string_form]


def list_XOR(list1: list, list2: list):
	return ['1' if list1[i] != list2[i] else '0' for i in range(len(list1))]


def list_left_shift(list1: list, n: int):
	return list1[n:] + list1[:n]


def f_func(k1: list, R1: list):
	interval = 6
	R_48_bits = match_table(E, R1)
	temp1 = list_XOR(R_48_bits, k1)
	result1 = []

	# split into 6 each loop
	i = 0
	s_i = 0
	while i < len(temp1):
		list_6_bits = temp1[i:i+interval]

		# s box
		S = Ss[s_i]
		r = int(''.join([list_6_bits[0]] + [list_6_bits[5]]), 2)
		c = int(''.join(list_6_bits[1:5]), 2)
		value_10_base = int(S[r * 16 + c])
		list_4_bits = [char for char in bin(value_10_base)[2:].zfill(4)]

		# concatenate
		result1 += list_4_bits

		# increase
		i += interval
		s_i += 1

	return match_table(P, result1)


if __name__ == "__main__":
	# read tables file content
	# file = open("tables", "r")
	# IP = []
	# E = []
	# PC1 = []
	# PC2 = []
	# P = []
	# Ss = []
	# IP1 = []

	# get table for all list
	# if file.mode == 'r':
	# 	contents = file.read()
	# 	contents = [x for x in contents.split('\n') if x]
	# 	IP = get_table(contents, "IP")
	# 	E = get_table(contents, "E")
	# 	PC1 = get_table(contents, "PC-1")
	# 	PC2 = get_table(contents, "PC-2")
	# 	P = get_table(contents, "P")
	# 	Ss = [get_table(contents, f'S{i}') for i in range(1, 9)]
	# 	# IP1 = get_table(contents, "IP-1")

	# get key
	key = sys.argv[1]
	# get plaintext
	plaintext = sys.argv[2]

	# get plaintext binary
	plaintext = get_string_binary(plaintext[2:])
	# get key binary
	key = get_string_binary(key[2:])

	# initialize
	# get key with 56 bits
	k = match_table(PC1, key)
	C = k[: int(len(k) / 2)]
	D = k[int(len(k) / 2):]

	# initial permutation for plaintext
	x = match_table(IP, plaintext)
	# get the left part and right part
	L = x[: int(len(x) / 2)]
	R = x[int(len(x) / 2):]

	# do 16 times for DES
	for i in range(0, 16):
		# transform
		# left shift the key
		if i+1 in [1, 2, 9, 16]:
			C = list_left_shift(C, 1)
			D = list_left_shift(D, 1)
		else:
			C = list_left_shift(C, 2)
			D = list_left_shift(D, 2)
		# match permutation PC-2
		k = match_table(PC2, C + D)
		
		# do the function for R part and key part
		result = f_func(k, R)

		# XOR the result with L part
		temp = list_XOR(result, L)
		# swap the position of L part and R part
		L = R
		R = temp

	# final permutation
	cipher = match_table(IP1, R + L)
	# change bits form to hex form
	cipher_per_4 = [hex(int(''.join(cipher[i:i+4]), 2))[2] for i in range(0, len(cipher), 4)]
	print('0x' + ''.join(cipher_per_4).upper())
