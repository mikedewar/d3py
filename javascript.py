#!/usr/bin/python

class JavaScript:
    def __init__(self, statements=None):
        self.statements = statements or []

    def __getitem__(self, item):
        return self.statements[item]

    def __setitem__(self, item, value):
        self.statements[item] = value

    def __add__(self, other):
        if isinstance(other, str):
            other = [other, ]
        elif isinstance(other, JavaScript):
            other = other.statements
        return JavaScript(self.statements + other)

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        js = ""
        for statement in self.statements:
            js += str(statement) + "\n"
        return js

class Object:
    def __init__(self, name):
        self.name = name
        self.opts = []

    def add_attribute(self, name, *args):
        self.opts.append({"name":name, "param":",".join(str(x) for x in args)})
        return self

    def select(self, *args): 
        return self.add_attribute("select", *args)
    def selectAll(self, *args): 
        return self.add_attribute("selectAll", *args)
    def data(self, *args): 
        return self.add_attribute("data", *args)
    def enter(self, *args): 
        return self.add_attribute("enter", *args)
    def append(self, *args): 
        return self.add_attribute("append", *args)
    def attr(self, *args): 
        return self.add_attribute("attr", *args)
    def id(self, *args): 
        return self.add_attribute("id", *args)

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        obj = self.name
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
        if isinstance(code, str):
            code = [code, ]
        self.code = code

    def __add__(self, more_code):
        if isinstance(more_code, JavaScript):
            return Function(self.name, self.arguments, self.code + more_code.statements)
        elif isinstance(more_code, Function):
            return Function(self.name, self.arguments, self.code + more_code.code)

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        fxn = "function"
        if self.name is not None:
            fxn += " %s"%self.name
        fxn += "(%s) {\n"%(",".join(self.arguments))
        for line in self.code:
            fxn += str(line) + "\n"
        fxn += "}\n"
        return fxn
