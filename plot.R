
data = read.table('../output/qual.out')
plot(data[,4],data[,5], xlab = "Site Quality", ylab = "Time to Quorum", type = 'l')
plot(data[,4],data[,6]/data[,5], xlab = "Site Quality", ylab = "Split Time", type = 'l')

data = read.table('../output/search.out')
plot(data[,2],data[,5], xlab = "Search Prob", ylab = "Time to Quorum", type = 'l')
plot(data[,2],data[,6]/data[,5], xlab = "Search Prob", ylab = "Split Time", type = 'l')

data = read.table('../output/quorum.out')
plot(data[,3],data[,5], xlab = "Quorum Size", ylab = "Time to Quorum", type = 'l')
plot(data[,3],data[,6]/data[,5], xlab = "Quorum Size", ylab = "Split Time", type = 'l')

data = read.table('../output/sites.out')
pdf('../plots/sites-split.pdf')
plot(data[,1],data[,5], xlab = "Number of Sites", ylab = "Time to Quorum", type = 'l', ylim = c(min(data[,5],data[,6], na.rm = T), max(data[,5],data[,6], na.rm = T)))
lines(data[,1],data[,6], col = 'red')
legend('bottomright', c('to first quorum','to second quorum'), lty = 1, col = c('black','red'))
dev.off()
