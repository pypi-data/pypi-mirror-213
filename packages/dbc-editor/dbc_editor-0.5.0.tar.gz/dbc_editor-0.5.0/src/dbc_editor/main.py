#!./runmodule.sh

'''
An editor for CAN bus database files like dbc or sym, based on cantools and urwid
'''

__version__ = '0.5.0'


import os
import sys
import argparse
import tempfile
import logging
import abc
from gettext import gettext as _

import urwid
import cantools

from .config import Config
from . import urwid_edit_with_history


ATTR_TITLE = 'title'
ATTR_HELP_LINE = 'help-line'
ATTR_ERROR = 'error'

CANCEL = 'cancel'

urwid.command_map['j'] = urwid.CURSOR_DOWN
urwid.command_map['k'] = urwid.CURSOR_UP
urwid.command_map['h'] = urwid.CURSOR_LEFT
urwid.command_map['l'] = urwid.CURSOR_RIGHT


# ------- base classes -------

# I am not inheriting from abc.ABC to avoid TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
class MyWindow(urwid.Frame):

	def __init__(self, body=None, **kw):
		self.prev_window = kw.pop('prev_window', None)
		self.errors: 'list[str]' = []
		self.help_line = None
		super().__init__(body, **kw)

	def set_body(self, body):
		self.body = body

	def set_title(self, title):
		self.header = urwid.Text((ATTR_TITLE, title))

	def set_help_line(self, shortcuts):
		'''shortcuts: iterable of (key, command) tuples'''
		ln = ", ".join(f"{key}: {cmd}" for key, cmd in shortcuts)
		self.help_line = urwid.Text((ATTR_HELP_LINE, ln))
		self.footer = self.help_line

	def cmd_back(self):
		return self.prev_window

	def cmd_search(self):
		search_edit = SearchEdit(self)
		search_edit.set_direction(reverse=False)
		self.footer = search_edit
		self.focus_position = "footer"

	def cmd_search_reverse(self):
		search_edit = SearchEdit(self)
		search_edit.set_direction(reverse=True)
		self.footer = search_edit
		self.focus_position = "footer"

	def search_do(self, text, **flags):
		self.body.search_do(text, **flags)

	def search_cancel(self):
		self.footer = self.help_line
		self.focus_position = "body"

	def show_error(self, msg: str) -> None:
		self.errors.append(msg)
		self.footer = urwid.Pile([urwid.Text((ATTR_ERROR, msg)) for msg in self.errors])

	def reset_errors(self) -> None:
		self.errors.clear()
		self.footer = self.help_line

	def keypress(self, size, key):
		self.reset_errors()
		return super().keypress(size, key)


	@abc.abstractmethod
	def get_selected_message(self) -> cantools.database.Message:
		raise NotImplementedError()


class MyListBox(urwid.ListBox):

	def search_do(self, text, **flags):
		#TODO
		pass

class LineWidget(urwid.Text):

	def keypress(self, size, key):
		return key

	def selectable(self):
		return True


# ------- input widgets -------

class EditBaseClass(urwid.Edit):

	def register_on_change_listener(self, callback: 'Callable[[Self, T], None]') -> None:
		urwid.connect_signal(self, 'postchange', callback)


class TextEdit(EditBaseClass):

	def check(self) -> bool:
		return bool(self.value())

	def value(self) -> str:
		return self.get_edit_text()

	def set_value(self, value: str) -> None:
		self.set_edit_text(value)
		self.set_edit_pos(len(self.get_edit_text()))

class OptionalTextEdit(EditBaseClass):

	def check(self) -> bool:
		return True

	def value(self) -> 'str|None':
		out = self.get_edit_text()
		if out:
			return out
		return None

	def set_value(self, value: 'str|None') -> None:
		if value is None:
			self.set_edit_text('')
		else:
			self.set_edit_text(value)
			self.set_edit_pos(len(self.get_edit_text()))

class HexEdit(EditBaseClass):

	fmt = '03X'

	# override method of super class
	def valid_char(self, ch: str) -> bool:
		return ch.lower() in '0123456789abcdef'

	def check(self) -> bool:
		return bool(self.get_edit_text())

	def value(self) -> int:
		return int(self.get_edit_text(), base=16)

	def set_value(self, value: int) -> None:
		self.set_edit_text(format(value, self.fmt))
		self.set_edit_pos(len(self.get_edit_text()))

class UintEdit(EditBaseClass):

	def __init__(self, caption: str, *, default_value: 'float|None' = None, fmt: str = '') -> None:
		super().__init__(caption=caption)
		self.default_value = default_value
		self.fmt = fmt

	# override method of super class
	def valid_char(self, ch: str) -> bool:
		return ch.lower() in '0123456789'

	def check(self) -> bool:
		if self.default_value is not None:
			return True
		return bool(self.get_edit_text())

	def value(self) -> int:
		if self.default_value is not None and not self.get_edit_text():
			return self.default_value
		return int(self.get_edit_text())

	def set_value(self, value: int) -> None:
		self.set_edit_text(format(value, self.fmt))
		self.set_edit_pos(len(self.get_edit_text()))

class UintListEdit(EditBaseClass):

	fmt = '%s'

	# override method of super class
	def valid_char(self, ch: str) -> bool:
		return ch.lower() in '0123456789xABCDEFabcdef, '

	def check(self) -> bool:
		try:
			self.value()
			return True
		except ValueError:
			return False

	def value(self) -> 'list[int]':
		return [int(i, base=0) for i in self.get_edit_text().split(',')]

	def set_value(self, value: 'list[int]') -> None:
		self.set_edit_text(', '.join(self.fmt % i for i in value))
		self.set_edit_pos(len(self.get_edit_text()))


class FloatEdit(EditBaseClass):

	def __init__(self, caption: str, *, default_value: 'float|None' = None, fmt: str = '') -> None:
		super().__init__(caption=caption)
		self.default_value = default_value
		self.fmt = fmt

	# override method of super class
	def valid_char(self, ch: str) -> bool:
		return ch.lower() in '-0123456789.'

	def check(self) -> bool:
		val = self.get_edit_text()
		if not val:
			return self.default_value is not None
		try:
			float(val)
			return True
		except ValueError:
			return False

	def value(self) -> float:
		val = self.get_edit_text()
		if not val:
			return self.default_value
		out = float(val)
		if out.is_integer():
			return int(out)
		return out

	def set_value(self, value: float) -> None:
		self.set_edit_text(format(value, self.fmt))
		self.set_edit_pos(len(self.get_edit_text()))


class PackableRadioButton(urwid.RadioButton):

	def pack(self, size=None, focus=False):
		text = ' '*self.reserve_columns + self.get_label()
		return urwid.Text(text).pack(size=size, focus=focus)

class ChoiceEdit(urwid.Columns):

	def __init__(self, caption: str, *, choices: 'list[str]|dict[str, T]') -> None:
		self.caption = caption
		self.choices: 'dict[str, T]' = choices if isinstance(choices, dict) else {v:v for v in choices}
		buttons_group = []
		self.caption = urwid.Text(caption)
		self.radio_buttons = {key: PackableRadioButton(buttons_group, key) for key in list(choices)}
		widgets = [self.caption] + list(self.radio_buttons.values())
		widget_list = [('pack', w) for w in widgets]
		super().__init__(widget_list, dividechars=1)

	def check(self) -> bool:
		return any(btn.state for btn in self.radio_buttons.values())

	def value(self) -> 'T':
		for key, rb in self.radio_buttons.items():
			if rb.state:
				return self.choices[key]

		return None

	def set_value(self, value: 'T') -> None:
		for key, val in self.choices.items():
			if val == value:
				self.radio_buttons[key].set_state(True)
				return

		raise ValueError('Invalid value %r. Should be one of %s' % (value, ', '.join(repr(v) for v in self.choices.values())))

	def register_on_change_listener(self, callback: 'Callable[[Self, T], None]') -> None:
		emit = [False]
		def wrapper(rbtn: urwid.RadioButton, old_state: bool):
			# This is triggered by every radio button which changes,
			# i.e. twice, once for the button which changes from True to False
			# and once for the button which changes from False to True.
			# Checking rbtn.state would ensure that callback is called only once
			# but depending on whether the selection is moved from left to right
			# or right to left it would be called before or after the update
			# so self.value() would be sometimes correct and sometimes not.
			# Instead I am using emit to ensure that callback is called every
			# second time wrapper is called.
			if emit[0]:
				callback(rbtn, self.value())
			emit[0] = not emit[0]

		for rbtn in self.radio_buttons.values():
			urwid.connect_signal(rbtn, 'postchange', wrapper)


# ------- search widget -------

class SearchEdit(urwid_edit_with_history.EditWithHistory):

	PROMPT = "/"
	PROMPT_REVERSE = "?"

	FLAG_SEP = "/"

	flags = {
		'c' : ('case_sensitive', True),
		'i' : ('case_sensitive', False),
		'e' : ('is_regex', True),
		'f' : ('is_regex', False),
	}

	def __init__(self, app):
		super().__init__(multiline=False)
		self.app = app
	
	def clear(self):
		self.edit_text = ""
	
	def set_direction(self, reverse):
		if reverse:
			caption = self.PROMPT_REVERSE
		else:
			caption = self.PROMPT

		self.set_caption(caption)

	def keypress(self, size, key):
		if not super().keypress(size, key):
			return

		cmd = self._command_map[key]
		if cmd == urwid.ACTIVATE:
			try:
				text, flags = self.parse_input()
			except ParseException as err:
				self.app.show_error(err.msg)
				return
			self.app.search_do(text, **flags)
		elif cmd == CANCEL:
			self.app.search_cancel()
	
	def parse_input(self):
		text = self.edit_text

		if self.FLAG_SEP in text:
			text, flags = text.rsplit(self.FLAG_SEP, 1)
			flags = self.parse_flags(flags)
		else:
			flags = {}

		return text, flags

	def parse_flags(self, text):
		flags = {}

		for c in text:
			if c in self.flags:
				key, val = self.flags[c]
				flags[key] = val
			else:
				supported_flags = _(",").join(self.flags.keys())
				self.error(_("invalid flag {flag}; should be one of {supported_flags}").format(flag=c, supported_flags=supported_flags))

		return flags

	def error(self, msg):
		raise ParseException(msg)

class ParseException(ValueError):

	def __init__(self, msg):
		super().__init__(msg)
		self.msg = msg


# ------- main window classes -------

class MyAttrMap(urwid.AttrMap):

	def __init__(self, widget):
		super().__init__(widget, None, CanDatabaseEditor.focus_map)


class ChoiceBox(urwid.Overlay):

	MIN_WIDTH = 30

	def __init__(self, bg, title, choices, cancel=None, **kw):
		self.choices = choices

		title = urwid.Text(title)
		buttons = urwid.Columns(urwid.Button(label, on_press=self.wrap_callback(callback)) for label, callback in choices.items())
		fg = urwid.Pile([title, buttons])
		fg = urwid.LineBox(fg)

		kw.setdefault('align', urwid.CENTER)
		kw.setdefault('valign', urwid.MIDDLE)
		kw.setdefault('width', self.get_width())
		kw.setdefault('height', None)
		super().__init__(fg, bg, **kw)

		if cancel:
			self.cmd_cancel = cancel
		else:
			self.cmd_cancel = lambda: bg

	def wrap_callback(self, callback) -> None:
		def wrapper(btn: urwid.Button) -> None:
			new_window = callback()
			if new_window:
				self.app.open_window(new_window)

		return wrapper

	def get_width(self):
		out = sum(len(c)+4 for c in self.choices)
		if out < self.MIN_WIDTH:
			out = self.MIN_WIDTH
		out += 2
		return out


class MessageList(MyWindow):

	title = 'messages in {fn}'
	_sort_key: 'Callable[[cantools.database.Message], object]'
	_reverse: bool

	def sort_by_name(self) -> object:
		self._sort_key = lambda msg: msg.name
		self._reverse = False
		self.update()

	def sort_by_id(self) -> object:
		self._sort_key = lambda msg: msg.frame_id
		self._reverse = False
		self.update()

	def sort_by_dbc(self) -> object:
		self._sort_key = lambda msg: self.db.messages.index(msg)
		self._reverse = False
		self.update()

	sortby_methods = {
		'dbc': sort_by_dbc,
		'id': sort_by_id,
		'name': sort_by_name,
	}

	_sort_by_keys = tuple(sortby_methods.keys())
	sortby = Config('message-list.sort-by', _sort_by_keys[0], allowed_values=_sort_by_keys)

	_command_map = MyWindow._command_map.copy()
	_command_map['0'] = 'sort_by_dbc'
	_command_map['1'] = 'sort_by_id'
	_command_map['2'] = 'sort_by_name'

	def __init__(self, db: cantools.database.Database, ffn: str) -> None:
		self.db = db
		path, fn = os.path.split(ffn)
		title = self.title.format(ffn=ffn, fn=fn)
		shortcuts = [
			('up/down', 'select message'),
			('+', 'new message'),
			('-', 'delete message'),
			('enter', 'show signals'),
			('i', 'edit message'),
			('q', 'quit'),
			('1', 'sort by id'),
			('2', 'sort by name'),
			('0', 'sort by dbc'),
		]

		super().__init__()
		self.set_title(title)
		self.set_help_line(shortcuts)
		self.sortby_methods[self.sortby](self)

	def update(self):
		content = [MyAttrMap(MessageLineWidget(msg)) for msg in sorted(self.db.messages, key=self._sort_key, reverse=self._reverse)]
		content = MyListBox(content)
		self.set_body(content)

	def _sort_key_name(self, msg: cantools.database.Message) -> str:
		return msg.name


	def keypress(self, size, key: str) -> 'str|None':
		if not super().keypress(size, key):
			return None

		cmd = self._command_map[key]
		if cmd == 'sort_by_id':
			self.sort_by_id()
		elif cmd == 'sort_by_name':
			self.sort_by_name()
		elif cmd == 'sort_by_dbc':
			self.sort_by_dbc()
		else:
			return key

		return None


	def get_selected_message(self):
		return self.body.focus.base_widget.msg

	def cmd_open(self):
		return SignalList(self.get_selected_message(), prev_window=self)

	def cmd_edit(self):
		return MessageEdit(self.db, self.get_selected_message(), prev_window=self)

	def cmd_new(self):
		return MessageEdit(self.db, prev_window=self)

	def cmd_remove(self):
		self.db.messages.remove(self.get_selected_message())
		self.update()
		self.app.notify_has_changed()

class MessageLineWidget(LineWidget):

	fmt_line = Config('message-list.fmt', '{msg.frame_id:>0{frame_id_width}x} {msg.name}  (DLC: {msg.length}, bytes used: {bytes_used})')

	def __init__(self, msg):
		bytes_used = sum(sig.length for sig in msg.signals) / 8.0
		if bytes_used.is_integer():
			bytes_used = int(bytes_used)
		ln = self.fmt_line.format(msg=msg, bytes_used=bytes_used,
			frame_format = "ext" if msg.is_extended_frame else "std",
			frame_id_width = 8 if msg.is_extended_frame else 3,
		)
		super().__init__(ln)
		self.msg = msg


class MessageEdit(MyWindow):

	title_edit = 'edit message {msg.frame_id:03x} {msg.name}'
	title_new = 'create new message'

	def __init__(self, db, msg=None, **kw):
		self.db = db
		self.msg = msg
		self.edit_frame_id = HexEdit("Frame ID (hex): ")
		self.edit_is_extended_frame = ChoiceEdit("", choices={"Extended Frame": True, "Standard Frame": False})
		self.edit_name = TextEdit("Message Name: ")
		self.edit_comment = OptionalTextEdit("Comment: ")
		self.edit_length = UintEdit("Data length (in bytes): ", default_value=0)

		if msg:
			title = self.title_edit.format(msg=msg)
			for key in ('frame_id', 'is_extended_frame', 'name', 'comment', 'length'):
				val = getattr(msg, key)
				if val is None:
					val = ''
				widget = getattr(self, 'edit_%s' % key)
				widget.set_value(val)
		else:
			title = self.title_new

		pile = urwid.Pile([
			self.edit_frame_id,
			self.edit_is_extended_frame,
			self.edit_name,
			self.edit_comment,
			self.edit_length,
		])
		filler = urwid.Filler(pile)

		super().__init__(filler, **kw)
		self.set_title(title)

	def get_input_data(self):
		out = {}
		out['frame_id'] = self.edit_frame_id.value()
		out['is_extended_frame'] = self.edit_is_extended_frame.value()
		out['name'] = self.edit_name.value()
		out['comment'] = self.edit_comment.value()
		out['length'] = self.edit_length.value()
		return out

	def check(self, *, silent: bool = False) -> bool:
		for w in (
			self.edit_frame_id,
			self.edit_is_extended_frame,
			self.edit_name,
			self.edit_comment,
			self.edit_length,
		):
			if not w.check():
				if not silent:
					self.show_error('Invalid input for %s' % w.caption.rstrip().rstrip(':'))
				return False

		return True

	def has_changed(self):
		if not self.msg:
			return True

		if not self.check(silent=True):
			return True

		data = self.get_input_data()
		for key in data:
			new_val = data[key]
			old_val = getattr(self.msg, key)
			if (new_val or old_val) and new_val != old_val:
				return True

		return False

	#TODO: this name is somewhat misleading for save but that is what activate is currently mapped to
	def cmd_open(self):
		return self.reply_save()

	def cmd_cancel(self):
		return super().cmd_back()

	def cmd_back(self):
		if self.has_changed():
			return ChoiceBox(bg=self, title='Save changes?', choices={'Yes':self.reply_save, 'No':self.reply_dont_save}, cancel=self.reply_cancel)

		return super().cmd_back()

	def reply_save(self):
		if not self.check():
			return

		if self.msg:
			for attr, value in self.get_input_data().items():
				setattr(self.msg, attr, value)
			out = self.prev_window
		else:
			newmsg = cantools.database.Message(signals=[], **self.get_input_data())
			self.db.messages.append(newmsg)
			out = SignalList(newmsg, prev_window=self.prev_window)

		self.prev_window.update()
		self.app.notify_has_changed()
		return out

	def reply_dont_save(self):
		return self.cmd_cancel()

	def reply_cancel(self):
		return self


	def get_selected_message(self) -> cantools.database.Message:
		return self.msg


class MessageLayout(MyWindow):

	title = 'layout of message {msg.frame_id:03x} {msg.name}'

	def __init__(self, msg, **kw):
		self.msg = msg

		import cantools.subparsers.dump.formatting
		layout = cantools.subparsers.dump.formatting.layout_string(msg)
		layout = '\n' + layout
		body = [urwid.Text(ln, wrap='clip') for ln in layout.splitlines()]
		body = MyListBox(body)

		shortcuts = [
			('up/down', 'scroll'),
			('left', 'back'),
			('q', 'quit')
		]

		super().__init__(body, **kw)
		self.set_title(self.title.format(msg=msg))
		self.set_help_line(shortcuts)


	#def cmd_open(self):
	#	return SignalList(self.msg, prev_window=self)

	def cmd_edit(self):
		return SignalList(self.msg, prev_window=self)

	def cmd_cancel(self):
		return self.cmd_back()


	def get_selected_message(self) -> cantools.database.Message:
		return self.msg


class SignalList(MyWindow):

	title = 'signals of message {msg.frame_id:03x} {msg.name}'

	def __init__(self, msg, **kw):
		self.msg = msg

		title = self.title.format(msg=msg)
		shortcuts = [
			('up/down', 'select signal'),
			('+', 'new signal'),
			('=', 'copy signal'),
			('-', 'delete signal'),
			('i', 'edit signal'),
			('q', 'quit')
		]
		body = [MyAttrMap(SignalLineWidget(sig)) for sig in sorted(self.msg.signals, key=lambda sig: sig.start)]
		body = MyListBox(body)

		super().__init__(body, **kw)
		self.set_title(title)
		self.set_help_line(shortcuts)

	def update(self):
		body = [MyAttrMap(SignalLineWidget(sig)) for sig in sorted(self.msg.signals, key=lambda sig: sig.start)]
		body = MyListBox(body)
		self.set_body(body)

	def select_signal(self, signal) -> None:
		for i, widget in enumerate(self.body.body):
			widget = widget.base_widget
			if widget.signal == signal:
				self.body.body.set_focus(i)
				return

	def get_selected_signal(self):
		return self.body.focus.base_widget.signal

	def cmd_open(self):
		return SignalEdit(self.msg, self.get_selected_signal(), prev_window=self)

	def cmd_edit(self):
		return SignalEdit(self.msg, self.get_selected_signal(), prev_window=self)

	def cmd_new(self):
		return SignalEdit(self.msg, prev_window=self)

	def cmd_copy(self):
		return SignalEdit(self.msg, self.get_selected_signal(), copy=True, prev_window=self)

	def cmd_remove(self):
		self.msg.signals.remove(self.get_selected_signal())
		self.update()
		self.app.notify_has_changed()


	def get_selected_message(self) -> cantools.database.Message:
		return self.msg

class SignalLineWidget(LineWidget):

	def __init__(self, signal):
		self.signal = signal

		unit = signal.unit if signal.unit else ''

		if signal.scale != 1 and signal.offset != 0:
			calc = '(x{signal.scale} {signal.offset:+})'
		elif signal.offset != 0:
			calc = f'{signal.offset:+}'
		elif signal.scale != 1:
			calc = f'x{signal.scale}'
		else:
			calc = ''

		if calc and unit:
			calc_unit = f'{calc}->{unit}'
		elif calc:
			calc_unit = calc
		else:
			calc_unit = unit

		super().__init__(f'{signal.name}  {signal.start},{signal.length}  {calc_unit}')


class SignalEdit(MyWindow):

	title_edit = 'edit signal {sig.name} of message {msg.frame_id:03x} {msg.name}'
	title_new = 'create new signal for message {msg.frame_id:03x} {msg.name}'

	TYPE_UNSIGNED_INT = 'uint'
	TYPE_SIGNED_INT = 'int'
	TYPE_FLOAT = 'float'
	TYPE_CHOICES = 'choices'
	TYPES = (TYPE_UNSIGNED_INT, TYPE_SIGNED_INT, TYPE_FLOAT, TYPE_CHOICES)

	BYTE_ORDER = {
		'Little Endian / Intel' : 'little_endian',
		'Big Endian / Motorola' : 'big_endian',
	}

	default_byte_order = Config('signal-edit.default-byte-order', 'little_endian', allowed_values=BYTE_ORDER.values())

	def __init__(self, msg, sig=None, *, copy: bool = False, **kw):
		self.msg = msg
		self.sig = sig
		self.copy = copy
		self.edit_name = TextEdit("Signal Name: ")
		self.edit_start = UintEdit("Start Bit: ")
		self.edit_length = UintEdit("Length (number of bits): ")
		self.edit_byte_order = ChoiceEdit("Byte Order: ", choices=self.BYTE_ORDER)
		self.edit_type = ChoiceEdit("Type: ", choices=self.TYPES)
		# Factor by which the raw value transmitted via the CAN bus must be multiplied in order to get the specified unit
		self.edit_scale = FloatEdit("Scale: ", default_value=1)
		# Summand by which the scaled value must be added in order to get the specified unit
		self.edit_offset = FloatEdit("Offset: ", default_value=0)
		self.edit_unit = OptionalTextEdit("Unit: ")
		self.edit_comment = OptionalTextEdit("Comment: ")
		self.text_value_range = urwid.Text("")
		self.edit_is_multiplexer = ChoiceEdit("Is multiplexer: ", choices={'true': True, 'false': False})
		self.edit_is_multiplexer.set_value(False)
		self.edit_is_multiplexed = ChoiceEdit("Depends on the value of another signal", choices={'true': True, 'false': False})
		self.edit_multiplexer_signal = ChoiceEdit("Multiplexer signal: ", choices=[s.name for s in msg.signals if s.is_multiplexer])
		self.edit_multiplexer_ids = UintListEdit("Multiplexer IDs: ")
		self.pile_multiplexed = urwid.Pile([self.edit_multiplexer_signal, self.edit_multiplexer_ids])
		self.pile_not_multiplexed = urwid.Text("")
		self.edit_is_multiplexed.set_value(False)
		for s in msg.signals:
			if s.is_multiplexer:
				self.edit_multiplexer_signal.set_value(s.name)
		self.placeholder_multiplexed = urwid.WidgetWrap(self.pile_not_multiplexed)
		self.edit_is_multiplexed.register_on_change_listener(self.change_is_multipexed)

		self.choices_input_mode_selector = ChoiceEdit('choice key', choices=('dec', 'hex'))
		self.choices_input_mode_selector.register_on_change_listener(self.change_choices_input_mode)
		self.choices_group: 'list[ChoiceLineEdit]' = []
		ChoiceLineEdit(self.choices_group, self.update_pile_choices)
		self.pile_choices = urwid.Pile([self.choices_input_mode_selector] + self.choices_group)
		self.pile_number = urwid.Pile([
			self.edit_scale,
			self.edit_offset,
			self.edit_unit,
		])
		self.placeholder = urwid.WidgetWrap(self.pile_number)
		self.edit_type.register_on_change_listener(self.on_type_change)

		if sig:
			title = self.title_edit.format(sig=sig, msg=msg)
			for key in ('name', 'start', 'length', 'byte_order', 'scale', 'unit', 'offset', 'comment'):
				val = getattr(sig, key)
				widget = getattr(self, 'edit_%s' % key)
				widget.set_value(val)
			if sig.choices:
				for val, name in sig.choices.items():
					self.choices_group[-1].set_value(val, str(name))
					# new ChoiceLineEdit are created automatically by ChoiceLineEdit.add_after_if_last
				self.edit_type.set_value(self.TYPE_CHOICES)
			elif sig.is_float:
				self.edit_type.set_value(self.TYPE_FLOAT)
			elif sig.is_signed:
				self.edit_type.set_value(self.TYPE_SIGNED_INT)
			else:
				self.edit_type.set_value(self.TYPE_UNSIGNED_INT)
			if sig.is_multiplexer:
				self.edit_is_multiplexer.set_value(True)
			if sig.multiplexer_signal:
				self.edit_is_multiplexed.set_value(True)
				self.edit_multiplexer_signal.set_value(sig.multiplexer_signal)
				self.edit_multiplexer_ids.set_value(sig.multiplexer_ids)
		else:
			self.edit_byte_order.set_value(self.default_byte_order)
			#TODO: does this work for big endian, too?
			if self.msg.signals:
				last_signal = self.msg.signals[-1]
				self.edit_start.set_value(last_signal.start + last_signal.length)
			else:
				self.edit_start.set_value(0)
			title = self.title_new.format(msg=msg)

		pile = urwid.Pile([
			self.edit_start,
			self.edit_name,
			self.edit_length,
			self.edit_type,
			self.placeholder,
			self.edit_comment,
			self.edit_byte_order,
			self.text_value_range,
			self.edit_is_multiplexer,
			self.edit_is_multiplexed,
			self.placeholder_multiplexed,
		])
		filler = urwid.Filler(pile)

		super().__init__(filler, **kw)
		self.set_title(title)
		self.init_value_range()
		pile.set_focus(1)

	def change_choices_input_mode(self, widget: ChoiceEdit, value: str) -> None:
		if value == 'hex':
			for w in self.choices_group:
				w.set_input_mode_to_hex()
		elif value == 'dec':
			for w in self.choices_group:
				w.set_input_mode_to_dec()
		else:
			assert False, f'invalid value {value} should be hex or dec'

	def change_is_multipexed(self, widget: ChoiceEdit, value: bool) -> None:
		self.placeholder_multiplexed._w = self.pile_multiplexed if value else self.pile_not_multiplexed

	def init_value_range(self) -> None:
		dependencies = (
			self.edit_length,
			self.edit_type,
			self.edit_scale,
			self.edit_offset,
			self.edit_unit,
		)
		def get_value_range() -> str:
			if not all(w.check() for w in dependencies):
				return ''

			length = self.edit_length.value()
			dtype = self.edit_type.value()
			scale = self.edit_scale.value()
			offset = self.edit_offset.value()
			unit = self.edit_unit.value()

			if dtype == self.TYPE_UNSIGNED_INT:
				min_val = 0
				max_val = 2**length - 1
			elif dtype == self.TYPE_SIGNED_INT:
				p = 2 ** (length-1)
				min_val = -p
				max_val = p - 1
			else:
				return ''

			min_val *= scale
			max_val *= scale

			# offset is added after scale
			# see cantools.database.utils.decode_data
			# https://github.com/cantools/cantools/blob/master/cantools/database/utils.py
			min_val += offset
			max_val += offset

			if unit is None:
				unit = ''

			return '(value range: {min_val}{unit}..{max_val}{unit})'.format(min_val=min_val, max_val=max_val, unit=unit)
		def update() -> None:
			self.text_value_range.set_text(get_value_range())
		for w in dependencies:
			w.register_on_change_listener(lambda widget, value: update())

		update()

	def on_type_change(self, widget, value) -> None:
		if value == self.TYPE_CHOICES:
			self.placeholder._w = self.pile_choices
		else:
			self.placeholder._w = self.pile_number

	def update_pile_choices(self) -> None:
		self.pile_choices = urwid.Pile([self.choices_input_mode_selector] + self.choices_group, focus_item=self.pile_choices.get_focus())
		self.placeholder._w = self.pile_choices


	def get_input_data(self):
		dtype = self.edit_type.value()
		if dtype and dtype not in self.TYPES:
			raise ValueError('invalid type %r, should be one of %s' % (dtype, self.TYPES))

		out = {}
		out['name'] = self.edit_name.value()
		out['start'] = self.edit_start.value()
		out['length'] = self.edit_length.value()
		out['is_signed'] = dtype in {self.TYPE_SIGNED_INT, self.TYPE_FLOAT}
		out['is_float'] = dtype == self.TYPE_FLOAT
		out['byte_order'] = self.edit_byte_order.value()
		out['scale'] = self.edit_scale.value()
		out['offset'] = self.edit_offset.value()
		out['unit'] = self.edit_unit.value()
		out['comment'] = self.edit_comment.value()
		out['choices'] = {c.edit_value.value() : c.edit_name.value() for c in self.choices_group if c.edit_name.check()} if dtype == self.TYPE_CHOICES else None
		out['is_multiplexer'] = self.edit_is_multiplexer.value()
		if self.edit_is_multiplexed.value():
			out['multiplexer_signal'] = self.edit_multiplexer_signal.value()
			out['multiplexer_ids'] = self.edit_multiplexer_ids.value()
		else:
			out['multiplexer_signal'] = None
			out['multiplexer_ids'] = None
		return out

	def check(self, *, silent: bool = False) -> bool:
		if self.edit_type.value() == self.TYPE_CHOICES:
			placeholder_edits = tuple(c.edit_value for c in self.choices_group if c.edit_name.check())
		else:
			placeholder_edits = tuple(widget for widget, options in self.pile_number.contents)
		if self.edit_is_multiplexed.value():
			placeholder_mux = (self.edit_multiplexer_signal, self.edit_multiplexer_ids)
		else:
			placeholder_mux = tuple()
		for w in (
			self.edit_name,
			self.edit_start,
			self.edit_length,
			self.edit_type,
			self.edit_byte_order,
			self.edit_comment,
			self.edit_is_multiplexer,
			self.edit_is_multiplexed,
		) + placeholder_edits + placeholder_mux:
			if not w.check():
				if not silent:
					self.show_error('Invalid input for %s' % w.caption.rstrip().rstrip(':'))
				return False

		if self.edit_is_multiplexer.value() == False:
			multiplexed_signals = self.get_signals_depending_on_this_signal()
			if multiplexed_signals:
				if not silent:
					self.show_error('This signal cannot be disabled as a multiplexer because the following signals depend on it: %s' % ', '.join(s.name for s in multiplexed_signals))
				return False

		if self.edit_is_multiplexed.value():
			try:
				multiplexer_signal = self.msg.get_signal_by_name(self.edit_multiplexer_signal.value())
			except KeyError:
				if not silent:
					self.show_error('This message does not have a signal named %r' % self.edit_multiplexer_signal.value())
				return False
			if multiplexer_signal.name == self.edit_name.value():
				if not silent:
					self.show_error('This signal cannot be multiplexed by itself')
				return False
			if not multiplexer_signal.is_multiplexer:
				if not silent:
					self.show_error('%s is not multiplexer' % multiplexer_signal)
				#return False

			multiplexer_ids = self.edit_multiplexer_ids.value()
			if not multiplexer_ids:
				if not silent:
					self.show_error('No multiplexer IDs specified which would activate this signal')
				return False
			id_too_big = 1 << multiplexer_signal.length
			for i in multiplexer_ids:
				if i >= id_too_big:
					if not silent:
						self.show_error(f'Multiplexer ID {i} is too big, {multiplexer_signal.name} is only {multiplexer_signal.length} bits long')
					return False

		return True

	def get_signals_depending_on_this_signal(self) -> 'list[cantools.db.Signal]':
		if not self.sig:
			return []
		return [s for s in self.msg.signals if s.multiplexer_signal == self.sig.name]

	def has_changed(self):
		if not self.sig:
			return True

		if not self.check(silent=True):
			return True

		data = self.get_input_data()
		for key in data:
			new_val = data[key]
			old_val = getattr(self.sig, key)
			if (new_val or old_val) and new_val != old_val:
				return True

		return False

	#TODO: this name is somewhat misleading for save but that is what activate is currently mapped to
	def cmd_open(self):
		return self.reply_save()

	def cmd_cancel(self):
		return super().cmd_back()

	def cmd_back(self):
		if self.has_changed():
			return ChoiceBox(bg=self, title='Save changes?', choices={'Yes':self.reply_save, 'No':self.reply_dont_save}, cancel=self.reply_cancel)

		return super().cmd_back()

	def reply_save(self):
		if not self.check():
			return

		if self.sig and not self.copy:
			for attr, value in self.get_input_data().items():
				if attr == 'name' and self.sig.name != value:
					for s in self.get_signals_depending_on_this_signal():
						s.multiplexer_signal = value
				setattr(self.sig, attr, value)
		else:
			newsig = cantools.database.Signal(**self.get_input_data())
			if self.sig:
				i = self.msg.signals.index(self.sig) + 1
			else:
				i = len(self.msg.signals)
			self.msg.signals.insert(i, newsig)
			self.sig = newsig
			self.copy = False

		self.prev_window.update()
		self.prev_window.select_signal(self.sig)
		self.app.notify_has_changed()
		return self.cmd_cancel()

	def reply_dont_save(self):
		return self.cmd_cancel()

	def reply_cancel(self):
		return self


	def get_selected_message(self) -> cantools.database.Message:
		return self.msg



class ChoiceLineEdit(urwid.Columns):

	min_value_width = 3

	# ------- init -------

	def __init__(self, group: 'list[ChoiceLineEdit]', update_pile: 'Callable[[], None]', *, before: 'ChoiceLineEdit|None' = None, value_edit_type: 'type[UintEdit|HexEdit]' = UintEdit) -> None:
		self.group = group
		self.update_pile = update_pile
		self.edit_value: 'UintEdit|HexEdit' = value_edit_type('')
		self.edit_name = TextEdit('')

		if before is None:
			group.append(self)
		else:
			group.insert(group.index(before), self)
		self.init_value()
		super().__init__([], dividechars=1)
		self._update_widgets()
		self.edit_name.register_on_change_listener(lambda w, v: self.add_after_if_last())

	def init_value(self) -> None:
		prev = self.get_prev_value()
		self.edit_value.set_value(0 if prev is None else prev+1)

	def get_prev_value(self) -> 'int|None':
		i = self.group.index(self) - 1
		while i >= 0:
			prev_widget = self.group[i]
			if prev_widget.edit_value.check():
				return prev_widget.edit_value.value()
			i -= 1
		return None

	def set_value(self, value: int, name: str) -> None:
		self.edit_value.set_value(value)
		self.edit_name.set_value(name)
		self._update_widgets()

	def set_input_mode_to_hex(self) -> None:
		val = self.edit_value.value()
		self.edit_value = HexEdit('')
		self.edit_value.set_value(val)
		self._update_widgets()

	def set_input_mode_to_dec(self) -> None:
		val = self.edit_value.value()
		self.edit_value = UintEdit('')
		self.edit_value.set_value(val)
		self._update_widgets()

	def _update_widgets(self) -> None:
		needed_with = len(self.edit_value.get_text()[0])
		value_width = max(self.min_value_width, needed_with)
		value_width += 1
		self.contents = [
			(self.edit_value, self.options('given', value_width)),
			(self.edit_name, self.options('weight', 1)),
		]

	# ------- events -------

	def add_after_if_last(self) -> None:
		i = self.group.index(self)
		if i < len(self.group) - 1:
			return

		ChoiceLineEdit(self.group, self.update_pile, value_edit_type=type(self.edit_value))
		self.update_pile()

	#TODO: this is not called. Does the UintEdit gobble the event?
	def cmd_new(self) -> None:
		self.add_before()

	#TODO: this is not called. Does the UintEdit gobble the event?
	def cmd_remove(self) -> None:
		self.group.remove(self)
		#TODO: decrement numbers of following
		self.update_pile()

	def add_before(self) -> None:
		ChoiceLineEdit(self.group, self.update_pile, before=self, value_edit_type=type(self.edit_value))
		#TODO: change duplicate numbers
		self.update_pile()


# ------- main classes -------

class UserInputError(Exception):
	pass

class CanDatabaseEditor:

	palette = [
		(ATTR_TITLE, 'brown', 'default'),
		(ATTR_HELP_LINE, 'dark blue', 'default'),
		(ATTR_ERROR, 'dark red', 'default'),
	]

	focus_map = {}

	command_map = urwid.command_map
	command_map['w'] = 'write'
	command_map['q'] = 'quit'
	command_map['e'] = 'edit'
	command_map['i'] = 'edit'
	command_map['esc'] = 'cancel'
	command_map['+'] = 'new'
	command_map['='] = 'copy'
	command_map['-'] = 'remove'
	command_map['/'] = 'search'
	command_map['?'] = 'search_reverse'
	command_map['v'] = 'message_layout'

	fallback_commands = {
		'activate' : 'open',
		'cursor right' : 'open',
		'cursor left' : 'back',
	}

	# see what is supported by dump_file in
	# https://github.com/cantools/cantools/blob/master/cantools/database/__init__.py
	supported_database_formats = ('dbc', 'kcd', 'sym')

	def __init__(self, fn=None):
		self.init_focus_map()
		self.has_changed = False
		if fn and os.path.isfile(fn):
			self.db = cantools.database.load_file(fn, prune_choices=False, sort_signals=None)
		else:
			if fn.split(os.path.extsep)[-1] not in self.supported_database_formats:
				raise UserInputError('invalid database format, should be one of %s' % ', '.join(self.supported_database_formats))
			self.db = cantools.database.Database()
		self.filename = fn

		MessageList.app = self
		MessageEdit.app = self
		SignalList.app = self
		SignalEdit.app = self
		ChoiceBox.app = self

		self.logging_handler = LoggingHandler(self)
		logging.basicConfig(handlers=[self.logging_handler], format='%(message)s', level=logging.WARNING)

	def init_focus_map(self):
		for name, fg, bg in tuple(self.palette):
			name_focused = name + '_focused'
			self.palette.append((name_focused, fg+',standout', bg))
			self.focus_map[name] = name_focused

		self.focus_map[None] = 'default_focused'
		self.palette.append(('default_focused', 'default,standout', 'default'))

	def run(self):
		widget = MessageList(self.db, self.filename)
		self.loop = urwid.MainLoop(widget, self.palette, handle_mouse=False, unhandled_input=self.unhandled_input)
		self.loop.run()

	def get_current_window(self) -> MyWindow:
		return self.loop.widget

	def open_window(self, window):
		self.loop.widget = window

	def unhandled_input(self, key):
		cmd = self.command_map[key]
		cmd = self.fallback_commands.get(cmd, cmd)
		if cmd == 'quit':
			self.quit()
			return
		elif cmd == 'write':
			self.write()
			return
		elif cmd == 'message_layout':
			current_window = self.get_current_window()
			if isinstance(current_window, MessageLayout):
				return
			self.open_window(MessageLayout(current_window.get_selected_message(), prev_window=current_window))
			return

		window = self.get_current_window()
		func = getattr(window, 'cmd_%s' % cmd, None)
		if func:
			new_window = func()
			if new_window:
				self.open_window(new_window)


	def show_error(self, msg: str) -> None:
		self.loop.widget.show_error(msg)


	# ------- write and quit -------

	def notify_has_changed(self):
		self.has_changed = True

	def quit(self):
		if self.has_changed:
			self.open_window(ChoiceBox(bg=self.get_current_window(), title='Save changes?', choices={'Yes':self.write_and_quit, 'No':self.quit_without_write}))
			return

		self.quit_without_write()

	def write_and_quit(self):
		self.write()
		self.quit_without_write()

	def write(self):
		if not self.check():
			return

		cantools.database.dump_file(self.db, self.filename)
		self.has_changed = False

	def check(self) -> bool:
		self.logging_handler.reset_errors()
		with tempfile.TemporaryDirectory() as tmppath:
			fn = os.path.join(tmppath, os.path.split(self.filename)[1])
			cantools.database.dump_file(self.db, fn)
			try:
				cantools.database.load_file(fn, prune_choices=False, sort_signals=None)
			except Exception as e:
				self.show_error(str(e))
				return False

		if self.logging_handler.has_errors():
			return False

		return True

	def quit_without_write(self):
		raise urwid.ExitMainLoop()


class LoggingHandler(logging.Handler):

	def __init__(self, app: CanDatabaseEditor) -> None:
		super().__init__()
		self.app = app
		self._has_errors = False

	def emit(self, record: logging.LogRecord):
		if not self.has_errors():
			self.app.show_error(_('The following error(s) would occur when trying to load this database. Please fix them before saving it:'))
		msg = self.format(record)
		self.app.show_error(msg)
		self._has_errors = True


	def has_errors(self) -> bool:
		return self._has_errors

	def reset_errors(self) -> None:
		self._has_errors = False


class PrintVersion(argparse.Action):

	def __init__(self, option_strings, dest, **kwargs):
		kwargs.setdefault('nargs', 0)
		argparse.Action.__init__(self, option_strings, dest, **kwargs)

	def __call__(self, parser, namespace, values, option_string=None):
		print(__version__)
		sys.exit(0)


def main(arglist: 'list[str]|None' = None) -> None:
	p = argparse.ArgumentParser(description=__doc__)
	p.add_argument("-v", "--version", action=PrintVersion, help="show the version number of this program and exit")
	p.add_argument('file', help='CAN bus database file, e.g. dbc or sym file')

	args = p.parse_args(arglist)
	try:
		dbeditor = CanDatabaseEditor(args.file)
		dbeditor.run()
	except UserInputError as e:
		print(e)


if __name__ == '__main__':
	main()
