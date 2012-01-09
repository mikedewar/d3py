#!/usr/bin/python

class CSS:
	def __init__(self):
		self.objects = {}

	def __getitem__(self, item):
		return self.objects[item]

	def __setitem__(self, item, value):
		assert(isinstance(value, dict))
		if item in self.objects:
			self.objects[item].update(value)
		else:
			self.objects[item] = value

	def __add__(self, item):
		if isinstance(item, dict):
			for value in item.itervalues():
				assert(isinstance(item, dict))
				self.objects.update(item)
			return self
		elif isinstance(item, CSS):
			return self.__add__(item.objects)
		else:
			raise Exception("Unsupported addition between %s and %s"%(type(CSS), type(item)))

	def __str__(self):
		css = ""
		for key, props in self.objects.iteritems():
			css += "%s {\n"%key
			for prop, value in props.iteritems():
				if value is None:
					value = "none"
				css += "\t%s: %s;\n"%(prop, value)
			css += "}\n\n"
		return css
