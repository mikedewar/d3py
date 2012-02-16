#!/usr/bin/python

from d3py import javascript as JS

def test_JavaScript_object_lookup():
    g = JS.Object("g").attr("color", "red")
    j = JS.JavaScript() + g

    assert(j.get_object("g", JS.Object) == g)

    g.attr("test", "test")
    assert(j.get_object("g", JS.Object) == g)

    f = JS.Function("test", None, "return 5")
    j += f

    assert(j.get_object("test", JS.Function) == f)

    f = "console.debug('hello')" + f
    assert(j.get_object("test", JS.Function) == f)

if __name__ == "__main__":
    test_JavaScript_object_lookup()


