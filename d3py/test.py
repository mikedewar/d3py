import unittest
import css
import pandas
import d3py
import javascript


class TestCSS(unittest.TestCase):
    
    def setUp(self):
        self.css = css.CSS()
    
    def test_init(self):
        out = css.CSS({"#test":{"fill":"red"}})
        self.assertTrue(out["#test"] == {"fill":"red"})
    
    def test_get(self):
        self.css["#test"] = {"fill":"red"}
        self.assertTrue(self.css["#test"] == {"fill":"red"})
    
    def test_set(self):
        self.css["#test"] = {"fill":"red"}
        self.css["#test"] = {"stroke":"black"}
        self.assertTrue(self.css["#test"] == {"fill":"red", "stroke":"black"})
    
    def test_add(self):
        a = css.CSS()
        b = css.CSS()
        a["#foo"] = {"fill":"red"}
        a["#bar"] = {"fill":"blue"}
        b["#foo"] = {"stroke":"green"}
        b["#bear"] = {"fill":"yellow"}
        out = a + b
        expected = css.CSS({
            "#foo":{
                "fill":"red", 
                "stroke":"green"
            },
            "#bar" : {"fill":"blue"},
            "#bear" : {"fill":"yellow"}
        })
        self.assertTrue(out.rules == expected.rules)
    
    def test_str(self):
        self.css["#test"] = {"fill":"red"}
        out = str(self.css)
        self.assertTrue(out == "#test {\n\tfill: red;\n}\n\n")

class Test_d3py(unittest.TestCase):
    def setUp(self):
        self.df = pandas.DataFrame({
            "count": [1,2,3],
            "time": [1326825168, 1326825169, 1326825170]
        })
        
    def test_data_to_json(self):
        p = d3py.Figure(self.df)
        j = p.data_to_json()

class Test_JavaScript_object_lookup(unittest.TestCase):
    def setUp(self):
        self.g = javascript.Object("g").attr("color", "red")
        self.j = javascript.JavaScript() + self.g
        self.f = javascript.Function("test", None, "return 5")
    
    def test_getobject(self):
        self.assertTrue(self.j.get_object("g", javascript.Object) == self.g)

    def test_inplace_mod(self):
        self.g.attr("test", "test")
        self.assertTrue(self.j.get_object("g", javascript.Object) == self.g)

    def test_add_fucntion(self):
        self.j += self.f
        self.assertTrue(self.j.get_object("test", javascript.Function) == self.f)

    def test_prepend_function(self):
        self.j += self.f
        self.f = "console.debug('hello')" + self.f
        self.assertTrue(self.j.get_object("test", javascript.Function) == self.f)

if __name__ == '__main__':
    unittest.main()