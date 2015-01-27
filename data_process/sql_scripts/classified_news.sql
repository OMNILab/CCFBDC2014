-- Usage: mysql -h 10.50.15.191 -p -u omnilab < classified_news.sql
USE omnilab_bd;


-- Create temp table to store updated events
CREATE TEMPORARY TABLE classified_news_tmp (
	event_id BIGINT NOT NULL,
	event_tag INT NOT NULL,
	day_offset BIGINT NOT NULL,
	news_id VARCHAR(128),
	news_title VARCHAR(1024),
	content VARCHAR(1024),
	PRIMARY KEY (news_id));

-- Upload data in file to temp table
LOAD DATA LOCAL INFILE 'classified_news.txt' INTO TABLE classified_news_tmp
	FIELDS TERMINATED BY '\t';

-- Add new columns about detected events
ALTER TABLE t_lable_group_comp ADD (
		event_id BIGINT NOT NULL,
		event_tag INT NOT NULL,
		day_offset BIGINT NOT NULL,
		content VARCHAR(1024)
		);

-- Update target table with temp table
UPDATE t_lable_group_comp e, classified_news_tmp et SET
	e.event_id = et.event_id,
	e.event_tag = et.event_tag,
	e.day_offset = et.day_offset,
	e.content = et.content
	WHERE e.id = et.news_id;

-- Weibo
CREATE TEMPORARY TABLE classified_weibo_tmp (
	event_id BIGINT NOT NULL,
	event_tag INT NOT NULL,
	day_offset BIGINT NOT NULL,
	news_id VARCHAR(128),
	news_title VARCHAR(1024),
	#content VARCHAR(1024),
	PRIMARY KEY (news_id));

-- Upload data in file to temp table
LOAD DATA LOCAL INFILE 'classified_weibo.txt' INTO TABLE classified_weibo_tmp
	FIELDS TERMINATED BY '\t';

-- Update target table with temp table
UPDATE t_lable_group_comp e, classified_weibo_tmp et SET
	e.event_id = et.event_id,
	e.event_tag = et.event_tag,
	e.day_offset = et.day_offset,
	e.content = et.news_title
	WHERE e.id = et.news_id;

-- Create new table with filtered news
DROP TABLE t_lable_filtered;
CREATE TABLE IF NOT EXISTS t_lable_filtered LIKE t_lable_group_comp;
INSERT INTO t_lable_filtered SELECT * FROM t_lable_group_comp WHERE event_tag > 0;

-- Create temp table to store updated events
-- DROP TABLE table_id_title_news;
-- CREATE TABLE table_id_title_news (
-- 	event_id CHAR(255) NOT NULL,
-- 	title VARCHAR(1024),
-- 	hit_tag INT NOT NULL,
-- 	event_tag INT NOT NULL,
-- 	content VARCHAR(1024));
-- INSERT INTO table_id_title_news SELECT id,title,hit_tag,event_tag,format_content FROM t_lable_group_comp WHERE source_type = 0;
-- DROP TABLE table_read_time;
-- CREATE TABLE table_read_time (
-- 	name VARCHAR(1024),
-- 	time_read VARCHAR(1024));
-- LOAD DATA LOCAL INFILE 'fenpei.txt' INTO TABLE table_read_time
-- FIELDS TERMINATED BY '|';
-- INSERT INTO table_id_title_weibo SELECT id,hit_tag,event_tag,title,format_content FROM t_lable_group_comp WHERE source_type = 4;