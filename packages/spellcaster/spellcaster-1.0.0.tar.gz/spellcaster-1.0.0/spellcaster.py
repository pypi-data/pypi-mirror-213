"""
A module programmed by Omer Drkić that adds loads of new features and makes Python easier to use.
"""

import keyboard as lib_keyboard
import os as lib_os
import random as lib_random
import subprocess as lib_subprocess
import time as lib_time

timer = lib_time.time()

def choose(*values):
  """
  Returns a random item from the specified tuple.
  """
  return lib_random.choice(values)

def chooseindex(index: int, *values):
  """
  Returns an item from the specified tuple using a zero-based index.
  """
  return values[index]

def clear():
  """
  Clears the previous console output.
  """
  lib_os.system("cls")

def key(key: int):
  """
  Pauses the program until the requested key is pressed.
  """
  if key == 0:
    lib_keyboard.wait("escape")
  elif key == 1:
    lib_keyboard.wait("f1")
  elif key == 2:
    lib_keyboard.wait("f2")
  elif key == 3:
    lib_keyboard.wait("f3")
  elif key == 4:
    lib_keyboard.wait("f4")
  elif key == 5:
    lib_keyboard.wait("f5")
  elif key == 6:
    lib_keyboard.wait("f6")
  elif key == 7:
    lib_keyboard.wait("f7")
  elif key == 8:
    lib_keyboard.wait("f8")
  elif key == 9:
    lib_keyboard.wait("f9")
  elif key == 10:
    lib_keyboard.wait("f10")
  elif key == 11:
    lib_keyboard.wait("f11")
  elif key == 12:
    lib_keyboard.wait("f12")
  elif key == 13:
    lib_keyboard.wait("asciitilde")
  elif key == 14:
    lib_keyboard.wait("num 1")
  elif key == 15:
    lib_keyboard.wait("num 2")
  elif key == 16:
    lib_keyboard.wait("num 3")
  elif key == 17:
    lib_keyboard.wait("num 4")
  elif key == 18:
    lib_keyboard.wait("num 5")
  elif key == 19:
    lib_keyboard.wait("num 6")
  elif key == 20:
    lib_keyboard.wait("num 7")
  elif key == 21:
    lib_keyboard.wait("num 8")
  elif key == 22:
    lib_keyboard.wait("num 9")
  elif key == 23:
    lib_keyboard.wait("num 0")
  elif key == 24:
    lib_keyboard.wait("num minus")
  elif key == 25:
    lib_keyboard.wait("equal")
  elif key == 26:
    lib_keyboard.wait("tab")
  elif key == 27:
    lib_keyboard.wait("caps lock")
  elif key == 28:
    lib_keyboard.wait("left shift")
  elif key == 29:
    lib_keyboard.wait("left control")
  elif key == 30:
    lib_keyboard.wait("left win")
  elif key == 31:
    lib_keyboard.wait("left alt")
  elif key == 32:
    lib_keyboard.wait("space")
  elif key == 33:
    lib_keyboard.wait("alt gr")
  elif key == 34:
    lib_keyboard.wait("right win")
  elif key == 35:
    lib_keyboard.wait("menu")
  elif key == 36:
    lib_keyboard.wait("right control")
  elif key == 37:
    lib_keyboard.wait("right shift")
  elif key == 38:
    lib_keyboard.wait("return")
  elif key == 39:
    lib_keyboard.wait("backspace")
  elif key == 40:
    lib_keyboard.wait("q")
  elif key == 41:
    lib_keyboard.wait("w")
  elif key == 42:
    lib_keyboard.wait("e")
  elif key == 43:
    lib_keyboard.wait("r")
  elif key == 44:
    lib_keyboard.wait("t")
  elif key == 45:
    lib_keyboard.wait("y")
  elif key == 46:
    lib_keyboard.wait("u")
  elif key == 47:
    lib_keyboard.wait("i")
  elif key == 48:
    lib_keyboard.wait("o")
  elif key == 49:
    lib_keyboard.wait("p")
  elif key == 50:
    lib_keyboard.wait("a")
  elif key == 51:
    lib_keyboard.wait("s")
  elif key == 52:
    lib_keyboard.wait("d")
  elif key == 53:
    lib_keyboard.wait("f")
  elif key == 54:
    lib_keyboard.wait("g")
  elif key == 55:
    lib_keyboard.wait("h")
  elif key == 56:
    lib_keyboard.wait("j")
  elif key == 57:
    lib_keyboard.wait("k")
  elif key == 58:
    lib_keyboard.wait("l")
  elif key == 59:
    lib_keyboard.wait("z")
  elif key == 60:
    lib_keyboard.wait("x")
  elif key == 61:
    lib_keyboard.wait("c")
  elif key == 62:
    lib_keyboard.wait("v")
  elif key == 63:
    lib_keyboard.wait("b")
  elif key == 64:
    lib_keyboard.wait("n")
  elif key == 65:
    lib_keyboard.wait("m")
  elif key == 66:
    lib_keyboard.wait("bracketleft")
  elif key == 67:
    lib_keyboard.wait("bracketright")
  elif key == 68:
    lib_keyboard.wait("semicolon")
  elif key == 69:
    lib_keyboard.wait("apostrophe")
  elif key == 70:
    lib_keyboard.wait("backslash")
  elif key == 71:
    lib_keyboard.wait("comma")
  elif key == 72:
    lib_keyboard.wait("dot")
  elif key == 73:
    lib_keyboard.wait("slash")
  elif key == 74:
    lib_keyboard.wait("up arrow")
  elif key == 75:
    lib_keyboard.wait("left arrow")
  elif key == 76:
    lib_keyboard.wait("down arrow")
  elif key == 77:
    lib_keyboard.wait("right arrow")
  elif key == 78:
    lib_keyboard.wait("num lock")
  elif key == 79:
    lib_keyboard.wait("num add")
  elif key == 80:
    lib_keyboard.wait("num sub")
  elif key == 81:
    lib_keyboard.wait("num multiply")
  elif key == 82:
    lib_keyboard.wait("num divide")
  elif key == 83:
    lib_keyboard.wait("num enter")
  elif key == 84:
    lib_keyboard.wait("insert")
  elif key == 85:
    lib_keyboard.wait("delete")
  elif key == 86:
    lib_keyboard.wait("home")
  elif key == 87:
    lib_keyboard.wait("end")
  elif key == 88:
    lib_keyboard.wait("page up")
  elif key == 89:
    lib_keyboard.wait("page down")
  elif key == 90:
    lib_keyboard.wait("print screen")
  elif key == 91:
    lib_keyboard.wait("scroll lock")
  elif key == 92:
    lib_keyboard.wait("pause break")

def random(min: float, max: float):
  """
  Returns a random float inside the specified range, including the lowest end but not the highest.
  """
  return lib_random.uniform(min, max)

def run(path: str, prog: str,):
  """
  Runs an external script file.
  """
  if prog == "batch":
    lib_subprocess.call([path])
  else:
    lib_subprocess.call([prog, path])

def time():
  """
  Returns the number of seconds that passed since the beginning of the program.
  """
  return int(lib_time.time() - timer)

def tstamp():
  """
  Returns the number of seconds that passed since epoch.
  """
  return int(lib_time.time())

def wait(interval: float):
  """
  Pauses the program for the given number of seconds.
  """
  lib_time.sleep(interval)