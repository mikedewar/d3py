Hello
=====

August 2013

Hello! Maybe you're looking for a nice Python interface to build interactive, javascript based plots that look as nice as all those d3 plots you've been seeing lately? Well, this repository is not a bad place to start looking. The code herein was an experiment to see if this approach was a good idea and, if it was, what the experience of plotting into the browser from Python would feel like. 

All the code should work, more or less, and you are welcome to fork it, muck about with it, and generally get a taste for what this sort of plotting feels like. 

You probably don't want to stop reading here, though. Instead, you should go check out [vincent](https://github.com/wrobstory/vincent) which is a much nicer take on this idea, created using [vega](https://github.com/trifacta/vega), and is in general a much more gentlemanly way to go about this sort of thing. It's also being properly updated and developed, unlike the code below. 

d3py
====

This is `d3py`: a plotting library for python based on d3. The aim of d3py is to provide a simple way to plot data from the command line or simple scripts into a browser window.

d3py accomplishes this by building on two excellent packages. The first is `d3.js` (Mike Bostock), which is a javascript library for creating data driven documents, which allows us to place arbitrary svg into a browser window. The second is the `pandas` Python module (Wes Mckinney), which blesses Python with (amongst other things) the DataFrame data structure.

The idioms used to plot data are very simple, and borrow from R's [ggplot2](http://had.co.nz/ggplot2/) (Hadley Wickham) and Python's [matplotlib](http://matplotlib.sourceforge.net/) (John Hunter et al).

#### Install `d3py` and dependencies:
1. `easy_install https://github.com/mikedewar/d3py/tarball/master`
2. `pip install pandas`
3. `pip install numpy`
4. `pip install networkx`

#### Example:

1. create a `PandasFigure` object around a `DataFrame` (or a NetworkXFigure object around a `Graph`)
2. add `geom`s to the figure object to plot specific combinations of columns of the data frame.
3. show the figure, which serves up the figure in a browser window
4. muck about with the style of the plot using the browser's developer tools
5. share FTW! 

Each geom takes as parameters an appropriate number of column names of the data frame as arguments. For example the `Line` geom, which has two dimensions, takes an x-value and a y-value. A `Point` geom, which makes up a scatter plot, has three dimensions and so takes three parameters: x, y and colour (in the future it could take size, too!).

Each geom is styled using css which you can pass in arbitrarily. So, for example, the `Point` geom comes with a bunch of default styles, but you can also specify `fill=red` as a keyword argument which will add a custom css line for that set of points which will turn them red. This also means you can style the plot live in the browser using Firebug in Firefox or Chrome's developer tools.

d3py aims to create really simple javascript source code wherever possible, so you can go in and edit the plots to embed them into your own sites if needs be. The `.show()` method writes an html file containing the basic markup, a css file with the styles for each geom, a json file with the data from the Figure's DataFrame and a js file with the d3 code in it. The strings that generate the js and css files can always be pulled from the Figure object so you can see how d3py builds up your graph.

An example session could like:

```python
import d3py
import pandas
import numpy as np
	
# some test data
T = 100
# this is a data frame with three columns (we only use 2)
df = pandas.DataFrame({
    "time" : range(T),
    "pressure": np.random.rand(T),
    "temp" : np.random.rand(T)
})
## build up a figure, ggplot2 style
# instantiate the figure object
fig = d3py.PandasFigure(df, name="basic_example", width=300, height=300) 
# add some red points
fig += d3py.geoms.Point(x="pressure", y="temp", fill="red")
# writes 3 files, starts up a server, then draws some beautiful points in Chrome
fig.show() 
```

Check out the examples in the folder for more functionality! Assuming everything is working OK, the examples should generate (something akin to) the following plots:

# point

![point example](http://mikedewar.org/scatter.png)

# line

![line example](http://mikedewar.org/line.png)

# bar

![bar example](http://mikedewar.org/bar.png)

# area

![area example](http://mikedewar.org/area.png)
