def add_js(self,s):
    """
    adds a line of javascript to the js object. Right now this 
    just deals with newlines, but who knows? Maybe this could
    do pretty indenting one day, too.
    """
    if not (s.startswith("function") or s.startswith("}")):
        self.js += "\t"
    if s.startswith('.'):
        self.js += "\t"
    self.js += s
    self.js += "\n"
