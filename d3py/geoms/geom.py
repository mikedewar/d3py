from ..css import CSS
from ..javascript import JavaScript, Object, Function

class Geom:
    def __init__(self, **kwargs):
        self.styles = kwargs
        self.js = JavaScript()
        self.css = CSS()
    
    def build_js(self):
        raise NotImplementedError
    
    def build_css(self):
        raise NotImplementedError
