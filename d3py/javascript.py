#!/usr/bin/python

class JavaScript:
    # TODO: Add a lookup function so you can easily find/edit functions/objects
    #       defined within the JavaScript object
    def __init__(self, statements=None):
        self.statements = []
        if statements is not None:
            statements = self._obj_to_statements(statements)
            if isinstance(statements, list):
                self.statements = statements
            else:
                raise Exception("Invalid inputed statement type")

    def get_object(self, name):
        return self.objects_lookup[name]

    def __getitem__(self, item):
        return self.statements[item]

    def __setitem__(self, item, value):
        self.statements[item] = value

    def _obj_to_statements(self, other):
        if isinstance(other, (Function, Object)):
            other = [other, ]
        elif isinstance(other, str):
            other = [other, ]
        elif isinstance(other, JavaScript):
            other = other.statements
        return other

    def __iadd__(self, other):
        other = self._obj_to_statements(other)
        if isinstance(other, list):
            self.statements = self.statements + other
            return self
        raise NotImplementedError


    def __add__(self, other):
        other = self._obj_to_statements(other)
        if isinstance(other, list):
            newobj = JavaScript()
            newobj.statements = self.statements + other
            return newobj
        raise NotImplementedError

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

    def __add__(self, other):
        if isinstance(other, str):
            return self.__str__() + other
        raise NotImplementedError

    def __radd__(self, other):
        return other.__add__( self.__str__() )

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        obj = self.name
        for opt in self.opts:
            if opt["param"] is None:
                param = ""
            elif isinstance(opt["param"], (list, tuple)):
                param = ",".join([str(x) for x in opt["param"]])
            else:
                param = opt["param"]
            obj += ".%s(%s)"%(opt["name"], param)
        return obj

class Function:
    def __init__(self, name, arguments, code):
        self.name = name
        self.arguments = arguments
        if isinstance(code, str):
            code = [code, ]
        self.code = code

    def __add__(self, more_code):
        if isinstance(more_code, str):
            more_code = [more_code, ]
        elif isinstance(more_code, JavaScript):
            more_code = more_code.statements
        if isinstance(more_code, (list, tuple)):
            return Function(self.name, self.arguments, self.code + more_code)
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        fxn = "function"
        if self.name is not None:
            fxn += " %s"%self.name
        fxn += "(%s) {\n"%(",".join(self.arguments))
        for line in self.code:
            fxn += "\t%s\n"%str(line)
        fxn += "}\n"
        return fxn
