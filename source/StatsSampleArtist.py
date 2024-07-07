from matplotlib.pyplot import subplots, fill_between, show
from numpy import ndarray, linspace
from typing import Literal
from seaborn import swarmplot
from scipy.stats import norm

class StatsSampleArtist(object):
    
    def __init__(self,
                 ax = None,
                 sample = None,
                 kwargs_swarmplot: dict = None,
                 label = None):
        '''
        Creates a distribution function artist on a stage.
    
                Parameters:
                        ax                     (obj):      An axes from - see matplotlib.pyplot.axes          
                        sample                 (obj):      A sample
                        kwargs_swarmplot       (dict):     Parameters for plotting the distribution function - see plot_distfun
                        label                  (str):      A label for the sample
        '''
        self.ax = ax
        self.sample = sample if sample is not None else norm().rvs(10)
        self.kwargs_swarmplot = kwargs_swarmplot if kwargs_swarmplot is not None else dict()
        self.label = label if label is not None else "Sample"

    def set_stage(self):
        _, ax = subplots(1,1)
        self.ax = ax
        return ax
        
    def plot_sample(self):
        '''
        Plots a distribution function between a lower and upper percent point
    
                Parameters: <empty on purpose>

                Returns: None
        ''' 
        kwargs_swarmplot = self.kwargs_swarmplot

        ax = self.ax if self.ax is not None else self.set_stage()
        sample = self.sample
        label = self.label

        hue = [label]*len(sample)
        
        swarmplot(ax=ax, x=sample, hue=hue, **kwargs_swarmplot) 
        
    def add_labels(self):
        self.add_xlabel()
        self.add_ylabel()

    def add_xlabel(self):
        ax = self.ax if self.ax is not None else self.set_stage()
        ax.set_xlabel('Random variable')

    def add_ylabel(self):
        ax = self.ax if self.ax is not None else self.set_stage()
        ax.set_ylabel('Jitter')


    def add_legend(self):
        pass