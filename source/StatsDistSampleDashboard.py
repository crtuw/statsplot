from matplotlib.pyplot import subplots, show
from .StatsSampleArtist import StatsSampleArtist
from .StatsDistFunArtist import StatsDistFunArtist

class StatsDistSampleDashboard(object):

    def __init__(self,
                 ax = None,
                 statsDistFunArtist = None,
                 statsSampleArtist = None):

        self.ax = ax

        self.statsDistFunArtist = statsDistFunArtist if statsDistFunArtist is not None else StatsDistFunArtist(ax = ax[0] if ax is not None else None)
        self.statsSampleArtist = statsSampleArtist if statsSampleArtist is not None else StatsSampleArtist(ax = ax[1] if ax is not None else None)

    def set_stage(self):
        _, ax = subplots(2,1)
        self.ax = ax
        return ax
        
    def plot_all(self):
        # Check for stage
        ax = self.ax if self.ax is not None else self.set_stage()

        self.statsDistFunArtist.ax = ax[0]
        self.statsSampleArtist.ax = ax[1]
        
        self.statsDistFunArtist.plot_distfun()
        self.statsSampleArtist.plot_sample()