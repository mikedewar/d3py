from ..css import CSS
from ..javascript import JavaScript, Selection, Function

class Geom:
    def __init__(self, **kwargs):
        self.styles = kwargs
        self.js = JavaScript()
        self.css = CSS()
    
    def _build_js(self):
        raise NotImplementedError
    
    def _build_css(self):
        raise NotImplementedError
