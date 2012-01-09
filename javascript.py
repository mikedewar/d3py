#!/usr/bin/python

class JavaScript:
	def __init__(self, statements=None):
		self.statements = statements or []

	def __add__(self, other):
		self.statements.append(other)
		return self

	def __repr__(self):
		return self.__str__()
	
	def __str__(self):
		js = ""
		for statement in self.statements:
			js += str(statement) + "\n"
		return js

class Object:
	def __init__(self, obj, opts):
		self.obj = obj
		self.opts = opts

	def __repr__(self):
		return self.__str__()
	
	def __str__(self):
		obj = self.obj
		for opt in self.opts:
			if opt["param"] is None:
				param = ""
			elif isinstance(opt["param"], list) or isinstance(opt["param"], tuple):
				param = ",".join([str(x) for x in opt["param"]])
			else:
				param = opt["param"]
			obj += ".%s(%s)"%(opt["name"], param)
		return obj

class Function:
	def __init__(self, name, arguments, code):
		assert(isinstance(code, str) or isinstance(code, JavaScript))
		self.name = name
		self.arguments = arguments
		self.code = code

	def __repr__(self):
		return self.__str__()
	
	def __str__(self):
		fxn = "function"
		if self.name is not None:
			fxn += " %s"%self.name
		fxn += "(%s) {\n"%(",".join(self.arguments))
		fxn += str(self.code)
		fxn += "}\n"
		return fxn
