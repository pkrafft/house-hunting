
random = read.table('../output/random-time.out')
equal = read.table('../output/equal-time.out')

pdf('../plots/runtime.pdf')
ylim = c(min(c(random[,2],equal[,2])), max(c(random[,2],equal[,2])))
plot(random, type = 'l', ylim = ylim,
     xlab = 'number of sites', ylab = 'average steps to quorum',
     main = '100 ants, 0.01 search prob, quorum size 10')
lines(equal, lty = 2)
legend('bottomright', c('random qualities','equal qualities'), lty = c(1,2))
dev.off()

random = read.table('../output/random-split.out')
equal = read.table('../output/equal-split.out')

pdf('../plots/splitprob.pdf')
plot(random, type = 'l', ylim = c(0,1),
     xlab = 'number of sites', ylab = 'probability of multiple sites reaching a quorum',
     main = '100 ants, 0.01 search prob, quorum size 10')
lines(equal, lty = 2)
legend('bottomright', c('random qualities','equal qualities'), lty = c(1,2))
dev.off()
