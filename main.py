import sys
import getch

def process(script):
	replacements = {
		"public": "[",
		"private": "]",
		"class": "<",
		"interface": ">",
		"static": "+",
		"final": "-",
		"println": ".",
		"scanner": ","
	}

	for literal, replacement in replacements.items():
		script = script.replace(literal, replacement)

	return "".join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], list(script)))

def verify(script):
	for token in ["public", "private", "class", "interface", "static", "final", "println", "scanner"]:
		if token in script:
			return True
	return False


def eval(script):
	script = process(script)
	chrmap = build_chrmap(script)

	mem, byte, addr = [0], 0, 0

	while byte < len(script):
		cmd = script[byte]

		if cmd == ">":
			addr += 1
			if addr == len(mem): mem.append(0)

		if cmd == "<": addr = 0 if addr <= 0 else addr - 1
		if cmd == "+": mem[addr] = mem[addr] + 1 if mem[addr] < 255 else 0
		if cmd == "-": mem[addr] = mem[addr] - 1 if mem[addr] > 0 else 255
		if cmd == "[" and mem[addr] == 0: byte = chrmap[byte]
		if cmd == "]" and mem[addr] != 0: byte = chrmap[byte]
		if cmd == ".": sys.stdout.write(chr(mem[addr]))
		if cmd == ",": mem[addr] = ord(getch.getch())
			
		byte += 1

def build_chrmap(script):
	tmp_struct, chrmap = [], {}

	for pos, cmd in enumerate(script):
		if cmd == "[": tmp_struct.append(pos)
		if cmd == "]":
			start = tmp_struct.pop()
			chrmap[start] = pos
			chrmap[pos] = start
	return chrmap

def main():
	if len(sys.argv) != 2: print("Usage:", sys.argv[0], "<file path>"); exit()
	with open(sys.argv[1], "r") as f: 
		script = f.read()
		if not verify(script): print(f"'{sys.argv[1]}' does not appear to be a valid Brainfu4J file!")
		eval(script)

if __name__ == "__main__": main()