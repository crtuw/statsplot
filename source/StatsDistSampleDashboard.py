from matplotlib.pyplot import subplots, show
from .StatsSampleArtist import StatsSampleArtist
from .StatsDistFunArtist import StatsDistFunArtist
import adjustText

class StatsDistSampleDashboard(object):

    def __init__(self,
                 fig = None,
                 ax = None,
                 statsDistFunArtist = None,
                 statsSampleArtist = None):
        self.fig = fig
        self.ax = ax

        self.statsDistFunArtist = statsDistFunArtist if statsDistFunArtist is not None else StatsDistFunArtist(ax = ax[0] if ax is not None else None)
        self.statsSampleArtist = statsSampleArtist if statsSampleArtist is not None else StatsSampleArtist(ax = ax[1] if ax is not None else None)

    def set_stage(self):
        fig, ax = subplots(2,1, sharex=True)
        self.fig = fig
        self.ax = ax
        return ax
        
    def plot_all(self):
        # Check for stage
        ax = self.ax if self.ax is not None else self.set_stage()

        self.statsDistFunArtist.ax = ax[0]
        self.statsSampleArtist.ax = ax[1]
        
        self.statsDistFunArtist.plot_distfun()
        self.statsDistFunArtist.add_labels()
        self.statsDistFunArtist.annotate_mean()
        self.statsDistFunArtist.annotate_std()

        self.statsSampleArtist.plot_sample()
        self.statsSampleArtist.add_labels()

        self.symmetrize_lims()
        
        ax[0].legend(loc="upper right")
        ax[1].legend(loc="upper right")

    def freeze_lims(self, lims):
        ax = self.ax
        for _ax in ax: _ax.set_xlim(lims)
        
    
    def symmetrize_lims(self):
        ax = self.ax
        lims = ax[0].get_xlim()
        mean = self.statsDistFunArtist.dist.mean()
        
        newlims = get_symmetrized_lims(lims, mean)
                    
        for _ax in ax: _ax.set_xlim(newlims)
        
    
def get_symmetrized_lims(lims, center):
    dl = max(abs(x-center) for x in lims)
    ll = center - dl
    ul = center + dl
    return [ll, ul]


        