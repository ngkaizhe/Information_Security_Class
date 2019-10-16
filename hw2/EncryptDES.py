import re

def get_table(contents: list, name: str):
	rows = 0
	cols = 0
	pos = 0

	for line in contents:
		if name in line:
			pos = contents.index(line)
			line_list = re.split(' |:', line)
			line_list = [x for x in line_list if x]
			rows = int(line_list[1])
			cols = int(line_list[2])
			break

	rtn = []
	for r in range(pos + 1, pos + 1 + rows):
		temp = [int(x) for x in contents[r].split(' ') if x]
		rtn += temp
	
	# print(rtn)
	# print(f"Pos is {pos}, Row is {rows}, Col is {cols}")
	return rtn



if __name__ == "__main__":
	# read tables file content
	file = open("tables", "r")
	IP = []
	E = []
	PC1 = []
	PC2 = []
	P = []
	Ss = []


	if file.mode == 'r':
		contents = file.read()
		contents = [x for x in contents.split('\n') if x]
		# IP = get_table(contents, "IP")
		# E = get_table(contents, "E")
		# PC1 = get_table(contents, "PC-1")
		# PC2 = get_table(contents, "PC-2")
		# P = get_table(contents, "P")
		Ss = [get_table(contents, f'S{i}') for i in range(1, 9)]


	print(Ss)


