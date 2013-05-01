  # -*- coding: utf-8 -*-
'''
Figure Test
-------

Test figure object with nose package:
https://nose.readthedocs.org/en/latest/

'''

import d3py
import nose.tools as nt


class TestFigure():

    def setup(self):
        '''Setup Figure object for testing'''

        self.Figure = d3py.Figure('test figure', 1024, 768, True, 'Asap',
                                  False, None, 'localhost', 8000,
                                  kwarg='test')

    def test_atts(self):
        '''Test attribute setting'''

        assert self.Figure.name == 'test_figure'
        assert self.Figure.host == 'localhost'
        assert self.Figure.port == 8000
        assert self.Figure._server_thread == None
        assert self.Figure.httpd == None
        assert self.Figure.interactive == True
        assert self.Figure.margins == {'bottom': 25, 'height': 768, 'left': 60,
                                       'right': 20, 'top': 10, 'width': 1024}
        assert self.Figure.font == 'Asap'
        assert self.Figure.args == {'font-family': "'Asap'; sans-serif",
                                    'height': 733, 'width': 944,
                                    'kwarg': 'test'}
