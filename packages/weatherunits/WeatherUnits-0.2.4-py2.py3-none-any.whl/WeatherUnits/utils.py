from enum import Enum as _Enum, EnumMeta as _Meta


class AddressableEnum(_Meta):

	def __getitem__(self, indexOrName):
		if isinstance(indexOrName, str):
			return super().__getitem__(indexOrName)
		elif isinstance(indexOrName, int) and indexOrName < super().__len__():
			return self._list[indexOrName]
		elif isinstance(indexOrName, slice):
			indices = range(*indexOrName.indices(len(self._list)))
			return [self._list[i] for i in indices]

	@property
	def _list(self):
		return list(self)


class Indexer:
	i = 0
	lastClass: object = None

	@classmethod
	def get(cls, caller):
		cls.i, cls.lastClass = (0, caller) if not caller == cls.lastClass else (cls.i + 1, caller)
		return cls.i


class ScaleMeta(_Enum, metaclass=AddressableEnum):

	def __new__(cls, *args):
		obj = object.__new__(cls)
		obj._value_ = Indexer.get(cls)
		obj._mul_ = args[0]
		return obj

	def __str__(self):
		return str(self.value)

	# this makes sure that the description is read-only
	@property
	def index(self):
		return self._value_

	@property
	def value(self):
		return self._mul_

	def __repr__(self):
		return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, self._mul_)

	def __mul__(self, other):
		if isinstance(other, self.__class__):
			val = 1
			array = self.__class__[min(self.index, other.index) + 1: max(self.index, other.index) + 1]
			array.sort(key=lambda x: x.index)
			for i in array:
				val *= i.value
			return val

	def __gt__(self, other):
		if isinstance(other, self.__class__):
			return self.index > other.index
		else:
			return self.index > int(other)

	def __lt__(self, other):
		if isinstance(other, self.__class__):
			return self.index < other.index
		else:
			return self.index < int(other)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.index == other.index
		else:
			return self.index == int(other)

	def __le__(self, other):
		if isinstance(other, self.__class__):
			return self.index <= other.index
		else:
			return self.index <= int(other)

	def __ge__(self, other):
		if isinstance(other, self.__class__):
			return self.index >= other.index
		else:
			return self.index >= int(other)


'''https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python'''


def levenshtein(seq1, seq2):
	oneago = None
	thisrow = range(1, len(seq2) + 1) + [0]
	for x in range(len(seq1)):
		twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
		for y in range(len(seq2)):
			delcost = oneago[y] + 1
			addcost = thisrow[y - 1] + 1
			subcost = oneago[y - 1] + (seq1[x] != seq2[y])
			thisrow[y] = min(delcost, addcost, subcost)
	return thisrow[len(seq2) - 1]
