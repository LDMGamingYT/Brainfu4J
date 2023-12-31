import sys

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def process(script:str):
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

def verify(script:str):
	for token in ["public", "private", "class", "interface", "static", "final", "println", "scanner"]:
		if token in script:
			return True
	return False


def eval(script:str):
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

def build_chrmap(script:str):
	tmp_struct, chrmap = [], {}

	for pos, cmd in enumerate(script):
		if cmd == "[": tmp_struct.append(pos)
		if cmd == "]":
			start = tmp_struct.pop()
			chrmap[start] = pos
			chrmap[pos] = start
	return chrmap

def main():
	if len(sys.argv) != 2: print("Usage:", sys.argv[0], "<file path>"); exit(1)
	with open(sys.argv[1], "r") as f: 
		script = f.read()
		if not verify(script): print(f"'{sys.argv[1]}' does not appear to be a valid Brainfu4J file!"); sys.exit(2)
		eval(script)

if __name__ == "__main__": main()