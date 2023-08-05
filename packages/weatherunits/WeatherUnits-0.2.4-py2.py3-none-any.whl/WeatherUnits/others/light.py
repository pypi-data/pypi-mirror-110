from .. import Measurement, NamedType


@NamedType
class Light(Measurement):
	pass

@NamedType
class UVI(Light):
	_format = "{:1d}"


@NamedType
class Irradiance(Light):
	_format = "{:4d}"
	_unit = 'W/m²'


@NamedType
class Illuminance(Light):
	_format = "{:4d}"
	_unit = 'lux'

	def __new__(cls, value):
		if value > 1000:
			cls._format = '{2:1f}'
			cls._decorator = 'k'
			value /= 1000
		return float.__new__(cls, value)

	def __init__(self, value):
		float.__init__(value)


RadiantFlux = Irradiance
Lux = Illuminance
