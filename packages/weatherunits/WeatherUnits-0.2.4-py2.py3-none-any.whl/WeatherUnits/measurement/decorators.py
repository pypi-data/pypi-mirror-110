def NamedType(cls):
	cls._type = cls
	return cls


def NamedSubType(cls):
	cls._subType = cls
	return cls


def UnitSystem(cls):
	cls._unitSystem = cls
	return cls


def BaseUnit(cls):
	cls._unitSystem._baseUnit = cls
	return cls
