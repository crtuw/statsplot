from .StatsDistSampleDashboard import StatsDistSampleDashboard
from .StatsDistFunArtist import StatsDistFunArtist
from .StatsSampleArtist import StatsSampleArtist
from scipy.stats import norm


def create_dist_sample_dashboard(loc:str, scale:str, n:str, dlim:str, ctp:str):

    loc = float(loc)
    scale = float(scale)
    n = int(n)
    dlim = abs(float(dlim))
    ctp = abs(float(ctp))
    dtp = (1-ctp) / 2

    # Set up distribution & sample
    dist = norm(loc=float(loc), scale=float(scale))
    sample = dist.rvs(int(n))
    
    # Tolerances
    TOL_ctp_min = 1.e-3
    TOL_ctp_max = 1. - TOL_ctp_min
    TOL_dlim = scale / 1000.

    # Set up distribution artist
    kwargs_distfun2poly = dict(ll = dtp, ul = 1-dtp, lref = "lbtp", uref = "ubtp") if ctp > TOL_ctp_min and ctp < TOL_ctp_max else dict()
    statsDistFunArtist = StatsDistFunArtist(dist = dist, 
                                            kwargs_distfun2poly = kwargs_distfun2poly,
                                            kwargs_fillstyle = dict(color="lightgrey"))

    # Set up sample artist    
    statsSampleArtist = StatsSampleArtist(sample = sample)

    # Set up dashboard
    
    statsDistSampleDashboard = StatsDistSampleDashboard(statsSampleArtist=statsSampleArtist, 
                                                        statsDistFunArtist=statsDistFunArtist)
    statsDistSampleDashboard.plot_all()

    # Adapt limits (center or freeze & center)
    if dlim > TOL_dlim:
        statsDistSampleDashboard.freeze_lims([loc-dlim, loc+dlim]) 
    else: 
        statsDistSampleDashboard.symmetrize_lims()
    
    return statsDistSampleDashboard