from copy import deepcopy
# import re
import regex 
from functools import lru_cache
import itertools
from logging import getLogger


logger = getLogger(name=__name__)


DEFANG_WRAPPERS = {
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>',
}

ZERO_WIDTH = chr(0x200b)

DEFANG_CHARACTERS = (
	''.join(o+c for o, c in DEFANG_WRAPPERS.items()) + ZERO_WIDTH)

DEFANG_CHARACTER_REGEX = regex.compile(fr'[{regex.escape(DEFANG_CHARACTERS)}]')


class DefaultFormatMap(dict):
	def __getitem__(self, key):
		try:
			return super().__getitem__(key)
		except KeyError:
			return f'{{{key}}}'


class Template:
	def __init__(self, format, normalised=None, data=None):
		self.format_string = str(format)
		data = {} if data is None else data
		self.data = DefaultFormatMap(data)
		self.normalised = normalised
		self.globals = {}

	def __str__(self):
		escaped = self.expand_format(component_map=self.data)
		return escaped.replace(r'{{', r'{').replace(r'}}', r'}')

	def __repr__(self):
		return f'{self.__class__}({self.format_string})'

	def __setitem__(self, key, value):
		if not isinstance(value, self.__class__):
			value = self.__class__(format=value)

		self.data[key] = value

	def __getitem__(self, key):
		return self.data[key]

	def __deepcopy__(self, memo=None):
		format_string = self.format_string
		data = deepcopy(self.data)
		return self.__class__(
			format=format_string, normalised=self.normalised, data=data)

	@property
	def regex(self):
		return compile_regex(str(self))

	def expand_format(self, component_map):
		format = self.format_string.replace(r'{{', r'{{{{')
		format = format.replace(r'}}', r'}}}}')
		return format.format_map(component_map)

	def normalise(self, text):
		if self.normalised is None:
			raise ValueError('Missing a normalisation value')

		return self.regex.sub(self.normalised, text)

	@classmethod
	def from_defang_pattern(
			cls,
			pattern,
			normalised,
			openers=None,
			match_unwrapped=True,
			allow_unbalanced=True,
	):
		if openers is None:
			openers = DEFANG_WRAPPERS.keys()

		components = (
			(
				regex.escape(o).replace('{', '{{'),
				pattern,
				regex.escape(DEFANG_WRAPPERS[o]).replace('}', '}}'),
			)
			for o in openers
		)

		if match_unwrapped and allow_unbalanced:
			components = ((f'{o}?', p, f'{c}?') for o, p, c in components)
		elif allow_unbalanced:
			components = itertools.chain(
				((f'{o}', p, f'{c}?') for o, p, c in components),
				((f'{o}?', p, f'{c}') for o, p, c in components),
			)
		elif match_unwrapped:
			components = itertools.chain(components, [('', pattern, '')])

		#atomic
		template_format = '(?>{})'.format(
			'|'.join(f'{o}(?>{p}){c}' for o, p, c in components))

		logger.debug('Refanging template format: %r', template_format)
		return cls(format=template_format, normalised=normalised)


@lru_cache
def compile_regex(pattern):
	return regex.compile(pattern)
