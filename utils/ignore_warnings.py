import warnings

def ignore_warnings():
    warnings.resetwarnings()
    warnings.filterwarnings("ignore")
    # Ignore all DeprecationWarnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Ignore all FutureWarnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    # Ignore all UserWarnings
    warnings.filterwarnings("ignore", category=UserWarning)
    # Ignore all ImportWarnings
    warnings.filterwarnings("ignore", category=ImportWarning)
    # Ignore all RuntimeWarnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)