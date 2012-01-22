import unittest
import css
import pandas
import d3py

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

if __name__ == '__main__':
    unittest.main()