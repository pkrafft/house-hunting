
data = read.table('../output/sites.out')
pdf('../plots/sites-split.pdf')
plot(data[,1],data[,5], xlab = "Number of Sites", ylab = "Time to Quorum", type = 'l', ylim = c(min(data[,5],data[,6], na.rm = T), max(data[,5],data[,6], na.rm = T)))
lines(data[,1],data[,6], col = 'red')
legend('bottomright', c('to first quorum','to second quorum'), lty = 1, col = c('black','red'))
dev.off()

data = read.table('../output/ants.out')
pdf('../plots/ants-split.pdf')
plot(data[,1],data[,6], xlab = "Number of Ants", ylab = "Time to Quorum", type = 'l', ylim = c(min(data[,6],data[,7], na.rm = T), max(data[,6],data[,7], na.rm = T)))
lines(data[,1],3*data[,7], col = 'red')
legend('topright', c('to first quorum','to second quorum'), lty = 1, col = c('black','red'))
dev.off()
