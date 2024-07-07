from .StatsDistSampleDashboard import StatsDistSampleDashboard
from .StatsDistFunArtist import StatsDistFunArtist
from .StatsSampleArtist import StatsSampleArtist
from scipy.stats import norm

def create_dist_sample_dashboard(loc:str, scale:str, n:str, dlim:str="", ctp:str=""):

    loc = float(loc)
    scale = float(scale)
    n = int(n)

    # Optional parameters:
    dlim = abs(float(dlim)) if dlim != "" else None
    ctp = abs(float(ctp)) if ctp != "" else None
    dtp = (1-ctp) / 2 if ctp is not None else None
    
    # Set distribution limits if provided
    kwargs_distfun2poly = dict(ll = dtp, ul = 1 - dtp, lref = "lbtp", uref = "ubtp") if ctp is not None else dict()

    # Set up distribution & sample
    dist = norm(loc=float(loc), scale=float(scale))
    sample = dist.rvs(int(n))

    # Set up distribution artist
    statsDistFunArtist = StatsDistFunArtist(dist = dist, 
                                            kwargs_distfun2poly = kwargs_distfun2poly,
                                            kwargs_fillstyle = dict(color="lightgrey"))

    # Set up sample artist    
    statsSampleArtist = StatsSampleArtist(sample = sample)

    # Set up dashboard
    statsDistSampleDashboard = StatsDistSampleDashboard(statsSampleArtist=statsSampleArtist, 
                                                        statsDistFunArtist=statsDistFunArtist)
    statsDistSampleDashboard.plot_all()

    # Set plot horizon
    if dlim is not None:
        statsDistSampleDashboard.freeze_lims([loc-dlim, loc+dlim]) 
    else:
        statsDistSampleDashboard.symmetrize_lims()
    
    return statsDistSampleDashboard

def create_distfun_dashboard(loc:str, scale:str, dlim:str="", ctp:str=""):

    loc = float(loc)
    scale = float(scale)

    # Optional parameters:
    dlim = abs(float(dlim)) if dlim != "" else None
    ctp = abs(float(ctp)) if ctp != "" else None
    dtp = (1-ctp) / 2 if ctp is not None else None
    
    # Set distribution limits if provided
    kwargs_distfun2poly = dict(ll = dtp, ul = 1 - dtp, lref = "lbtp", uref = "ubtp") if ctp is not None else dict()

    # Set up distribution & sample
    dist = norm(loc=float(loc), scale=float(scale))

    # Set up distribution artist
    statsDistFunArtist = StatsDistFunArtist(dist = dist, 
                                            kwargs_distfun2poly = kwargs_distfun2poly,
                                            kwargs_fillstyle = dict(color="lightgrey"))
    statsDistFunArtist.plot_distfun()
    statsDistFunArtist.add_labels()
    statsDistFunArtist.annotate_mean()
    statsDistFunArtist.annotate_std()

    # Set plot horizon
    if dlim is not None:
        statsDistFunArtist.freeze_lims([loc-dlim, loc+dlim]) 
    else:
        statsDistFunArtist.symmetrize_lims()
    
    return statsDistFunArtist