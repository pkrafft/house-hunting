
random = read.table('../output/random.out')
equal = read.table('../output/equal.out')

pdf('../plots/runtime.pdf')
ylim = c(min(c(random[,2],equal[,2])), max(c(random[,2],equal[,2])))
plot(random, type = 'l', ylim = ylim,
     xlab = 'number of sites', ylab = 'average steps to quorum',
     main = '100 ants, 0.01 search prob, quorum size 10')
lines(equal, lty = 2)
legend('bottomright', c('random qualities','equal qualities'), lty = c(1,2))
dev.off()
