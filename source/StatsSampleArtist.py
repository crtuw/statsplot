from matplotlib.pyplot import subplots, fill_between, show
from numpy import ndarray, linspace
from typing import Literal
from seaborn import swarmplot
from scipy.stats import norm

class StatsSampleArtist(object):
    
    def __init__(self,
                 ax = None,
                 sample = None,
                 kwargs_plot_sample: dict = None):
        '''
        Creates a distribution function artist on a stage.
    
                Parameters:
                        ax                     (obj):      An axes from - see matplotlib.pyplot.axes          
                        dist                   (obj):      A parametrized continuos distribution - see scipy.stats
                        distfun                (str):      A reference to a distribution function - see scipy.stats.pdf
                        kwargs_plot_distfun    (dict):     Parameters for plotting the distribution function - see plot_distfun
        '''
        _, self.ax = (None, ax) if ax is not None else subplots()
        self.sample = sample if sample is not None else norm().rvs(10)
        self.kwargs_plot_sample= kwargs_plot_sample if kwargs_plot_sample is not None else dict()

    def plot_sample(self,
                    kwargs_plot_sample:    dict = None):
        '''
        Plots a distribution function between a lower and upper percent point
    
                Parameters:
                        distfun2poly      (Callable): A function that maps the distribution to a polygon - see distfun2poly
                        kwargs_fun2poly   (dict):     Arguments passed on to the fill2poly - see fill2poly
                        kwargs_linestyle  (dict):     Arguments passed on to the lineplot - see seaborn.lineplot
                        kwargs_fillstyle  (dict):     Arguments passed on to the fill_between - see matplotlib.pyplot.fill_between
                        
                Returns:
                        The created plot objects
        ''' 
        kwargs_plot_sample    = kwargs_plot_sample    if kwargs_plot_sample    is not None else dict()

        ax = self.ax
        sample = self.sample

        swarmplot(ax=ax, x=sample)  
