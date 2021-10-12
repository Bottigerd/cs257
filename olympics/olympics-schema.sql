CREATE TABLE olympian_athletes (
	id SERIAL,
	name text,
	sex text,
	noc integer
);

CREATE TABLE noc_regions (
	id SERIAL,
	noc text,
	region text,
	notes text
);

CREATE TABLE olympics (
	id SERIAL,
	games text,
	year integer,
	season text,
	city text
);

CREATE TABLE olympic_events (
	id SERIAL,
	season text,
	sport text,
	event text,
);

CREATE TABLE olympic_event_results (
	id SERIAL,
	olympic_id integer,
	olympic_event_id integer,
	olympian_id integer,
	medal text,
);

CREATE TABLE per_olympic_athlete_data (
	id SERIAL,
	olympic_id integer,
	olympian_id integer,
	age text,
	height text,
	weight text
);
	
	