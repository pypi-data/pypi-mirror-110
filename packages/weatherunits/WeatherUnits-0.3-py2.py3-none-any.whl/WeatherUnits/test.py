# from enum import Enum as _Enum, EnumMeta as _Meta
# from types import DynamicClassAttribute
#
# from src.WeatherUnits import Measurement
#
#
# class Enum(_Enum):
#
# 	# @DynamicClassAttribute
# 	# def cls(self):
# 	# 	"""The name of the Enum member."""
# 	# 	return type(self._name_, (Measurement,), {'name': 'dog'})
#
# 	def __init__(self, *args):
# 		self._class_ = type(self._name_, (Measurement,), {'name': 'dog'})
# 		return super(Enum, self).__init__()
#
#
# class AddressableEnum(_Meta):
#
# 	def __new__(mcs, cls, bases, classdict):
# 		return super().__new__(mcs, cls, bases, classdict)
#
# 	def __getitem__(self, indexOrName):
# 		if isinstance(indexOrName, str):
# 			return super().__getitem__(indexOrName)
# 		elif isinstance(indexOrName, int) and indexOrName < super().__len__():
# 			return self._list[indexOrName]
# 		elif isinstance(indexOrName, slice):
# 			indices = range(*indexOrName.indices(len(self._list)))
# 			return [self._list[i] for i in indices]
#
# 	@property
# 	def _list(self):
# 		return list(self)
#
# 	def __getattr__(cls, name):
#
# 		if _Meta._is_dunder(name):
# 			raise AttributeError(name)
# 		try:
# 			return cls._member_map_[name]._class_
# 		except KeyError:
# 			raise AttributeError(name) from None
#
#
# class Indexer:
# 	i = 0
# 	lastClass: object = None
#
# 	@classmethod
# 	def get(cls, caller):
# 		cls.i, cls.lastClass = (0, caller) if not caller == cls.lastClass else (cls.i + 1, caller)
# 		return cls.i
#
#
# class ScaleMeta(Enum, metaclass=AddressableEnum):
#
# 	def __new__(cls, *args):
# 		obj = object.__new__(cls)
# 		obj._value_ = Indexer.get(cls)
# 		# obj._class_ = type(obj.name, (Measurement,), {'_unit': args[1]})
# 		obj._mul_ = args[0]
#
# 		return obj
#
# 	def __str__(self):
# 		return str(self.value)
#
# 	# this makes sure that the description is read-only
# 	@property
# 	def index(self):
# 		return self._value_
#
# 	@property
# 	def value(self):
# 		return self._mul_
#
# 	def __repr__(self):
# 		return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, self._mul_)
#
# 	def __mul__(self, other):
# 		if isinstance(other, self.__class__):
# 			val = 1
# 			array = self.__class__[min(self.index, other.index) + 1: max(self.index, other.index) + 1]
# 			array.sort(key=lambda x: x.index)
# 			for i in array:
# 				val *= i.value
# 			return val
#
# 	def __gt__(self, other):
# 		if isinstance(other, self.__class__):
# 			return self.index > other.index
#
# 	def __lt__(self, other):
# 		if isinstance(other, self.__class__):
# 			return self.index < other.index
#
#
# class test(type):
#
# 	def __new__(mcl, name: str, bases, classdict):
# 		cls = type(name, (object,), {'name': 'dog'})
# 		for name, value in classdict.items():
# 			if not name.startswith('_'):
# 				print(name, value)
# 				setattr(cls, name, type(name, (Measurement,), {'_mul_': value[0], '_unit': value[1]}))
#
# 		return cls
#
#



from src.WeatherUnits import time, length, temperature, pressure


def update(value):
	print(f'updated: {value.withUnit}')



# y = pressure.pascal.PoundsPerSquareInch(1)
y = pressure.Atmosphere(1)
y.updateFunction = update
y |= pressure.Pascal(y)
z = pressure.mmHg(y)
t = pressure.psi(z)
print(y.withUnit)
# print(x.withUnit)
print(z.withUnit)
print(t.sizeHint)

d = {1: y, 2: z}
print(d)
d[1] |= t
print(d)
print(d[1])




# d = time.Day(657)
# w = time.Week(d)
# m = time.Month(d)
# print(d.auto)

# c = 0
# v = 1000 * 100000
# print(v)
# while len(str(v)) >= :
# 	c += 1
# 	v //= 1000
# print(v, c)
