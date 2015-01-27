library(minerva)
library(lattice)

i <- 3

#公交车爆炸features_1，暴恐事件features_2，校园砍杀features_3
input_file1 <- "features_1"
#特征名称
input_file2 <- "feature_readme.txt"

features <- read.csv(paste(input_file1, i, ".txt", sep=""),
                     head=F, sep='\t',stringsAsFactors=T)
summary(pc.cr <- princomp(features[,2:length(features)]))

features.names <- read.csv(input_file2, head=F)
colnames(features) <- features.names[,1]

# pc.cr$scores
# pca.plot <- xyplot(pc.cr$scores[,2] ~ pc.cr$scores[,1])
# pca.plot$xlab <- "First Component"
# pca.plot$ylab <- "Second Component"
# pca.plot
#
# mic <- mine(features[,2:ncol(features)])
# #saveRDS(mic, "mic.rds")
# svg("figures/feature_space.svg", width=6, height=6)
# image(mic$MIC, xlab="特征索引",ylab="特征索引")
# dev.off()
#
# hclust(mic$MIC)

######################################################
# Spatial connections
library(gclus)
library(stringr)
cor.pair <- function(dta, title){
  dta <- as.data.frame(sapply(dta, function(x) jitter(x, factor=.8)))
  dta.r <- abs(cor(dta)) # get correlations
  dta.col <- dmat.color(dta.r) # get colors
  # reorder variables so those with highest correlation
  # are closest to the diagonal
  dta.o <- order.single(dta.r)
  labels <- sapply(str_split(colnames(dta), '_'), function(x) x[1])
  cpairs(dta, dta.o, panel.colors=dta.col, gap=.5, pch=1, lwd=.1,
         cex=.6,main=title, labels=labels)
}

# Area connections
titles <- c("公交爆炸事件的地区相关性(红>绿>黄)",
            "暴力恐怖事件的地区相关性(红>绿>黄)",
            "校园砍杀事件的地区相关性(红>绿>黄)")
svg(paste("figures/area_cor_cls", i, ".svg", sep=""), width=6, height=6)
cor.pair(features[,41:48], titles[i])
dev.off()

# cor.pair(features[,c(c(3,8), 47, 92, 98, 104, 201)])

######################################################
# Temporal connections
library(RMySQL)
mydb <- dbConnect(MySQL(), user='omnilab', password='omnilab',
                  dbname='omnilab_bd', host='10.50.15.191')
dbSendQuery(mydb,'SET NAMES utf8')
sq <- dbSendQuery(mydb, "SELECT event_id, event_tag, day_offset, duration,
                  total_news, total_weibo
                  FROM event_attributes;")
events <- fetch(sq, n=-1)
colnames(events) <- c("eid", "etag", "time", "dur","news","weibo")
mysqlCloseConnection(mydb)

library(dplyr)
events <- events %>%
  mutate(
    date = as.Date("2011-04-01") + time,
    rpt = news + weibo,
    rpt = ifelse(is.na(rpt), 0, rpt))
events$etag <- as.factor(events$etag)

library(pracma)
library(xts)
library(ggplot2)
gg <- ggplot(events, aes(date, rpt, group=etag, color=etag)) + 
  theme_bw() + geom_line() + ylim(0,2000) +
  xlim(as.Date("2013-05-01"), as.Date("2014-04-30"))
plot(gg)

svg("figures/time_pacf.svg", height=9, width=6)
par(mfrow=c(3,1), mar=c(5,5,2,2), cex.lab=1.5)
titles = c("公交爆炸事件","暴力恐怖事件","校园砍杀事件")
df.acf <- data.frame()
for( i in 1:3){
  events.one <- events[events$etag==i,]
  events.one.ts <- xts(events.one$rpt, events.one$date)
  hurstexp(xts(events.one$rpt, events.one$date))
  v <- acf(coredata(events.one.ts), type="partial", plot=F)
  df.acf <- df.acf %>% rbind(data.frame(lag=v$lag, acf=v$acf, t=i))
  plot(v$lag, v$acf, main=titles[i], pch=21, type="h",
       xlab="时间间隔", ylab="偏自相关函数(PACF)", ylim=c(-0.1, 0.2),
       lwd=3)
  points(v$lag, v$acf, pch=21, col="black", cex=1, bg="green")
  n <- length(events.one.ts)
  abline(h=-1.96/sqrt(n), lty=2, col="red")
  abline(h=1.96/sqrt(n), lty=2, col="red")
  abline(h=0, lty=1, col="black")
}
dev.off()

df.acf$t <- as.factor(df.acf$t)
gg <- ggplot(df.acf, aes(lag, acf, group=t, fill=t)) +
  theme_bw() + geom_bar(stat="identity", position=position_dodge())
plot(gg)