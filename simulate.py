import sys
import random

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

    def __init__(self, n_sites, random_qual):
        
        self.n_ants  = 100
        self.search_prob = 0.01
        self.site_quals = [None]*n_sites
        for site in range(n_sites):
            if random_qual:
                self.site_quals[site] = random.betavariate(1,1)
            else:
                self.site_quals[site] = [0.6]
        self.n_sites = len(self.site_quals)
        self.site_pops = [0]*self.n_sites
        self.quorum_size = 10

        self.ants = [[HOME, None] for i in range(self.n_ants)]
        self.at_home = dict(zip(range(self.n_ants), self.n_ants*[True]))        
        self.going_home = {}
        self.going_to_site = {}    
    
    def main(self):
        
        t = 0
        quorum = False
        
        while not quorum:

            t += 1
            if t > MAX_STEPS:
                print "Warning: Maximum number of steps reached without quorum"
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
            
            for pop in self.site_pops:
                if pop >= self.quorum_size:
                    quorum = True
        
        return t

    def explore(self, i):
        if random.random() < self.search_prob:
            site = random.randint(0, self.n_sites - 1)
            self.ants[i][LOC] = IN_TRANSIT
            self.ants[i][SITE] = site
            del(self.at_home[i])
            self.going_to_site[i] = True
            self.site_pops[site] += 1
    
    def recruit(self, i):
        site = self.ants[i][SITE]
        if random.random() < self.site_quals[site]:
            if len(self.at_home) > 0:
                follower = random.choice(self.at_home.keys())
                self.ants[follower][SITE] = site
                del(self.at_home[follower])
                self.ants[i][LOC] = IN_TRANSIT
                self.ants[follower][LOC] = IN_TRANSIT
                self.going_to_site[i] = True
                self.going_to_site[follower] = True
                self.site_pops[site] += 2
    
    def go_home(self, i):
        site = self.ants[i][SITE]
        if random.random() < 1 - self.site_quals[site]:            
            self.site_pops[site] -= 1
            self.ants[i][LOC] = IN_TRANSIT
            self.going_home[i] = True

if __name__ == '__main__':

    rand = bool(sys.argv[1])

    n_iter = 1000
    sizes = range(1,21)
    for size in sizes:
        ave = 0
        for i in range(n_iter):
            colony = Colony(size, rand)
            ave += colony.main()
        ave = float(ave)/n_iter
        print size,ave
