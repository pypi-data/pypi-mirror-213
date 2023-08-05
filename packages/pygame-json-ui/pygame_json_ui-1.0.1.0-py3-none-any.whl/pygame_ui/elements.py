"""
blabla
"""

import os
import sys

import pygame.font as pygfont
import pygame.rect as pygrect
import pygame.draw as pygdraw
import pygame.display as pygdisplay
import pygame.surface as pygsurface
import pygame._sdl2 as pygsdl2

from pygame_ui.constants import *


sys.path.append(os.getcwd())

pygfont.init()


class UI_Element:
	is_visible = True
	is_hoverable = False
	is_clickable = False
	position = [0,0]
	position_anchor = "top left"
	position_relative = False
	position_units = ["px","px"] # or ["w%", "h%"]
	size = [0,0]
	size_units = ["px", "px"] # or ["w%", "h%"]
	auto_size = False
	background_color = None
	use_sdl2 = False

	def __init__(self, initial_data, kwargs):
		if initial_data[0]['use_sdl2']:
			renderer = initial_data[0].pop('renderer')
		for dictionary in initial_data:
			for key in dictionary:
				setattr(self, key, dictionary[key])
		self.parent = kwargs.pop('parent')

		for key in kwargs:
			setattr(self, key, kwargs[key])
		
		self.position_initial = list(self.position)
		self.size_initial = list(self.size)
		self.change_position(self.position, self.position_units)
		self.change_size(self.size, self.size_units)

		if self.use_sdl2:
			if self.background_color != None:
				if len(self.background_color) < 4:
					bg_c = self.background_color + [255]
				else:
					bg_c = self.background_color
				image = pygsurface.Surface(self.size).convert_alpha()
				image.fill(bg_c)
				self.texture = pygsdl2.Texture.from_surface(renderer, image)

	def change_position(self, new_position, units=['px','px']):
		"""
		You can figure this one out yourself. If you can't then... *sigh*
		"""
		new_position = list(new_position)

		# Apply relative positioning
		position_zero = [0,0]
		if self.position_relative:
			percentage_target = self.parent.size
			position_zero = list(self.parent.position)
		else:
			percentage_target = pygdisplay.get_surface().get_size()

		# Apply anchor point
		if self.position_anchor == 'center':
			anchor = [0,0]
		else:
			anchor = [ANCHORS[self.position_anchor.split(' ')[i]] for i in [1,0]]
		
		# Apply percentages
		for i in [0, 1]:
			if units[i] == 'w%':
				new_position[i] = percentage_target[0]*new_position[i]/100
			elif units[i] == 'h%':
				new_position[i] = percentage_target[1]*new_position[i]/100
		
		self.position = [new_position[i] - (anchor[i]/2+.5)*self.size[i] + position_zero[i] for i in [0,1]]
		self.rectangle = pygrect.Rect(self.position, self.size)

	def change_size(self, new_size, units=['px','px']):
		"""
		You can figure this one out yourself. If you can't then... *sigh*
		"""
		new_size = list(new_size)
		
		# Apply relative positioning
		new_position = list(self.position)
		if self.position_relative:
			new_position = [self.position[i] - self.parent.position[i] for i in [0,1]]

		# Apply anchor point
		if self.position_anchor == 'center':
			anchor = [0,0]
		else:
			anchor = [ANCHORS[self.position_anchor.split(' ')[i]] for i in [1,0]]
		new_position = [new_position[i] + (anchor[i]/2+.5)*self.size[i] for i in [0,1]]

		# Apply percentages 
		percentage_target = pygdisplay.get_surface().get_size()
		for i in [0, 1]:
			if units[i] == 'w%':
				new_size[i] = percentage_target[0]*new_size[i]/100
			elif units[i] == 'h%':
				new_size[i] = percentage_target[1]*new_size[i]/100
		
		self.size = new_size

		# Calculate new position
		self.change_position(new_position)
	
	def draw_bg(self, pygame_window):
		draw_surface = pygsurface.Surface(pygdisplay.get_surface().get_size()).convert_alpha()
		draw_surface.fill((0,0,0,0))
		
		pygdraw.rect(draw_surface, self.background_color, self.rectangle)
		
		if len(self.background_color) < 4:
			draw_surface.set_alpha(255)

		pygame_window.blit(draw_surface, [0,0])
	
	def draw_bg_sdl2(self, renderer):
		# This works but i don't like it, it's not pretty and could probably be faster
		renderer.blit(self.texture, self.rectangle)
		# Something like this below would make more sense, but i couldn't get the alpha channel to work :(
		#renderer.draw_color = bg_c
		#renderer.alpha = bg_c[3]
		#renderer.fill_rect(self.rectangle)


class frame(UI_Element):
	"""
	The UI element that works as a sort of bundle or group.

	Yes, frame-ception is a thing.
	"""
	
	contents = {}

	def __init__(self, *initial_data, **kwargs):
		self.elements = {}
		if initial_data[0]['use_sdl2']:
			renderer = initial_data[0]['renderer']
		super().__init__(initial_data, kwargs)
		for name, data in self.contents.items():
			element_type = data.pop('type')
			data['use_sdl2'] = bool(self.use_sdl2)
			if self.use_sdl2:
				data['renderer'] = renderer
			self.elements[name] = globals()[element_type](data, parent=self)
	
	def get_text_input_elements(self):
		text_input_elements = []
		for name, element in self.elements.items():
			if element.is_visible:
				if isinstance(element, frame):
					text_input_elements.extend(element.get_text_input_elements())
				elif isinstance(element, text_input):
					text_input_elements.append(element)
		return text_input_elements

	def get_interactive_elements(self):
		interactives = []
		for name, element in self.elements.items():
			if element.is_visible:
				if isinstance(element, frame) and not isinstance(element, button):
					interactives.extend(element.get_interactive_elements())
				elif element.is_hoverable or element.is_clickable:
					interactives.append(element)
		return interactives
	
	def draw(self, pygame_window):
		for i in self.elements.values():
			if i.is_visible:
				if i.background_color != None:
					i.draw_bg(pygame_window)
				i.draw(pygame_window)
	
	def draw_sdl2(self, renderer):
		for i in self.elements.values():
			if i.is_visible:
				if i.background_color != None:
					i.draw_bg_sdl2(renderer)
				i.draw_sdl2(renderer)


class label(UI_Element):
	"""
	The UI element for text.

	Anything with letters will use this class.
	"""
	
	text = "Empty Label"
	text_color = (255,255,255)
	text_aa = True
	font_name = 'Arial'
	font_size = 10
	font_bold = False
	font_italic = False

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)
		self.font = pygfont.SysFont(self.font_name, self.font_size, self.font_bold, self.font_italic)
		if self.auto_size:
			if isinstance(self, label):
				self.change_size(self.font.size(self.text))
				self.rectangle = pygrect.Rect(self.position, self.size)
	
	def change_font(self, **kwargs):
		"""
		Used to change attributes of the font.

		The keyword arguments must exist in the following list:
		>>> ['font_name', 'font_size', 'font_bold', 'font_bold']
		"""

		for key in kwargs:
			if key in FONT_ATTRIBUTES:
				setattr(self, key, kwargs[key])
			else:
				raise KeyError(key+' is not a font attribute. '+MUST_BE+FONT_ATTRIBUTES+'\n'+ISSUE_REPORT)
		self.font = pygfont.SysFont(self.font_name, self.font_size, self.font_bold, self.font_italic)

	def draw(self, pygame_window):
		text_surface = self.font.render(self.text, self.text_aa, self.text_color, self.background_color)
		pygame_window.blit(text_surface, self.position)
	
	def draw_sdl2(self, renderer):
		text_surface = self.font.render(self.text, self.text_aa, self.text_color, self.background_color)
		if not 0 in text_surface.get_size():
			texture = pygsdl2.video.Texture.from_surface(renderer, text_surface)
			renderer.blit(texture, text_surface.get_rect().move(self.position))


class text_input(label):
	"""
	The UI element for an input field.

	My quote-bucket is empty :(
	"""
	is_clickable = True
	click_start = False
	click_end = False
	click_held = False
	typing_start_on_click = True
	typing_end_on_enter = True
	typing = False
	text = "Your input here"
	caret = False
	caret_timer = 0

	def draw(self, pygame_window):
		text_to_render = self.text
		if self.caret:
			text_to_render += '|'
		text_surface = self.font.render(text_to_render, self.text_aa, self.text_color, self.background_color)
		pygame_window.blit(text_surface, self.position)
	
	def draw_sdl2(self, renderer):
		text_to_render = self.text
		if self.caret:
			text_to_render += '|'
		text_surface = self.font.render(text_to_render, self.text_aa, self.text_color, self.background_color)
		if not 0 in text_surface.get_size():
			texture = pygsdl2.video.Texture.from_surface(renderer, text_surface)
			renderer.blit(texture, text_surface.get_rect().move(self.position))

class button(frame):
	"""
	The UI element for a button.

	What does this button do?
	"""
	is_clickable = True
	is_hoverable = True
	click_start = False
	click_end = False
	click_held = False
	hover_start = False
	hover_end = False
	hover_held = False


class switch(UI_Element):
	"""
	The UI element for a switch.

	Switcharoo!
	"""
	is_clickable = True
	is_hoverable = True
	click_start = False
	click_end = False
	click_held = False
	hover_start = False
	hover_end = False
	hover_held = False
	state = False
	preset = None

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)

	def draw(self, pygame_window):
		if self.preset == 'simple':
			size = [self.size[0]/2-5, self.size[1]-10]
			position = [self.position[0]+5+size[0]*int(self.state), self.position[1]+5]
			pygdraw.rect(pygame_window, (200,200,200), pygrect.Rect(position, size))

	def draw_sdl2(self, renderer):
		if self.preset == 'simple':
			size = [self.size[0]/2-5, self.size[1]-10]
			position = [self.position[0]+5+size[0]*int(self.state), self.position[1]+5]
			renderer.draw_color = (200,200,200,255)
			renderer.fill_rect(pygrect.Rect(position, size))

class slider(UI_Element):
	"""
	The UI element that slides.

	Sliiide to the left, sliiide to the right, criss cross!
	"""
	is_clickable = True
	is_hoverable = True
	click_start = False
	click_end = False
	click_held = False
	hover_start = False
	hover_end = False
	hover_held = False
	value_min = 0
	value_max = 1
	value = 0
	preset = None

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)

	def set_value_from_pos(self, position):
		if self.preset == 'simple':
			self.value/(self.value_max-self.value_min)
			x = (self.value_max - self.value_min) * (position[0]-self.size[1]/2 - self.position[0])/(self.size[0]-self.size[1])
			self.value = max(min(self.value_max, x), self.value_min)

	def draw(self, pygame_window):
		if self.preset == 'simple':
			size = [self.size[1]-10, self.size[1]-10]
			position = [self.position[0]+5+(self.size[0]-self.size[1])*self.value/(self.value_max-self.value_min), self.position[1]+5]
			pygdraw.rect(pygame_window, (200,200,200), pygrect.Rect(position, size))
	
	def draw_sdl2(self, renderer):
		if self.preset == 'simple':
			size = [self.size[1]-10, self.size[1]-10]
			position = [self.position[0]+5+(self.size[0]-self.size[1])*self.value/(self.value_max-self.value_min), self.position[1]+5]
			renderer.draw_color = (200,200,200,255)
			renderer.fill_rect(pygrect.Rect(position, size))


class dropdown(UI_Element):
	"""
	Unfinished
	"""
	is_clickable = True

	def __init__(self, *initial_data, **kwargs):
		super().__init__(initial_data, kwargs)

	def draw(self, pygame_window):
		pass