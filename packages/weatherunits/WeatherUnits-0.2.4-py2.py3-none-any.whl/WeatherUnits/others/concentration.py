from .. import Measurement as _Measurement, NamedType


@NamedType
class Humidity(_Measurement):
	_format = "{:2d}"
	_unit = ''
	_decorator = '%'
