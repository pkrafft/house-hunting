
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
plot(data[,1],data[,5], xlab = "Number of Sites", ylab = "Time to Quorum", type = 'l')
plot(data[,1],data[,6]/data[,5], xlab = "Number of Sites", ylab = "Split Time", type = 'l')
abline(h = 0.5, col = 'red')
abline(h = 0.25, col = 'red')
