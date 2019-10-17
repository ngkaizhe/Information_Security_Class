import re
import sys


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
	file = open("tables", "r")
	IP = []
	E = []
	PC1 = []
	PC2 = []
	P = []
	Ss = []
	IP1 = []

	# get table for all list
	if file.mode == 'r':
		contents = file.read()
		contents = [x for x in contents.split('\n') if x]
		IP = get_table(contents, "IP")
		E = get_table(contents, "E")
		PC1 = get_table(contents, "PC-1")
		PC2 = get_table(contents, "PC-2")
		P = get_table(contents, "P")
		Ss = [get_table(contents, f'S{i}') for i in range(1, 9)]
		IP1 = get_table(contents, "IP-1")

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
