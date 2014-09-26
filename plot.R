require("ggplot2")

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
ylim = c(min(c(random[,2],equal[,2])), max(c(random[,2],equal[,2])))
plot(random, type = 'l', ylim = ylim,
     xlab = 'number of sites', ylab = 'probability of multiple sites reaching a quorum',
     main = '100 ants, 0.01 search prob, quorum size 10')
lines(equal, lty = 2)
legend('bottomright', c('random qualities','equal qualities'), lty = c(1,2))
dev.off()

data = read.table('../output/equal-complete-time.out')
split = read.table('../output/equal-complete-split.out')
data = cbind(data, split[,3])
colnames(data) = c("sites", "quorum", "time", 'split')
data[,'quorum'] = factor(data[,'quorum'])

ggplot(data=data,
              aes(x=sites, y=time, colour=quorum)) +
        geom_line()

ggplot(data=data,
              aes(x=sites, y=split, colour=quorum)) +
        geom_line()
