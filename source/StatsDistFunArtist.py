from matplotlib.pyplot import subplots, fill_between, show
from numpy import ndarray, linspace
from typing import Literal
from seaborn import lineplot
from scipy.stats import norm

class StatsDistFunArtist(object):


    distfunkind_to_ylabel = {"pdf": "Probability density",
                             "cdf": "Lower tail probability"}
    distfunkind_to_label = {"pdf": "Probability density function",
                            "cdf": "Cumulative distribution function"}
    
    def __init__(self,
                 ax = None,
                 dist = None,
                 distfunkind: Literal["pdf","cdf"] = "pdf",
                 kwargs_distfun2poly: dict = None,
                 kwargs_linestyle: dict = None,
                 kwargs_fillstyle: dict = None,
                 label = None):
        '''
        Creates a distribution function artist on a stage.
    
                Parameters:
                        ax                (obj):      An axes from - see matplotlib.pyplot.axes          
                        dist              (obj):      A parametrized continuos distribution - see scipy.stats
                        distfun           (str):      A reference to a distribution function - see scipy.stats.pdf
                        kwargs_fun2poly   (dict):     Arguments passed on to the fill2poly - see fill2poly
                        kwargs_linestyle  (dict):     Arguments passed on to the lineplot - see seaborn.lineplot
                        kwargs_fillstyle  (dict):     Arguments passed on to the fill_between - see matplotlib.pyplot.fill_between
        '''
        self.ax = ax
        self.dist = dist if dist is not None else norm()
        self.distfunkind = distfunkind
        
        self.kwargs_distfun2poly  = kwargs_distfun2poly  if kwargs_distfun2poly  is not None else dict()
        self.kwargs_linestyle = kwargs_linestyle if kwargs_linestyle is not None else dict()
        self.kwargs_fillstyle = kwargs_fillstyle if kwargs_fillstyle is not None else dict()

        self.label = label if label is not None else StatsDistFunArtist.distfunkind_to_label[distfunkind]


    def set_stage(self):
        _, ax = subplots(1,1)
        self.ax = ax
        return ax
    
    def plot_distfun(self):
        '''
        Plots a distribution function between a lower and upper percent point
    
                Parameters:
                        
                Returns:
                        The created plot objects
        ''' 
        # Get parameters from instance       
        ax = self.ax if self.ax is not None else self.set_stage()
        
        dist = self.dist
        distfunkind = self.distfunkind
        
        kwargs_distfun2poly = self.kwargs_distfun2poly
        kwargs_linestyle    = self.kwargs_linestyle        
        kwargs_fillstyle    = self.kwargs_fillstyle        

        label = self.label
        
        # Calculate the polygon
        x, y = StatsDistFunArtist.distfun2poly(dist, distfunkind, **kwargs_distfun2poly)

        # Plot
        lineplot(ax=ax, x=x, y=y, **kwargs_linestyle, label=label)
        ax.fill_between(x=x, y1=y, **kwargs_fillstyle)  

    def add_labels(self):
        self.add_xlabel()
        self.add_ylabel()

    def add_xlabel(self):
        ax = self.ax if self.ax is not None else self.set_stage()
        ax.set_xlabel('Random variable')

    def add_ylabel(self):
        ax = self.ax if self.ax is not None else self.set_stage()
        distfunkind = self.distfunkind
        ax.set_ylabel(StatsDistFunArtist.distfunkind_to_ylabel[distfunkind])
    
    @staticmethod
    def distfun2poly(dist,
                     distfunkind: Literal["pdf","cdf"] = 'pdf', 
                     *,
                     ll: float = 0.05, 
                     ul: float = 0.95,
                     lref: Literal["lbtp", "lbvv"] = 'lbtp', 
                     uref: Literal["ubtp", "ubvv"] = 'ubtp') -> [ndarray, ndarray]:
        '''
        Renders a distribution function.
        
            Parameters:
                    dist ():            A distribution
                    
                    distfunkind (str):  Distribution function chosen from 
                                             "pdf": The probability distribution function
                                             "cdf": The cumulative distribution function
                                        
                    ll (float):         Lower limit (default = 0.05)
                        
                    ul (float):         Upper limit (default = 0.95)
                        
                    lref:               Lower reference (default = 'lbtp')
                                              "lbtp": Lower bound from tail probability
                                              "lbvv": Lower bound from (random) variable value
                                              
                    uref:               Upper reference (default = 'ubtp')
                                              "ubtp": Upper bound from tail probability
                                              "ubvv": Upper bound from (random) variable value
                                          
            Returns:
                    x, y
        '''
    
        xll = dist.ppf(ll) if lref == "lbtp" else ll
        xul = dist.ppf(ul) if uref == "ubtp" else ul
    
        x = linspace(xll,xul,100)

        if distfunkind == "pdf": distfun = dist.pdf
        if distfunkind == "cdf": distfun = dist.cdf
                
        y = distfun(x)
        return x, y