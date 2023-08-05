"""
Pygame UI
=========

A python library for quickly building user interfaces with pygame in a JSON.

Make sure you read the ``Getting started`` section of the documentation at https://pypi.org/project/pygame-json-ui/ or https://github.com/Rednax-Code/pygame_ui.
"""

from pygame_ui.base import *
from pygame_ui.elements import *

# release, year, month, session
__version__ = '1.0.1.0'

print('pygame-json-ui ' + __version__)

def test():
	try:
		import pygame_ui.base
		import pygame_ui.constants
		import pygame_ui.elements
		print('Successfully installed! enjoy :)\nversion: '+__version__+'\n'+ANY_QUESTIONS)
		del pygame_ui.base, pygame_ui.constants, pygame_ui.elements
	except:
		print(ISSUE_REPORT)

# Base64
# VGhpcyBjb2RlIHdhcyB3cml0dGVuIGJ5IFJlZG5heEdhbWluZyBvbiBnaXRodWI=