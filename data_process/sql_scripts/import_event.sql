-- Usage: mysql -h 10.50.15.191 -p -u omnilab < import_event.sql
USE omnilab_bd;

-- Create target table if its not there
CREATE TABLE IF NOT EXISTS event_attributes (
	event_id BIGINT NOT NULL,
	event_tag INT NOT NULL,
	day_offset BIGINT NOT NULL,
	name_title VARCHAR(1024),
	addr_title VARCHAR(1024),
	name_content VARCHAR(1024),
	addr_contnet VARCHAR(1024),
	PRIMARY KEY (event_id));

-- Create temp table to store updated events
CREATE TEMPORARY TABLE event_attributes_tmp (
	event_id BIGINT NOT NULL,
	event_tag INT NOT NULL,
	day_offset BIGINT NOT NULL,
	name_title VARCHAR(1024),
	addr_title VARCHAR(1024),
	name_content VARCHAR(1024),
	addr_contnet VARCHAR(1024),
	PRIMARY KEY (event_id));

-- Upload data in file to temp table
LOAD DATA LOCAL INFILE 'classified_event.txt' INTO TABLE event_attributes_tmp
	FIELDS TERMINATED BY '|';

-- Copy data from tmp db to formal db
INSERT INTO event_attributes (event_id, event_tag, day_offset,
	name_title, addr_title, name_content, addr_contnet)
	SELECT event_id, event_tag, day_offset,
	name_title, addr_title, name_content, addr_contnet
	FROM event_attributes_tmp;

-- Update target table with temp table
UPDATE event_attributes e, event_attributes_tmp et SET
	e.event_tag = et.event_tag,
	e.day_offset = et.day_offset,
	e.name_title = et.name_title,
	e.addr_title = et.addr_title,
	e.name_content = et.name_content,
	e.addr_contnet = et.addr_contnet
	where e.event_id = et.event_id;