from matplotlib.pyplot import subplots, show
from .StatsSampleArtist import StatsSampleArtist
from .StatsDistFunArtist import StatsDistFunArtist

class StatsDistSampleDashboard(object):

    def __init__(self,
                 ax = None,
                 statsDistFunArtist = None,
                 statsSampleArtist = None):

        _, self.ax = (None, ax) if ax is not None else subplots(2,1)
        self.statsDistFunArtist = statsDistFunArtist if statsDistFunArtist is not None else StatsDistFunArtist(ax = self.ax[0])
        self.statsSampleArtist = statsSampleArtist if statsSampleArtist is not None else StatsSampleArtist(ax = self.ax[1])

    def plot_all(self, kwargs_plot_dist = None,
                       kwargs_plot_sample = None):
        
        kwargs_plot_dist   = kwargs_plot_dist   if kwargs_plot_dist   is not None else dict()
        kwargs_plot_sample = kwargs_plot_sample if kwargs_plot_sample is not None else dict()
        
        self.statsDistFunArtist.plot_distfun()
        self.statsSampleArtist.plot_sample()