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
AT_HOME = 0
AT_SITE = 1

MAX_STEPS = 10000

class Colony:
    """
    >>> c = Colony(1, True, 10, 0.05, None, test = True)
    >>> x = c.main(True)
    >>> x = c.main(False)
    >>> c = Colony(10, True, 10, 0.05, None, test = True)
    >>> x = c.main(True)
    >>> x = c.main(False)
    """
    
    def __init__(self, n_sites, random_qual, quorum_size, search_prob, site_qual, test = False):
        
        self.n_ants  = 100
        self.search_prob = search_prob
        self.site_quals = [None]*n_sites
        for site in range(n_sites):
            if random_qual:
                self.site_quals[site] = random.betavariate(1,1)
            else:
                self.site_quals[site] = [site_qual]
        self.n_sites = len(self.site_quals)
        
        self.ants = [[AT_HOME, None] for i in range(self.n_ants)]
        
        self.at_home = dict(zip(range(self.n_ants), self.n_ants*[True]))
        self.at_site = [0]*self.n_sites
        self.know_site = [0]*self.n_sites
        self.quorum_size = quorum_size
        
        self.going_home = {}
        self.going_to_site = {}
        
        self.sites_chosen = [False]*self.n_sites
        
        self.test = test
    
    def main(self, to_quorum):
        
        t = 0        
        quorum = False
        complete = False
        
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
                if self.ants[i][LOC] == AT_HOME:
                    if self.ants[i][SITE] == None:
                        if random.random() < self.search_prob:
                            site = random.randint(0, self.n_sites - 1)
                            self.explore(i, site)
                    else:
                        if len(self.at_home) > 1:
                            site = self.ants[i][SITE]
                            if random.random() < self.site_quals[site]:
                                follower = random.choice(list(set(self.at_home.keys()) - set([i])))
                                self.recruit(i, follower)
                elif self.ants[i][LOC] == AT_SITE:
                    site = self.ants[i][SITE]
                    if random.random() < 1 - self.site_quals[site]:
                        self.go_home(i)
                else:
                    assert self.ants[i][LOC] == IN_TRANSIT

            if self.test:
                self.test_invariants(0)
            
            for i in self.going_home:
                self.ants[i][LOC] = AT_HOME
                self.at_home[i] = True
            
            for i in self.going_to_site:
                self.ants[i][LOC] = AT_SITE
            
            for site,pop in enumerate(self.at_site):
                if pop >= self.quorum_size:
                    quorum = True
                    self.sites_chosen[site] = True
            for pop in self.know_site:
                if pop == self.n_ants:
                    complete = True

            if self.test:
                self.test_invariants(1)
            
            if to_quorum and quorum:
                break
        
        return (t, self.sites_chosen)

    def explore(self, i, site):
        assert self.ants[i][SITE] == None
        self.ants[i][LOC] = IN_TRANSIT
        self.ants[i][SITE] = site
        del(self.at_home[i])
        self.going_to_site[i] = True
        self.at_site[site] += 1
        self.know_site[site] += 1
    
    def recruit(self, i, follower):
        assert self.ants[i][LOC] == AT_HOME and self.ants[follower][LOC] == AT_HOME
        site = self.ants[i][SITE]
        if self.ants[follower][SITE] != None:
            self.know_site[self.ants[follower][SITE]] -= 1
        self.ants[follower][SITE] = site
        del(self.at_home[i])
        del(self.at_home[follower])
        self.ants[i][LOC] = IN_TRANSIT
        self.ants[follower][LOC] = IN_TRANSIT
        self.going_to_site[i] = True
        self.going_to_site[follower] = True
        self.at_site[site] += 2
        self.know_site[site] += 1
    
    def go_home(self, i):
        assert self.ants[i][LOC] == AT_SITE
        site = self.ants[i][SITE]
        self.at_site[site] -= 1
        self.ants[i][LOC] = IN_TRANSIT
        self.going_home[i] = True
    
    def test_invariants(self, test):
        
        for i in self.at_home:
            assert self.ants[i][LOC] == AT_HOME
        
        if test == 0:
            
            for i in self.going_home:
                assert self.ants[i][LOC] == IN_TRANSIT
            
            for i in self.going_to_site:
                assert self.ants[i][LOC] == IN_TRANSIT
        
        if test == 1:
            
            nums_know = [0]*self.n_sites
            for a in self.ants:
                if a[SITE] != None:
                    nums_know[a[SITE]] += 1
            assert nums_know == self.know_site
            
            nums_at = [0]*self.n_sites
            for a in self.ants:
                if a[LOC] == AT_SITE:
                    nums_at[a[SITE]] += 1
            assert nums_at == self.at_site
            
            assert (sum(np.array(nums_at)) + len(self.at_home)) == self.n_ants
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
