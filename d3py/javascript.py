#!/usr/bin/python

class JavaScript:
    # TODO: Add a lookup function so you can easily find/edit functions/objects
    #       defined within the JavaScript object
    def __init__(self, statements=None):
        self.statements = []
        self.objects_lookup = {}
        if statements is not None:
            statements = self._obj_to_statements(statements)
            if isinstance(statements, list):
                self.statements = statements
                self.objects_lookup = self.parse_objects()
            else:
                raise Exception("Invalid inputed statement type")

    def merge(self, other):
        for line in other.statements:
            if hasattr(line, "name") and (line.name, type(line.__class__)) in self.objects_lookup:
                idx = self.objects_lookup[(line.name, type(line.__class__))][1]
                self.statements[idx] += line
            else:
                self.statements.append(line)
        self.objects_lookup = self.parse_objects()

    def get_object(self, name, objtype):
        return self.objects_lookup[(name,type(objtype))][0]

    def __getitem__(self, item):
        return self.statements[item]

    def __setitem__(self, item, value):
        self.statements[item] = value

    def parse_objects(self):
        objects = {}
        for i, item in enumerate(self.statements):
            if hasattr(item, "name") and item.name:
                # Is it necissary to compound the key with the class type?
                objects[ (item.name, type(item.__class__)) ] = (item, i)
        return objects

    def _obj_to_statements(self, other):
        if isinstance(other, (Function, Object)):
            other = [other, ]
        elif isinstance(other, str):
            other = [other, ]
        elif isinstance(other, JavaScript):
            other = other.statements
        return other

    def __radd__(self, other):
        other = self._obj_to_statements(other)
        if isinstance(other, list):
            return JavaScript(self.statements + other)
        raise NotImplementedError


    def __add__(self, other):
        other = self._obj_to_statements(other)
        if isinstance(other, list):
            newobj = JavaScript()
            newobj.statements = self.statements + other
            newobj.objects_lookup = newobj.parse_objects()
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
    
    # TODO maybe add_attribute should be add_method instead?
    
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
        # TODO what's this one for then?
        return self.add_attribute("id", *args)
    def call(self, *args):
        return self.add_attribute("call", *args)

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
    def __init__(self, name=None, arguments=None, statements=None, autocall=False):
        """
        name: string
        
        arguments: list of strings
        
        statements: list of strings
        
        This ends up as 
        
        function name(arg1, arg2, arg3){
            statement1;
            statement2;
            statement3;
        }
        
        """
        self.name = name
        self.arguments = arguments
        if isinstance(statements, str):
            statements = [statements, ]
        self.statements = statements or []
        self.autocall = autocall

    def _obj_to_statements(self, other):
        if isinstance(other, str):
            other = [other, ]
        elif isinstance(other, JavaScript):
            other = other.statements
        elif isinstance(other, Function) and other.name == self.name and other.arguments == self.arguments:
            other = other.statements
        elif isinstance(other, Object):
            other = [other, ]
        else:
            other = None
        return other

    def __add__(self, more_statements):
        more_statements = self._obj_to_statements(more_statements)
        if isinstance(more_statements, (list, tuple)):
            return Function(self.name, self.arguments, self.statements + more_statements, self.autocall)
        raise NotImplementedError

    def __radd__(self, more_statements):
        more_statements = self._obj_to_statements(more_statements)
        if isinstance(more_statements, (list, tuple)):
            return Function(self.name, self.arguments, more_statements + self.statements, self.autocall)
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        fxn = "function"
        if self.name is not None:
            fxn += " %s"%self.name
        fxn += "(%s) {\n"%(",".join(self.arguments or ""))
        for line in self.statements:
            fxn += "\t%s\n"%str(line)
        fxn += "}\n"
        if self.autocall:
            fxn += "%s(%s);\n"%(self.name, ",".join(self.arguments or ""))
        return fxn
