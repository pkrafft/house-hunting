
rand = bool(sys.argv[1])
to_quorum = bool(sys.argv[2])
output = sys.argv[3]

#    n_iter = 1000
n_iter = 1
n_sites = range(1,21)
n_sites = [1]
#    quorum_sizes = [1,2,4,8,16,32,64]
quorum_sizes = [50]
for m in n_sites:
    for q in quorum_sizes:
        ave = 0
        reached_quorum = 0
        split_decision = 0
        for i in range(n_iter):
            colony = Colony(m, rand, q, 0.05, 0.6)
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

