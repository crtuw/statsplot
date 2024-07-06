from matplotlib.pyplot import subplots, fill_between, show
from numpy import ndarray, linspace
from typing import Literal
from seaborn import lineplot
from scipy.stats import norm

class StatsDistFunArtist(object):
    
    def __init__(self,
                 ax = None,
                 dist = None,
                 distfun: Literal["pdf","cdf"] = "pdf",
                 kwargs_distfun2poly: dict = None,
                 kwargs_linestyle: dict = None,
                 kwargs_fillstyle: dict = None):
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
        _, self.ax = (None, ax) if ax is not None else subplots()
        self.dist = dist if dist is not None else norm()
        self.distfun = distfun
        
        self.kwargs_fun2poly  = kwargs_fun2poly  if kwargs_fun2poly  is not None else dict()
        self.kwargs_linestyle = kwargs_linestyle if kwargs_linestyle is not None else dict()
        self.kwargs_fillstyle = kwargs_fillstyle if kwargs_fillstyle is not None else dict()

    def plot_distfun(self,
                     distfun2poly = None,
                     kwargs_distfun2poly: dict = None,
                     kwargs_linestyle:    dict = None,
                     kwargs_fillstyle:    dict = None):
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
        # Process passed parameters
        _distfun2poly = distfun2poly if distfun2poly is not None \
                                     else StatsDistFunArtist.distfun2poly

        kwargs_distfun2poly = kwargs_distfun2poly if kwargs_distfun2poly is not None else dict()
        kwargs_linestyle = kwargs_linestyle if kwargs_linestyle is not None else dict()
        kwargs_fillstyle = kwargs_fillstyle if kwargs_fillstyle is not None else dict()
        
        # Get parameters from object       
        _ax = self.ax
        _dist = self.dist
        _distfun = self.distfun
        _kwargs_distfun2poly = self.kwargs_distfun2poly
        _kwargs_linestyle = self.kwargs_linestyle        
        _kwargs_fillstyle = self.kwargs_fillstyle        

        # Update with passed parameters
        _kwargs_distfun2poly.update(kwargs_distfun2poly)
        _kwargs_linestyle.update(kwargs_linestyle)
        _kwargs_fillstyle.update(kwargs_fillstyle)

        # Calculate the polygon
        _x, _y = distfun2poly(_dist, _distfun, **_kwargs_distfun2poly)

        # Plot
        lineplot(ax=ax, x=_x, y=_y, **_kwargs_linestyle)
        ax.fill_between(x=_x, y1=y, **_kwargs_fillstyle)  

    @staticmethod
    def distfun2poly(dist,
                     distfun: Literal["pdf","cdf"] = 'pdf', 
                     *,
                     ll: float = 0.05, 
                     ul: float = 0.95,
                     lref: Literal["lbtp", "lbvv"] = 'lbtp', 
                     uref: Literal["ubtp", "ubvv"] = 'ubtp') -> [ndarray, ndarray]:
        '''
        Renders a distribution function.
        
            Parameters:
                    dist ():        A distribution
                    
                    distfun (str):  Distribution function chosen from 
                                        "pdf": The probability distribution function
                                        "cdf": The cumulative distribution function
                                        
                    ll (float):     Lower limit (default = 0.05)
                    
                    ul (float):     Upper limit (default = 0.95)
                    
                    lref:           Lower reference (default = 'lbtp')
                                          "lbtp": Lower bound from tail probability
                                          "lbvv": Lower bound from (random) variable value
                                          
                    uref:           Upper reference (default = 'ubtp')
                                          "ubtp": Upper bound from tail probability
                                          "ubvv": Upper bound from (random) variable value
                                          
            Returns:
                    x, y
        '''
    
        xll = dist.ppf(ll) if lref == "lbtp" else ll
        xul = dist.ppf(ul) if uref == "ubtp" else ul
    
        x = linspace(xll,xul,100)

        match distfun:
            case "pdf":
                distfun = dist.pdf
            case "cdf":
                distfun = dist.cdf
                
        y = distfun(x)
        return x, y