

from .timeserie import TSTransient
from .collection import CompositeTransient

# https://sncosmo.readthedocs.io/en/stable/source-list.html

class SNeII( CompositeTransient ):
    
    _COLLECTION_OF = TSTransient

    _KIND = "SNII"
    # Vincenzi et al. 2019 from sncosmo.
    _TEMPLATES = ["v19-asassn14jb-corr","v19-asassn15oz-corr", "v19-1987a-corr",
                  "v19-1999em-corr","v19-2004et-corr","v19-2007od-corr",
                  "v19-2008bj-corr","v19-2008in-corr","v19-2009n-corr",
                  "v19-2009bw-corr","v19-2009dd-corr", "v19-2009ib-corr",
                  "v19-2009kr-corr", "v19-2012a-corr", "v19-2012aw-corr",
                  "v19-2013ab-corr", "v19-2013am-corr", "v19-2013by-corr",
                  "v19-2013ej-corr", "v19-2013fs-corr", "v19-2014g-corr",
                    "v19-2016x-corr", "v19-2016bkv-corr"]
        
    _RATE = 5.4e4 # (Perley 2020) CC 1e5 * (0.75 *0.72) for Type II. ; this is wrong but close.
    _MAGABS = (-17.7, 0.92) # Bright Transient Survey statistics (Perley 2020)
    
class SNeIIn( CompositeTransient ):
    
    _COLLECTION_OF = TSTransient

    _KIND = "SNIIn"
    # Vincenzi et al. 2019 from sncosmo.
    _TEMPLATES = ["v19-2006aa-corr", "v19-2007pk-corr", "v19-2008fq-corr",
                  "v19-2009ip-corr", "v19-2010al-corr", "v19-2011ht-corr"]
        
    _RATE = 5.4e4 # Perley CC 1e5 * (0.75 *0.72) for Type II.

class SNeIIb( CompositeTransient ):
    
    _COLLECTION_OF = TSTransient

    _KIND = "SNIIn"
    # Vincenzi et al. 2019 from sncosmo.
    _TEMPLATES = ["v19-1993j-corr", "v19-1999dn-corr", "v19-2006t-corr",
                  "v19-2008aq-corr", "v19-2008ax-corr", "v19-2008bo-corr",
                  "v19-2011dh-corr", "v19-2011ei-corr", "v19-2011fu-corr",
                  "v19-2011hs-corr", "v19-2013df-corr", "v19-2016gkg-corr"]
        
    _RATE = 5.4e4 # Perley CC 1e5 * (0.75 *0.72) for Type II.

    

    
    
