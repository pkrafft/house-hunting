import sys
import simulate
import numpy as np

exp = sys.argv[1]

# default values
n_iter = 1000
n_ants = 100
n_sites = 50
search_prob = 0.05
quorum_size = 15
site_qual = 0.5

def experiment(n_iter, n_ants, n_sites, search_prob, quorum_size, site_qual, test = False):
    
    ave_time = 0
    ave_diff = 0
    times = 0
    diffs = 0
    splits = 0
    
    for i in range(n_iter):
        
        colony = simulate.Colony(n_ants, n_sites, search_prob, quorum_size, site_qual, test = test)
        decision_times = colony.main()
        d_times = [decision_times[i] for i in decision_times]

        d_times.sort()
        if len(d_times) > 0:
            ave_time += d_times[0]
            times += 1
        if len(d_times) > 1:
            ave_diff += d_times[1] - d_times[0]
            diffs += 1
            splits += 1
    
    ave_time = float(ave_time)/times
    if diffs > 0:
        ave_diff = float(ave_diff)/diffs
    else:
        ave_diff = 'NA'
    prob_split = float(splits)/n_iter
    
    print n_sites, search_prob, quorum_size, site_qual, ave_time, ave_diff, prob_split

if exp == "sites":
    n_nests = range(1,51)
    for x in n_nests:
        experiment(n_iter, n_ants, x, search_prob, quorum_size, site_qual)

if exp == "search":
    probs = [x/20.0 for x in range(1,21)]
    for x in probs:
        experiment(n_iter, n_ants, n_sites, x, quorum_size, site_qual)

if exp == "quorum":
    quorum_sizes = [2**x for x in range(7)]
    for x in quorum_sizes:
        experiment(n_iter, n_ants, n_sites, search_prob, x, site_qual)

if exp == "qual":
    quals = [x/10.0 for x in range(1,10)]
    for x in quals:
        experiment(n_iter, n_ants, n_sites, search_prob, quorum_size, x)

if exp == "ants":
    ants = [x*20 for x in range(1,21)]
    for x in ants:
        experiment(n_iter, x, n_sites, search_prob, quorum_size, site_qual)

if exp == "single":
    experiment(1, n_ants, n_sites, search_prob, quorum_size, site_qual, test = True)
