import time
import random
import math


def typewriter(text, delay=0.1):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)


def rainbow(text):
    colors = ["red", "yellow", "green", "blue", "magenta", "cyan"]
    for char in text:
        color = random.choice(colors)
        print(f"\033[1;{colors.index(color) + 31}m{char}", end="")
    print("\033[0m")


def blink(text, repeat=5, delay=0.5):
    for _ in range(repeat):
        print(text, end="\r")
        time.sleep(delay)
        print(" " * len(text), end="\r")
        time.sleep(delay)


def wavy(text, amplitude=1, frequency=1):
    for i in range(len(text)):
        angle = i / frequency
        offset = int(amplitude * math.sin(angle))
        print(" " * offset + text[i], end="")
    print()


def vaporwave(text):
    vaporwave_chars = {
        "a": "ａ",
        "b": "ｂ",
        "c": "ｃ",
        "d": "ｄ",
        "e": "ｅ",
        "f": "ｆ",
        "g": "ｇ",
        "h": "ｈ",
        "i": "ｉ",
        "j": "ｊ",
        "k": "ｋ",
        "l": "ｌ",
        "m": "ｍ",
        "n": "ｎ",
        "o": "ｏ",
        "p": "ｐ",
        "q": "ｑ",
        "r": "ｒ",
        "s": "ｓ",
        "t": "ｔ",
        "u": "ｕ",
        "v": "ｖ",
        "w": "ｗ",
        "x": "ｘ",
        "y": "ｙ",
        "z": "ｚ",
        "A": "Ａ",
        "B": "Ｂ",
        "C": "Ｃ",
        "D": "Ｄ",
        "E": "Ｅ",
        "F": "Ｆ",
        "G": "Ｇ",
        "H": "Ｈ",
        "I": "Ｉ",
        "J": "Ｊ",
        "K": "Ｋ",
        "L": "Ｌ",
        "M": "Ｍ",
        "N": "Ｎ",
        "O": "Ｏ",
        "P": "Ｐ",
        "Q": "Ｑ",
        "R": "Ｒ",
        "S": "Ｓ",
        "T": "Ｔ",
        "U": "Ｕ",
        "V": "Ｖ",
        "W": "Ｗ",
        "X": "Ｘ",
        "Y": "Ｙ",
        "Z": "Ｚ",
        " ": " ",
    }

    for char in text:
        vaporwave_char = vaporwave_chars.get(char, char)
        print(vaporwave_char, end="")
    print()


def cc_text(text, delay=0.1):
    colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]
    for char in text:
        color = random.choice(colors)
        print(color + char, end="", flush=True)
        time.sleep(delay)
    print("\033[0m")


class Colors:
    # Text colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;207m"
    LIME = "\033[38;5;154m"
    TEAL = "\033[38;5;51m"
    LAVENDER = "\033[38;5;183m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_GRAY = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"
    BG_ORANGE = "\033[48;5;208m"
    BG_PINK = "\033[48;5;207m"
    BG_LIME = "\033[48;5;154m"
    BG_TEAL = "\033[48;5;51m"
    BG_LAVENDER = "\033[48;5;183m"

    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def color_func(color_code):
    return lambda text: f"{color_code}{text}{Colors.RESET}"


black = color_func(Colors.BLACK)
red = color_func(Colors.RED)
green = color_func(Colors.GREEN)
yellow = color_func(Colors.YELLOW)
blue = color_func(Colors.BLUE)
magenta = color_func(Colors.MAGENTA)
cyan = color_func(Colors.CYAN)
white = color_func(Colors.WHITE)
gray = color_func(Colors.GRAY)
bright_red = color_func(Colors.BRIGHT_RED)
bright_green = color_func(Colors.BRIGHT_GREEN)
bright_yellow = color_func(Colors.BRIGHT_YELLOW)
bright_blue = color_func(Colors.BRIGHT_BLUE)
bright_magenta = color_func(Colors.BRIGHT_MAGENTA)
bright_cyan = color_func(Colors.BRIGHT_CYAN)
bright_white = color_func(Colors.BRIGHT_WHITE)
orange = color_func(Colors.ORANGE)
pink = color_func(Colors.PINK)
lime = color_func(Colors.LIME)
teal = color_func(Colors.TEAL)
lavender = color_func(Colors.LAVENDER)

bg_black = color_func(Colors.BG_BLACK)
bg_red = color_func(Colors.BG_RED)
bg_green = color_func(Colors.BG_GREEN)
bg_yellow = color_func(Colors.BG_YELLOW)
bg_blue = color_func(Colors.BG_BLUE)
bg_magenta = color_func(Colors.BG_MAGENTA)
bg_cyan = color_func(Colors.BG_CYAN)
bg_white = color_func(Colors.BG_WHITE)
bg_gray = color_func(Colors.BG_GRAY)
bg_bright_red = color_func(Colors.BG_BRIGHT_RED)
bg_bright_green = color_func(Colors.BG_BRIGHT_GREEN)
bg_bright_yellow = color_func(Colors.BG_BRIGHT_YELLOW)
bg_bright_blue = color_func(Colors.BG_BRIGHT_BLUE)
bg_bright_magenta = color_func(Colors.BG_BRIGHT_MAGENTA)
bg_bright_cyan = color_func(Colors.BG_BRIGHT_CYAN)
bg_bright_white = color_func(Colors.BG_BRIGHT_WHITE)
bg_orange = color_func(Colors.BG_ORANGE)
bg_pink = color_func(Colors.BG_PINK)
bg_lime = color_func(Colors.BG_LIME)
bg_teal = color_func(Colors.BG_TEAL)
bg_lavender = color_func(Colors.BG_LAVENDER)

bold = color_func(Colors.BOLD)
underline = color_func(Colors.UNDERLINE)


def p_ac():
    print("Available Colors:")
    for color_name in Colors.__dict__:
        if not color_name.startswith("__") and not color_name.endswith("RESET"):
            print(color_name.lower())


def help():
    print(
        bold(blue(underline("Color Pack Library By LillisLove- Available Functions:")))
    )
    print()
    print(blue("Text Color Functions:"))
    print(blue("red(text) - Prints the text in red color."))
    print(blue("Usage example:") + bold("print(red('This is red text'))"))
    print()
    print(blue("Background Color Functions:"))
    print(blue("bg_blue(text) - Prints the text with a blue background."))
    print(blue("Usage example: print(bg_blue('This has a blue background'))"))
    print()
    print(bold(blue(underline("Utility Functions:"))))
    print()
    print("p_ac() - Print the available color names.")
    print("help() - Print this help message.")
    print('Rainbow text : rainbow("String")')
    print('blink("string", repeat=5,delay=0.5)')
    print('wavy_text("String",amplitude=1, frequency=1)')
    print('vaporwave("String")')
    print('cc_text("String")')
    typewriter(
        red(
            'typewriter("string",0.1) : Typewriter effect String + speed (default speed=0.1)'
        )
    )
    print()
    print(bold(red("Contact : https://t.me/onefinalhug")))
