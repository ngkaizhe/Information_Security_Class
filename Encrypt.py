import sys
import re

debug_mode = False

def debug_print(text: str):
	if debug_mode:
		print(text)
	else:
		pass

def caesar(key: str, plaintext: str):
	debug_print(f'caesar called! Plaintext is {plaintext}')
	key = int(key)

	# error to check: key must in int format
	Ciphertext = ''
	plaintext = plaintext.lower()

	for letter in plaintext:
		# only for alphabetic letter
		# shift
		small = chr(((ord(letter) - ord('a') + key) % 26) + ord('a'))
		Ciphertext += small

	return Ciphertext.upper()


def playfair(key: str, plaintext: str):
	debug_print(f'playfair called! Plaintext is {plaintext}')

	plaintext = plaintext.upper()
	key = key.upper()
	key += 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

	# create matrix
	temp = []
	for i in key:
		if(i not in temp):
			temp.append(i)

	Ciphertext = ''

	for tpl in [tuple(plaintext[i:i+2]) for i in range(0, len(plaintext), 2)]:
		letter1, letter2 = tpl
		r1, c1 = int(temp.index(letter1) / 5), temp.index(letter1) % 5
		r2, c2 = int(temp.index(letter2) / 5), temp.index(letter2) % 5

		# check is same row and col
		if r1 == r2 and c1 == c2:
			Ciphertext += letter1 + 'X'

		# check is same row
		elif r1 == r2:
			i1 = r1 * 5 + (c1 + 1) % 5
			i2 = r2 * 5 + (c2 + 1) % 5
			Ciphertext += temp[i1] + temp[i2]

		# check is same col
		elif c1 == c2:
			i1 = ((r1 + 1) % 5) * 5 + c1
			i2 = ((r2 + 1) % 5) * 5 + c2
			Ciphertext += temp[i1] + temp[i2]

		# else
		else:
			i1 = r1 * 5 + c2
			i2 = r2 * 5 + c1
			Ciphertext += temp[i1] + temp[i2]

	return Ciphertext



def vernam(key: str, plaintext: str):
	debug_print(f'vernam called! Plaintext is {plaintext}')

	plaintext = plaintext.upper()
	key = key.upper()
	key += plaintext

	Ciphertext = ''
	ip = 0

	while ip < len(plaintext):
		ik = ip

		seqPlain = ord(plaintext[ip]) - ord('A')
		seqKey = ord(key[ik]) - ord('A')
		Ciphertext += chr((seqPlain ^ seqKey) + ord('A'))

		ip += 1

	return Ciphertext



def row(key: int, plaintext: str):
	debug_print(f'row called! Plaintext is {plaintext}')

	plaintext = plaintext.upper()
	len_key = len(key)
	total_row = int(len(plaintext) / len_key)

	Ciphertext = ''

	for n in range(1, len_key + 1):
		col = key.index(str(n))
		Ciphertext += ''.join([plaintext[r * len_key + col] for r in range(total_row)])

	return Ciphertext



def rail_fence(key: str, plaintext: str):
	debug_print(f'rail_fence called! Plaintext is {plaintext}')

	plaintext = plaintext.upper()
	total_row = int(key)

	rail_fence = [[] for i in range(total_row)]

	Ciphertext = ''
	i = 0
	while i < len(plaintext):
		# row = 3, plaintext = WEAREDISCOVEREDFLEEATONCE
		# W . . . E . . . C . . . R . . . L . . . T . . . E 					W . E . C . R . L . T . E
		# . E . R . D . S . O . E . E . F . E . A . O . C .			==>			E R D S O E E F E A O C .
		# . . A . . . I . . . V . . . D . . . E . . . N . .						A . I . V . D . E . N . .
		# cipher text = WECRLTEERDSOEEFEAOCAIVDEN

		# row = 4, plaintext = WEAREDISCOVEREDFLEEATONCE
		# W . . . . . I . . . . . R . . . . . E . . . . . E 					 W . I . R . E . E
		# . E . . . D . S . . . E . E . . . E . A . . . C .			==>			 E D S E E E A C .
		# . . A . E . . . C . V . . . D . L . . . T . N . .						 A E C V D L T N .
		# . . . R . . . . . O . . . . . F . . . . . O . . .						 R . O . F . O . .
		# cipher text = WIREEEDSEEEACAECVDLTNROFO

		# top to bottom
		r = 0
		while i < len(plaintext) and r < total_row:
			rail_fence[r].append(plaintext[i])

			r += 1
			i += 1

		# bottom to top
		r = total_row - 1
		r -= 1
		while i < len(plaintext) and r > 0:
			rail_fence[r].append(plaintext[i])

			r -= 1
			i += 1


	debug_print(rail_fence)

	for i in rail_fence:
		Ciphertext += ''.join(i)

	return Ciphertext



CipherMap = {
	'caesar': caesar,
	'playfair': playfair,
	'vernam': vernam,
	'row': row,
	'rail_fence': rail_fence, 
}


if __name__ == "__main__":

	# input error checking
	if(len(sys.argv) is not 4):
		print(f'The number of arguments is not 4, your input number arguments is: {len(sys.argv)}')
	else:
		# get cipher
		cipher = sys.argv[1]
		# get key
		key = sys.argv[2]
		# get plaintext
		plaintext = sys.argv[3]

		# choose method
		Ciphertext = CipherMap[cipher](key, plaintext);
		print(Ciphertext)