import sys
import random
import numpy as np
import warnings

# assuming no failures for now

LOC = 0
SITE = 1
IN_TRANSIT = 2
NUM = 0
QUAL = 1
HOME = 0
AT_SITE = 1

MAX_STEPS = 10000

class Colony:

    def __init__(self, n_sites, random_qual, quorum_size):
        
        self.n_ants  = 100
        self.search_prob = 0.05
        self.site_quals = [None]*n_sites
        for site in range(n_sites):
            if random_qual:
                self.site_quals[site] = random.betavariate(1,1)
            else:
                self.site_quals[site] = [0.6]
        self.n_sites = len(self.site_quals)
        self.at_site = [0]*self.n_sites
        self.know_site = [0]*self.n_sites
        self.quorum_size = quorum_size

        self.ants = [[HOME, None] for i in range(self.n_ants)]
        self.at_home = dict(zip(range(self.n_ants), self.n_ants*[True]))        
        self.going_home = {}
        self.going_to_site = {}    
    
    def main(self, to_quorum):
        
        t = 0        
        quorum = False
        complete = False
        sites_chosen = [False]*self.n_sites
        
        while not complete:

            t += 1
            if t > MAX_STEPS:
                warnings.warn("Warning: Maximum number of steps reached without quorum")
                break
            
            self.going_home = {}
            self.going_to_site = {}
            
            inds = range(self.n_ants)
            random.shuffle(inds)
                        
            for i in inds:
                if self.ants[i][LOC] == HOME:
                    if self.ants[i][SITE] == None:
                        self.explore(i)
                    else:
                        self.recruit(i)
                elif self.ants[i][LOC] == AT_SITE:
                        self.go_home(i)
                else:
                    assert self.ants[i][LOC] == IN_TRANSIT

            for i in self.going_home:
                self.ants[i][LOC] = HOME
                self.at_home[i] = True
            
            for i in self.going_to_site:
                self.ants[i][LOC] = AT_SITE
            
            for site,pop in enumerate(self.at_site):
                if pop >= self.quorum_size:
                    quorum = True
                    sites_chosen[site] = True
            for pop in self.know_site:
                if pop == self.n_ants:
                    complete = True
            
            if to_quorum and quorum:
                break
        
        return (t,sites_chosen)

    def explore(self, i):
        if random.random() < self.search_prob:
            assert self.ants[i][SITE] == None
            site = random.randint(0, self.n_sites - 1)
            self.ants[i][LOC] = IN_TRANSIT
            self.ants[i][SITE] = site
            del(self.at_home[i])
            self.going_to_site[i] = True
            self.at_site[site] += 1
            self.know_site[site] += 1
    
    def recruit(self, i):
        site = self.ants[i][SITE]
        if random.random() < self.site_quals[site]:
            if len(self.at_home) > 0:
                follower = random.choice(self.at_home.keys())
                if self.ants[follower][SITE] != None:
                    self.know_site[self.ants[follower][SITE]] -= 1
                self.ants[follower][SITE] = site
                del(self.at_home[follower])
                self.ants[i][LOC] = IN_TRANSIT
                self.ants[follower][LOC] = IN_TRANSIT
                self.going_to_site[i] = True
                self.going_to_site[follower] = True
                self.at_site[site] += 2
                self.know_site[site] += 2
    
    def go_home(self, i):
        site = self.ants[i][SITE]
        if random.random() < 1 - self.site_quals[site]:            
            self.at_site[site] -= 1
            self.ants[i][LOC] = IN_TRANSIT
            self.going_home[i] = True

if __name__ == '__main__':

    rand = bool(sys.argv[1])
    to_quorum = bool(sys.argv[2])
    output = sys.argv[3]

    n_iter = 1000
    n_sites = range(1,21)
    quorum_sizes = [1,2,4,8,16,32,64]
    for m in n_sites:
        for q in quorum_sizes:
            ave = 0
            reached_quorum = 0
            split_decision = 0
            for i in range(n_iter):
                colony = Colony(m, rand, q)
                t,decisions = colony.main(to_quorum)
                if output == 'time':
                    ave += t
                if output == 'split':
                    n_decisions = sum(np.array(decisions))
                    if n_decisions > 0:
                        reached_quorum += 1
                    if n_decisions > 1:
                        split_decision += 1
            if output == 'time':
                ave = float(ave)/n_iter
            if output == 'split':
                ave = float(split_decision)/reached_quorum
            print m,q,ave

