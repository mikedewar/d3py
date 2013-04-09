'''
Vega
----

A Python to Vega translator. 

'''


class Vega(object): 
    '''Vega abstract base class'''
    
    def __init__(self, name='Vega', width=400, height=200,
                 padding={'top': 10, 'left': 30, 'bottom': 20, 'right': 10},
                 viewport=[]):
        '''
        The Vega classes generate JSON output in Vega grammer, a
        declarative format for creating and saving visualization designs.
        This class is meant to be an abstract base class on which to build
        the other piece of the complete VEGA specification. 
        
        A Vega object is initialized at the top level as a Vega Visualization, 
        with default values for the name, width, height, padding, and viewport.
        
        Parameters:
        -----------
        name: string, default 'Vega'
            Name of the visualization
        width: int, default 800
            Width of the visualization
        height: int, default 400
            Height of the visualization
        padding: dict, default {'T': 10, 'L': 30, 'B': 20, 'R': 10}
            Internal margins for the visualization, Top, Left, Bottom, Right
        viewport: list, default []
            Width and height of on-screen viewport
        '''
        
        self.name = name
        self.width = width
        self.height = height
        self.padding = padding
        self.viewport = viewport
        self.visualization = {'name': self.name, 'width': self.width, 
                              'padding': self.padding, 
                              'viewport': self.viewport}
        self.data = []
        self.scales = []
        self.axes = []
        self.marks = []
        self.vega = {'name': name, 'width': width, 'height': height,
                     'padding': padding, 'viewport': viewport, 
                     'data': self.data, 'scales': self.scales, 
                     'axes':self.axes, 'marks': self.marks}
                     
        
    def update_vega(self, **kwargs):
        '''
        Complete update of Vega object. Replaces all values for top level key.
        
        Examples: 
        >>>object.update_vega(width=500)
        '''

        self.vega.update(kwargs)
        
    def update_data(self, **kwargs, append=False):
        '''
        Update of data component. 
        
        Example: 
        >>>object.update_data(name='table', 
                           
    def to_json(self, path):
        '''
        Save Vega object to JSON
        
        Parameters: 
        -----------
        path: string
            Save path
        '''
        
        pass
        
           
           