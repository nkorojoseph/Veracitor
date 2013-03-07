""" 
TidalTrust! 

"""

import networkx as nx


class TidalTrust:

    # queue.append(x) Adds x to the end of the list.
    # queue.pop() Removes and returns the last item of the list. Optional argument: index.
    # len(queue) Returns the length of the list.
    
    # A queue of nodes at the current depth
    queue = []
    
    # TODO?
    cached_ratings = {}
    
    def tidal_trust(source, sink, graph):
        """ Calculates a trust value between the source and the sink nodes in the given graph """
        queue.push(source)
        depth = 1
        maxdepth = sys.maxint    # "Infinity" value. This value can be exceeded in python. longs have no explicit upper limit.
    
    
    

     
