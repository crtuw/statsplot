from matplotlib.pyplot import subplots, fill_between, show
from numpy import ndarray, linspace
from typing import Literal
from seaborn import lineplot
from scipy.stats import norm


DEFAULT_ANNOTATE_LINES = {"color" : "black", "linewidth" : 0.5}
DEFAULT_ANNOTATE_ARROWLABEL = {"xytext" : (1.,2.),                        \
                               "textcoords" : 'offset fontsize',          \
                               "arrowprops" : { "arrowstyle" : "->",      \
                                                "linewidth" : 0.5,        \
                                                "relpos" : (0.5, 0.0) } }
DEFAULT_ANNOTATE_DIMENSIONLINE = { "arrowprops": {"arrowstyle": '<->', "linewidth" : 0.5} }            
DEFAULT_ANNOTATE_DIMENSIONLINE_TEXT = {"xytext" : (0.,0.5), "textcoords" : 'offset fontsize', "ha": 'center'}

class StatsDistFunArtist(object):

    distfunkind_to_ylabel = {"pdf": "Probability density",
                             "cdf": "Lower tail probability"}
    distfunkind_to_label = {"pdf": "PDF",
                            "cdf": "CDF"}
    
    def __init__(self,
                 fig = None,
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
        self.fig = fig
        self.ax = ax
        self.dist = dist if dist is not None else norm()
        self.distfunkind = distfunkind
        
        self.kwargs_distfun2poly  = kwargs_distfun2poly if kwargs_distfun2poly is not None else dict()
        self.kwargs_linestyle = kwargs_linestyle if kwargs_linestyle is not None else dict()
        self.kwargs_fillstyle = kwargs_fillstyle if kwargs_fillstyle is not None else dict()

        self.label = label if label is not None else StatsDistFunArtist.distfunkind_to_label[distfunkind]


    def set_stage(self):
        fig, ax = subplots(1,1)
        self.fig = fig
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
        x, y = self.distfun2poly(**kwargs_distfun2poly)

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

    def annotate_mean(self):
        ax = self.ax if self.ax is not None else self.set_stage()
        mean = self.dist.mean()
        ymean = self.distfun(mean)
        
        ax.vlines(x=mean, ymin=0., ymax=ymean, **DEFAULT_ANNOTATE_LINES)
        an = ax.annotate("Mean", (mean, 0.), **DEFAULT_ANNOTATE_ARROWLABEL)
        
    def annotate_std(self):
        ax = self.ax if self.ax is not None else self.set_stage()
        distfun = self.distfun

        mean = self.dist.mean()
        std = self.dist.std()
        
        xl, xu = (mean - std, mean + std)
        yl, yu = (distfun(x) for x in (xl, xu))
        y = (yl + yu) / 2

        ax.annotate("", xy=(mean - std, y), xytext=(mean, y), **DEFAULT_ANNOTATE_DIMENSIONLINE)
        ax.annotate("", xy=(mean + std, y), xytext=(mean, y), **DEFAULT_ANNOTATE_DIMENSIONLINE)
        ax.annotate("Std. Dev.", xy=(mean - std / 2, y), **DEFAULT_ANNOTATE_DIMENSIONLINE_TEXT)
        ax.annotate("Std. Dev.", xy=(mean + std / 2, y), **DEFAULT_ANNOTATE_DIMENSIONLINE_TEXT)
        
    @property
    def distfun(self):
        dist = self.dist
        distfunkind = self.distfunkind

        if distfunkind == "pdf": distfun = dist.pdf
        if distfunkind == "cdf": distfun = dist.cdf
        
        return distfun
    
    def distfun2poly(self, **kwargs): return _distfun2poly(self.dist, self.distfun, **kwargs)

    def freeze_lims(self, lims):
        ax = self.ax
        ax.set_xlim(lims)
        
    def symmetrize_lims(self):
        ax = self.ax
        lims = ax[0].get_xlim()
        mean = self.statsDistFunArtist.dist.mean()
        
        newlims = get_symmetrized_lims(lims, mean)
                    
        ax.set_xlim(newlims)
            
def _distfun2poly(dist,
                  distfun, 
                  *,
                  ll: float = 0.05, 
                  ul: float = 0.95,
                  lref: Literal["lbtp", "lbvv"] = 'lbtp', 
                  uref: Literal["ubtp", "ubvv"] = 'ubtp') -> [ndarray, ndarray]:
    '''
    Renders a distribution function.
    
        Parameters:
                dist ():            A distribution
                
                distfun ():         Distribution function - see scipy.stats
                                    
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
    y = distfun(x)
    
    return x, y

def get_symmetrized_lims(lims, center):
    dl = max(abs(x-center) for x in lims)
    ll = center - dl
    ul = center + dl
    return [ll, ul]


        