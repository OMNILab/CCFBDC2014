library(RMySQL)
library(dplyr)
library(ggplot2)
library(stringr)

mydb <- dbConnect(MySQL(), user='omnilab', password='omnilab',
                 dbname='omnilab_bd', host='10.50.15.191')
dbSendQuery(mydb,'SET NAMES utf8')

# Read news info
sq <- dbSendQuery(mydb, "SELECT CAST(url_crc AS CHAR(50)),
                  source_type,media_name,release_date_day,
                  CAST(siteurl_crc AS CHAR(50)),content_media_name,
                  words,event_id,event_tag,day_offset,content
                  FROM t_lable_filtered")
news <- fetch(sq, n=-1)
colnames(news) <- c("tid", "source_type","media", "release", "uid",
                    "media_publish", "words", "eid", "etag", "offset",
                    "content")
news$tid <- str_trim(news$tid)
news$uid <- str_trim(news$uid)

# Read news status
sq <- dbSendQuery(mydb, "SELECT CAST(url_crc AS CHAR(50)),source_type,
                  comment_count,quote_count,attitudes_count FROM t_dpt_distinct")
news.status <- fetch(sq, n=-1)
colnames(news.status) <- c("tid", "source_type", "comment", "quote", "attitude")
news.status$tid <- str_trim(news.status$tid)

# Read weibo users info
sq <- dbSendQuery(mydb, "SELECT CAST(url_crc AS CHAR(50)),
                  location,province,gender,birthday,
                  created_at,followers_count,friends_count,statuses_count,
                  active_days,level_now FROM w_user_info_distinct")
weibors <- fetch(sq, n=-1)
colnames(weibors)  <- c("uid", "location", "province", "gender", "birthday",
                        "created_at", "followers", "friends", "statuses",
                        "active", "level")
weibors$uid <- str_trim(weibors$uid)

# Merge data sets into a unified one
news <- news %>%
  left_join(select(news.status, -source_type), by=c("tid")) %>%
  left_join(weibors, by=c("uid"))
#nrow(news[!is.na(news$gender),])
events <- news %>%
  group_by(eid, source_type) %>%
  summarise(
    total = length(unique(tid)),
    media_total = length(unique(media)),
    media_origin = length(unique(media_publish)),
    comments = sum(comment, na.rm=T),
    quotes = sum(quote, na.rm=T),
    attitudes = sum(attitude, na.rm=T),
    words_med = median(words),
    words_mean = mean(words)
  )

# Extract people and place names
extpp <- function(content){
  t <- str_replace_all(str_split(content, '[|]')[[1]], '\"', '')
  if(length(t) < 4) # patch to inconsistent format of content
    t <- c(t,rep("", 4-length(t)))
  name.stat <- function(x){
    y <- str_split(x, ' ')
    m <- do.call(rbind, str_split(unlist(y), ':'))
    if (dim(m)[2] != 2) # invalid content of location and people
      m <- cbind(m, 0)
    # 1,2 in title, 3,4 in content
    m <- data.frame(cbind(m, rep(c(1,2,3,4), sapply(y, length))))
    colnames(m) <- c("name", "n", "type")
    m[str_length(m$name)>0,]
  }
  df <- name.stat(t)
  df <- df %>% mutate(n=as.numeric(n), type=as.numeric(type))
  df
}

corpus <- news[1:1000,] %>%
  subset(source_type==0) %>%
  group_by(eid, tid) %>%
  do(extpp(.$content)) %>%
  mutate(
    # Weight names in titles
    n = n + (type <= 2) * 10,
    # Strip name suffix
    name = sapply(name, FUN=function(x){
      if (str_length(x) >= 3)
        x <- str_replace(x, "[县市省]$", "")
      return(x)}),
    # Upate types 3,4 to 1,2
    type = type - (type >= 3) * 2
    ) %>%
  # Update name frequency stat
  group_by(eid, tid, type, name) %>%
  summarise(n = sum(n)/length(n))

# Add table fields
dbSendQuery(mydb,
  "ALTER TABLE event_attributes ADD (
	total_news INT,
  total_weibo INT,
  media_total INT,
  media_origin INT,
	comments_news INT,
  comments_weibo INT,
	quotes_news INT,
  quotes_weibo INT,
  attitudes_news INT,
  attitudes_weibo INT,
  words_med_news INT,
  words_med_weibo INT,
  words_mean_news INT,
  words_mean_weibo INT
	)")

apply(events[events$source_type==4,], 1, FUN = function(e){
  dbSendQuery(mydb, paste("UPDATE event_attributes SET",
                          "total_weibo=", e[3],
                          ",media_total=", e[4],
                          ",media_origin=", e[5],
                          ",comments_weibo=", e[6],
                          ",quotes_weibo=", e[7],
                          ",attitudes_weibo=", e[8],
                          ",words_med_weibo=", e[9],
                          ",words_mean_weibo=", e[10],
                          "where event_id=", e[1]))
})

apply(events[events$source_type==0,], 1, FUN = function(e){
  dbSendQuery(mydb, paste("UPDATE event_attributes SET",
                          "total_news=", e[3],
                          ",media_total=", e[4],
                          ",media_origin=", e[5],
                          ",comments_news=", e[6],
                          ",quotes_news=", e[7],
                          ",attitudes_news=", e[8],
                          ",words_med_news=", e[9],
                          ",words_mean_news=", e[10],
                          "where event_id=", e[1]))
})

mysqlCloseConnection(mydb)
