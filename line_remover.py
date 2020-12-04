inp = open("output.json", "r")
arq = open("no_blank_lines.json", "w")
lines = []
for line in inp:
	if line == '' or line == '\n':
		continue
	else:
		lines.append(line)
for line in lines:
	arq.write(line)