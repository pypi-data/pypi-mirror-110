from abc import ABC
from unittest import mock

class Injectable(ABC):
	"""Base class for every class to be injected

	The framework minidi relies on objects to handle injections.
	This class is simply an interface other classes should derive from,
	so minidi can detect those classes correctly.

	Three very basic rules an Injectable has to follow:
	1. it must be a stateless class, so it should NOT hold any data or constants,
	2. it must have a default constructor,
	3. if you want to use other Injectables, they have to be type-defined like
	
	class GeneralCache(Injectable):
		cacheValidator: CacheValidator
		garbageCollector: GarbageCollector

		[...] # additional code
	
	You can think of Injectables as non-static Singletons,
	so they can be exchanged at any time if needed.
	"""

	def __setattr__(self, name: str, value):
		if not isinstance(value, (Injectable, mock.Base)):
			raise TypeError(f"Cannot add non-Injectable or mock as member to an Injectable!")
		
		super().__setattr__(name, value)
	# def __setattr__(self, name: str, value)
# class Injectable


_injectableInstances = {}


def _fillDependencies(injectableInstance: Injectable) -> Injectable:
	annotations = injectableInstance.__annotations__.items()
	for subInjectableName, subInjectableType in annotations:
		exec(f'injectableInstance.{subInjectableName} = get(subInjectableType)')
	
	return injectableInstance
# def _fillDependencies(injectableInstance: Injectable) -> Injectable


def get(cls) -> Injectable:
	"""Get the specified instance of an Injectable class.

	The heart of minidi.
	This function will return and eventually create the Injectable classes you requested.
	All additional Injectable members will be also created through this function.
	"""
	if not issubclass(cls, Injectable):
		raise ValueError(f"Argument passed '{cls}' has to be a sub class of Injectable!")
	
	clsName = f'{cls.__module__}.{cls.__qualname__}'

	if clsName not in _injectableInstances:
		try:
			injectableInstance = cls()
		except:
			raise ValueError(f"Injectable '{cls}' does not have a default constructor!")
		
		_injectableInstances[clsName] = injectableInstance

		if hasattr(injectableInstance, '__annotations__'):
			try:
				injectableInstance = _fillDependencies(injectableInstance)
			except ValueError:
				del _injectableInstances[clsName]
				raise ValueError(f"Members of argument passed '{cls}' have to be of type Injectable!")
		# if hasattr(injectableInstance, '__annotations__')
	# if clsName not in _injectableInstances

	return _injectableInstances[clsName]
# def get(cls) -> Injectable