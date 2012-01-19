#!/usr/bin/python


class CSS:
    """
    a CSS object is a dictionary whose keys are CSS selectors and whose values
    are dictionaries of CSS declarations. This object is named according to the
    definition of CSS on wikipedia:
        A style sheet consists of a list of rules.
        Each rule or rule-set consists of one or more selectors and a
        declaration block.
        A declaration-block consists of a list of declarations in braces.
        Each declaration itself consists of a property, a colon (:), a value.
    """
    def __init__(self, css=None):
        self.rules = css or {}
        assert isinstance(self.rules, dict)

    def __getitem__(self, selector):
        "returns the dictionary of CSS declarations, given a selector"
        return self.rules[selector]

    def __setitem__(self, selector, declarations):
        "adds a dictionary of CSS declarations to the specified selector"
        assert isinstance(declarations, dict)
        if selector in self.rules:
            self.rules[selector].update(declarations)
        else:
            self.rules[selector] = declarations

    def __add__(self, css):
        if isinstance(css, dict):
            for selector, declarations in css.iteritems():
                try:
                    self.rules[selector].update(declarations)
                except KeyError:
                    self.rules[selector] = declarations
            return self
        elif isinstance(css, CSS):
            return self.__add__(css.rules)
        else:
            errmsg = "Unsupported addition between %s and %s"
            raise Exception(errmsg % (type(self), type(css)))

    def __str__(self):
        css = ""
        for selector, declarations in self.rules.iteritems():
            css += "%s {\n" % selector
            for prop, value in declarations.iteritems():
                if value is None:
                    value = "none"
                css += "\t%s: %s;\n" % (prop, value)
            css += "}\n\n"
        return css
