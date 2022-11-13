import time
import random
import curses
from curses import wrapper


def start_screen(scrtxt):
	scrtxt.clear()
	scrtxt.addstr("This is the Speed Typing Test!")
	scrtxt.addstr("\nPress any key to begin!")
	scrtxt.refresh()
	scrtxt.getkey()

def display_text(scrtxt, target, current, wpm=0):
	scrtxt.addstr(target)
	scrtxt.addstr(1, 0, f"WPM: {wpm}")

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		scrtxt.addstr(0, i, char, color)

def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def wpm_test(scrtxt):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	scrtxt.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		scrtxt.clear()
		display_text(scrtxt, target_text, current_text, wpm)
		scrtxt.refresh()

		if "".join(current_text) == target_text:
			scrtxt.nodelay(False)
			break

		try:
			key = scrtxt.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(scrtxt):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(scrtxt)
	while True:
		wpm_test(scrtxt)
		scrtxt.addstr(2, 0, "You completed the text! Press any key to continue...")
		key = scrtxt.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)