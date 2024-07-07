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
        _, ax = subplots(2,1, sharex=True)
        self.ax = ax
        return ax
        
    def plot_all(self):
        # Check for stage
        ax = self.ax if self.ax is not None else self.set_stage()

        self.statsDistFunArtist.ax = ax[0]
        self.statsSampleArtist.ax = ax[1]
        
        self.statsDistFunArtist.plot_distfun()
        self.statsDistFunArtist.add_labels()

        self.statsSampleArtist.plot_sample()
        self.statsDistFunArtist.add_labels()

        self.symmetrize_lims()

    def freeze_lims(self, lims):
        ax = self.ax
        for _ax in ax: _ax.set_xlim(lims)
        
    
    def symmetrize_lims(self):
        ax = self.ax
        lims = ax[0].get_xlim()
        mean = self.statsDistFunArtist.dist.mean()
        
        newlims = StatsDistSampleDashboard.get_symmetrized_lims(lims, mean)
                    
        for _ax in ax: _ax.set_xlim(newlims)
        
    
    @staticmethod
    def get_symmetrized_lims(lims, center):
        dl = max(abs(x-center) for x in lims)
        ll = center - dl
        ul = center + dl
        return [ll, ul]


        