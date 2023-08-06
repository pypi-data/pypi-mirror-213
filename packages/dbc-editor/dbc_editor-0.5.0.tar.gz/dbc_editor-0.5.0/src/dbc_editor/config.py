#!./runmodule.sh

import os

class Config:

	instances = {}

	def __init__(self, key, default, *, help=None, allowed_values=None):
		self.key = key
		self.value = default
		self.type = type(default)
		self.help = help
		self.allowed_values = allowed_values

		cls = type(self)
		assert key not in cls.instances, 'duplicate config key %r' % key
		cls.instances[key] = self

	def __get__(self, instance, owner=None):
		if instance is None:
			return self

		return self.value

	def __set__(self, instance, value):
		self.value = value

	def __repr__(self):
		return "%s(%s)" % (type(self).__name__, ", ".join(repr(a) for a in (self.key, self.value)))


	def parse_and_set_value(self, value):
		'''throws ValueError if value is invalid'''
		self.value = self.parse_value(value)

	def parse_value(self, value):
		'''throws ValueError if value is invalid'''
		if self.type == int:
			return int(value, base=0)
		if self.allowed_values and value not in self.allowed_values:
			raise ValueError(f'invalid value for {self.key}: {value!r} (should be one of {self.format_allowed_values()})')
		return self.type(value)

	def format_allowed_values(self):
		return ", ".join(repr(v) for v in self.allowed_values)

	def value_to_str(self):
		return str(self.value)


	# ------- class methods -------

	COMMENT = '#'
	KEY_VAL_SEP = '='
	INCLUDE = 'include '

	@classmethod
	def load(cls, fn):
		with open(fn, 'rt') as f:
			for lnno, ln in enumerate(f, 1):
				cls.parse_line(ln, lnno, f)

	@classmethod
	def parse_line(cls, ln, lnno=None, f=None):
		ln = ln.strip()
		if not ln:
			return
		if ln.startswith(cls.COMMENT):
			return

		if ln.startswith(cls.INCLUDE):
			fn = ln[len(cls.INCLUDE):].lstrip()
			fn = os.path.expanduser(fn)
			if f and not os.path.isabs(fn):
				fn = os.path.join(os.path.split(os.path.abspath(f.name))[0], fn)

			if os.path.isfile(fn):
				cls.load(fn)
			else:
				cls.parse_error(f"no such file {fn!r}", ln, lnno)
			return

		if cls.KEY_VAL_SEP not in ln:
			cls.parse_error(f"missing {cls.KEY_VAL_SEP}", ln, lnno)
			return

		key, value = ln.split(cls.KEY_VAL_SEP, 1)
		key = key.rstrip()
		value = value.lstrip()

		if key not in cls.instances:
			cls.parse_error(f"invalid key {key!r}", ln, lnno)
			return

		instance = cls.instances[key]
		try:
			instance.parse_and_set_value(value)
		except ValueError as e:
			cls.parse_error(str(e), ln, lnno)


	@classmethod
	def save(cls, fn):
		with open(fn, 'wt') as f:
			for key in sorted(cls.instances):
				instance = cls.instances[key]
				value = instance.value_to_str()
				ln = f"{key} = {value}\n"
				f.write(ln)


	@classmethod
	def parse_error(cls, msg, ln, lnno):
		if lnno:
			lnno = ' %s' % lnno
		else:
			lnno = ''
		msg +=  f" while trying to parse line{lnno} {ln!r}"
		cls.error(msg)

	@classmethod
	def error(cls, msg):
		with open('config-errors.txt', 'at') as f:
			print(msg, file=f)


if __name__ == '__main__':
	fn = "test.conf"

	class Test:
		a = Config('a', 1)
		b = Config('b', 2)
		c = Config('c', 'c')
		d = Config('d', 'd1', allowed_values=('d1', 'd2', 'd3'))

	t = Test()
	print("default values:")
	print("Test.a: %r" % Test.a)
	print("t.a: %r" % t.a)
	print("t.b: %r" % t.b)
	print("t.c: %r" % t.c)
	print("t.d: %r" % t.d)

	if os.path.exists(fn):
		Config.load(fn)
		print("loaded values:")
		print("Test.a: %r" % Test.a)
		print("t.a: %r" % t.a)
		print("t.b: %r" % t.b)
		print("t.c: %r" % t.c)
		print("t.d: %r" % t.d)

	t.a += 1
	print("modified value:")
	print("Test.a: %r" % Test.a)
	print("t.a: %r" % t.a)
	print("t.b: %r" % t.b)
	print("t.c: %r" % t.c)
	print("t.d: %r" % t.d)

	Config.save(fn)
